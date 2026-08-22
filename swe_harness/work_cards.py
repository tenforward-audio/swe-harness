"""Validate canonical live work cards without creating presentation data."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


TRACKING_SOURCES = (
    (Path(".agents/ISSUES.md"), "intake", "issue"),
    (Path(".agents/FEATURES.md"), "intake", "feature"),
    (Path(".agents/workboard/PLANNING.md"), "planning", None),
    (Path(".agents/workboard/IN_PROGRESS.md"), "in-progress", None),
    (Path(".agents/workboard/REVIEWING.md"), "reviewing", None),
)
CARD_HEADING = re.compile(
    r"^###\s+((?:ISSUE|FEATURE)-\d{3,})\s+—\s+(.+?)\s*$", re.MULTILINE
)
FIELD_LINE = re.compile(r"^- ([A-Za-z][^:]*):(?:\s*(.*))?$")
LANE_LINE = re.compile(r"^  - Lane:\s*`?([a-z0-9][a-z0-9-]*)`?\s*$")
LANE_FIELD_LINE = re.compile(r"^    - ([A-Za-z][^:]*):(?:\s*(.*))?$")
TRACKED_ID = re.compile(r"^(?:ISSUE|FEATURE)-\d{3,}$")
DEPENDENCY_ID = re.compile(r"^(?:ISSUE|FEATURE|QUESTION)-\d{3,}$")

ISSUE_INTAKE_FIELDS = frozenset(
    {
        "Reported",
        "Type",
        "Report",
        "Expected outcome",
        "Acceptance notes",
        "Track",
        "Depends on",
        "Related to",
    }
)
FEATURE_INTAKE_FIELDS = frozenset(
    {
        "Reported",
        "User or project benefit",
        "Constraints",
        "Open questions",
        "Track",
        "Depends on",
        "Related to",
    }
)
SELECTED_FIELDS = frozenset(
    {
        "Source",
        "Outcome",
        "Scope",
        "Constraints",
        "Exit checks",
        "Manual acceptance",
        "Track",
        "Depends on",
        "Related to",
        "Owner",
        "Capabilities",
        "Next action",
    }
)
LANE_FIELDS = frozenset({"Branch", "Worktree", "Depends on", "Owns"})
WORKTREE_STATES = frozenset({"planned", "active", "retained", "missing"})


@dataclass(frozen=True)
class WorkCardFinding:
    severity: str
    message: str
    source: str | None = None


@dataclass
class _Lane:
    lane_id: str
    fields: dict[str, str]
    line: int


@dataclass
class _Card:
    identifier: str
    status: str
    kind: str
    source: str
    line: int
    fields: dict[str, str]
    lanes: list[_Lane]


def inspect_work_cards(
    root: Path, *, active_question_ids: frozenset[str] = frozenset()
) -> tuple[WorkCardFinding, ...]:
    """Return structural findings for the five canonical live tracking files."""

    resolved_root = root.resolve()
    findings: list[WorkCardFinding] = []
    cards: list[_Card] = []
    locations: dict[str, list[str]] = {}

    for relative, status, expected_kind in TRACKING_SOURCES:
        path = resolved_root / relative
        if path.is_symlink():
            findings.append(
                WorkCardFinding(
                    "ERROR",
                    f"tracking source must not be a symbolic link: {relative}",
                    relative.as_posix(),
                )
            )
            continue
        if not path.is_file():
            findings.append(
                WorkCardFinding("ERROR", f"missing tracking source: {relative}")
            )
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            findings.append(
                WorkCardFinding(
                    "ERROR",
                    f"cannot read tracking source: {relative}: {error}",
                    relative.as_posix(),
                )
            )
            continue

        parsed = _parse_cards(text, relative, status, findings)
        for card in parsed:
            if expected_kind and card.kind != expected_kind:
                findings.append(
                    WorkCardFinding(
                        "ERROR",
                        f"{card.identifier} has the wrong kind for {relative}",
                        f"{relative}:{card.line}",
                    )
                )
            locations.setdefault(card.identifier, []).append(relative.as_posix())
        cards.extend(parsed)

    for identifier, paths in sorted(locations.items()):
        if len(paths) > 1:
            findings.append(
                WorkCardFinding(
                    "ERROR",
                    f"tracked identifier {identifier} appears in multiple sources: "
                    + ", ".join(paths),
                )
            )

    in_progress_count = sum(card.status == "in-progress" for card in cards)
    if in_progress_count > 1:
        findings.append(
            WorkCardFinding(
                "ERROR",
                f"WIP limit exceeded: found {in_progress_count} in-progress cards",
            )
        )

    dependencies = _validate_references(cards, active_question_ids, findings)
    _validate_dependency_cycles(
        cards, dependencies, findings, external_ids=active_question_ids
    )
    return tuple(findings)


def _parse_cards(
    text: str,
    relative: Path,
    status: str,
    findings: list[WorkCardFinding],
) -> list[_Card]:
    matches = list(CARD_HEADING.finditer(text))
    cards: list[_Card] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[match.end() : end]
        line = text.count("\n", 0, match.start()) + 1
        identifier = match.group(1)
        kind = "issue" if identifier.startswith("ISSUE-") else "feature"
        fields, lanes = _parse_fields(
            body, relative, line + 1, identifier, findings
        )
        card = _Card(
            identifier,
            status,
            kind,
            relative.as_posix(),
            line,
            fields,
            lanes,
        )
        _validate_card(card, findings)
        cards.append(card)
    return cards


def _parse_fields(
    body: str,
    relative: Path,
    first_line: int,
    identifier: str,
    findings: list[WorkCardFinding],
) -> tuple[dict[str, str], list[_Lane]]:
    fields: dict[str, str] = {}
    lanes: list[_Lane] = []
    current_field: str | None = None
    current_lane: _Lane | None = None
    in_lanes = False

    for offset, raw_line in enumerate(body.splitlines()):
        line_number = first_line + offset
        if raw_line == "- Lanes:":
            if "Lanes" in fields:
                findings.append(
                    WorkCardFinding(
                        "ERROR",
                        f"{identifier} contains duplicate field Lanes",
                        f"{relative}:{line_number}",
                    )
                )
            fields["Lanes"] = ""
            current_field = "Lanes"
            current_lane = None
            in_lanes = True
            continue

        lane_match = LANE_LINE.match(raw_line) if in_lanes else None
        if lane_match:
            current_lane = _Lane(lane_match.group(1), {}, line_number)
            lanes.append(current_lane)
            continue

        lane_field_match = LANE_FIELD_LINE.match(raw_line) if current_lane else None
        if lane_field_match:
            key = lane_field_match.group(1).strip()
            value = (lane_field_match.group(2) or "").strip()
            if key in current_lane.fields:
                findings.append(
                    WorkCardFinding(
                        "ERROR",
                        f"{identifier} lane {current_lane.lane_id} contains "
                        f"duplicate field {key}",
                        f"{relative}:{line_number}",
                    )
                )
            current_lane.fields[key] = value
            continue

        field_match = FIELD_LINE.match(raw_line)
        if field_match:
            in_lanes = False
            current_lane = None
            key = field_match.group(1).strip()
            value = (field_match.group(2) or "").strip()
            if key in fields:
                findings.append(
                    WorkCardFinding(
                        "ERROR",
                        f"{identifier} contains duplicate field {key}",
                        f"{relative}:{line_number}",
                    )
                )
            fields[key] = value
            current_field = key
            continue

        stripped = raw_line.strip()
        if stripped and current_field and not in_lanes:
            fields[current_field] = (fields[current_field] + "\n" + stripped).strip()
    return fields, lanes


def _validate_card(card: _Card, findings: list[WorkCardFinding]) -> None:
    if card.status == "intake":
        required = (
            ISSUE_INTAKE_FIELDS if card.kind == "issue" else FEATURE_INTAKE_FIELDS
        )
        allowed = required
    else:
        required = SELECTED_FIELDS | (
            {"Evidence"} if card.status == "reviewing" else set()
        )
        allowed = SELECTED_FIELDS | {"Lanes", "Common base", "Evidence"}

    for key in sorted(required):
        if not card.fields.get(key, "").strip():
            findings.append(
                WorkCardFinding(
                    "ERROR",
                    f"{card.identifier} is missing required field {key}",
                    f"{card.source}:{card.line}",
                )
            )
    for key in sorted(set(card.fields) - allowed):
        findings.append(
            WorkCardFinding(
                "NOTE",
                f"{card.identifier} contains unrecognised field {key}",
                f"{card.source}:{card.line}",
            )
        )

    if card.kind == "issue" and card.status == "intake":
        issue_type = card.fields.get("Type")
        if issue_type and issue_type not in {"bug", "task", "maintenance", "security"}:
            findings.append(
                WorkCardFinding(
                    "ERROR",
                    f"{card.identifier} has unsupported issue type {issue_type}",
                    f"{card.source}:{card.line}",
                )
            )

    if "Lanes" in card.fields and not card.lanes:
        findings.append(
            WorkCardFinding(
                "ERROR",
                f"{card.identifier} defines Lanes without any lane entries",
                f"{card.source}:{card.line}",
            )
        )
    if card.lanes and card.status != "in-progress":
        findings.append(
            WorkCardFinding(
                "ERROR",
                f"{card.identifier} may define Lanes only while In progress",
                f"{card.source}:{card.line}",
            )
        )
    if card.lanes and not card.fields.get("Common base"):
        findings.append(
            WorkCardFinding(
                "ERROR",
                f"{card.identifier} with Lanes is missing required field Common base",
                f"{card.source}:{card.line}",
            )
        )

    lane_ids: set[str] = set()
    for lane in card.lanes:
        if lane.lane_id in lane_ids:
            findings.append(
                WorkCardFinding(
                    "ERROR",
                    f"{card.identifier} contains duplicate lane {lane.lane_id}",
                    f"{card.source}:{lane.line}",
                )
            )
        lane_ids.add(lane.lane_id)
        for key in sorted(LANE_FIELDS):
            if not lane.fields.get(key):
                findings.append(
                    WorkCardFinding(
                        "ERROR",
                        f"{card.identifier} lane {lane.lane_id} is missing required "
                        f"field {key}",
                        f"{card.source}:{lane.line}",
                    )
                )
        for key in sorted(set(lane.fields) - LANE_FIELDS):
            findings.append(
                WorkCardFinding(
                    "NOTE",
                    f"{card.identifier} lane {lane.lane_id} contains unrecognised "
                    f"field {key}",
                    f"{card.source}:{lane.line}",
                )
            )
        worktree = _plain(lane.fields.get("Worktree", ""))
        if worktree and worktree not in WORKTREE_STATES:
            findings.append(
                WorkCardFinding(
                    "ERROR",
                    f"{card.identifier} lane {lane.lane_id} has unsupported "
                    f"Worktree state {worktree}",
                    f"{card.source}:{lane.line}",
                )
            )


def _validate_references(
    cards: list[_Card],
    active_question_ids: frozenset[str],
    findings: list[WorkCardFinding],
) -> tuple[tuple[str, str], ...]:
    card_ids = {card.identifier for card in cards}
    dependencies: list[tuple[str, str]] = []

    for card in cards:
        for field_name in ("Depends on", "Related to"):
            for reference in _references(card.fields.get(field_name)):
                allowed_pattern = (
                    DEPENDENCY_ID if field_name == "Depends on" else TRACKED_ID
                )
                if not allowed_pattern.fullmatch(reference):
                    findings.append(
                        WorkCardFinding(
                            "ERROR",
                            f"{card.identifier} has malformed {field_name} reference "
                            f"{reference}",
                            f"{card.source}:{card.line}",
                        )
                    )
                    continue
                if reference == card.identifier:
                    findings.append(
                        WorkCardFinding(
                            "ERROR",
                            f"{card.identifier} cannot reference itself",
                            f"{card.source}:{card.line}",
                        )
                    )
                    continue
                if reference.startswith("QUESTION-"):
                    if reference not in active_question_ids:
                        findings.append(
                            WorkCardFinding(
                                "ERROR",
                                f"{card.identifier} references missing active "
                                f"planning question {reference}",
                                f"{card.source}:{card.line}",
                            )
                        )
                        continue
                elif reference not in card_ids:
                    findings.append(
                        WorkCardFinding(
                            "ERROR",
                            f"{card.identifier} references missing live card {reference}",
                            f"{card.source}:{card.line}",
                        )
                    )
                    continue
                if field_name == "Depends on":
                    dependencies.append((reference, card.identifier))

        lane_ids = {lane.lane_id for lane in card.lanes}
        for lane in card.lanes:
            lane_id = f"{card.identifier}#{lane.lane_id}"
            for reference in _references(lane.fields.get("Depends on")):
                if reference == lane.lane_id:
                    findings.append(
                        WorkCardFinding(
                            "ERROR",
                            f"{card.identifier} lane {lane.lane_id} cannot depend on itself",
                            f"{card.source}:{lane.line}",
                        )
                    )
                    continue
                if reference not in lane_ids:
                    findings.append(
                        WorkCardFinding(
                            "ERROR",
                            f"{card.identifier} lane {lane.lane_id} references missing "
                            f"lane {reference}",
                            f"{card.source}:{lane.line}",
                        )
                    )
                    continue
                dependencies.append(
                    (f"{card.identifier}#{reference}", lane_id)
                )
    return tuple(dependencies)


def _validate_dependency_cycles(
    cards: list[_Card],
    dependencies: tuple[tuple[str, str], ...],
    findings: list[WorkCardFinding],
    *,
    external_ids: frozenset[str] = frozenset(),
) -> None:
    identifiers = {card.identifier for card in cards}
    identifiers.update(external_ids)
    identifiers.update(
        f"{card.identifier}#{lane.lane_id}" for card in cards for lane in card.lanes
    )
    adjacency: dict[str, list[str]] = {identifier: [] for identifier in identifiers}
    for source, target in dependencies:
        adjacency[source].append(target)

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(identifier: str, trail: list[str]) -> None:
        if identifier in visiting:
            start = trail.index(identifier)
            cycle = trail[start:]
            findings.append(
                WorkCardFinding(
                    "ERROR", "dependency cycle detected: " + " -> ".join(cycle)
                )
            )
            return
        if identifier in visited:
            return
        visiting.add(identifier)
        for child in sorted(adjacency[identifier]):
            visit(child, trail + [child])
        visiting.remove(identifier)
        visited.add(identifier)

    for identifier in sorted(adjacency):
        visit(identifier, [identifier])


def _references(value: str | None) -> tuple[str, ...]:
    if not value or _plain(value).lower() in {"none", "not applicable"}:
        return ()
    return tuple(_plain(part) for part in value.split(",") if _plain(part))


def _plain(value: str) -> str:
    stripped = value.strip()
    if len(stripped) >= 2 and stripped[0] == stripped[-1] == "`":
        return stripped[1:-1]
    return stripped
