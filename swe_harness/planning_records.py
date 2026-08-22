"""Validate durable planning maps, questions, fog, and resolutions."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


ACTIVE_PATH = Path(".agents/planning/ACTIVE.md")
LEDGER_PATH = Path(".agents/planning/LEDGER.md")
RECORD_HEADING = re.compile(
    r"^###\s+((?:MAP|QUESTION)-\d{3,})\s+—\s+(.+?)\s*$", re.MULTILINE
)
FIELD_LINE = re.compile(r"^- ([A-Za-z][^:]*):(?:\s*(.*))?$")
MAP_ID = re.compile(r"^MAP-(\d{3,})$")
QUESTION_ID = re.compile(r"^QUESTION-(\d{3,})$")
FOG_ID = re.compile(r"^FOG-(\d{3,})$")
FOG_ENTRY = re.compile(r"^(FOG-\d{3,})\s+—\s+(.+)$")
COUNTER = re.compile(
    r"^- Next (map|question|fog):\s*`((?:MAP|QUESTION|FOG)-\d{3,})`\s*$",
    re.MULTILINE,
)

MAP_ACTIVE_FIELDS = frozenset(
    {
        "Source",
        "Destination",
        "Scope",
        "Notes",
        "Fog",
        "Out of scope",
        "Resolved questions",
        "Next action",
    }
)
MAP_LEDGER_FIELDS = MAP_ACTIVE_FIELDS | {"Outcome", "Concluded"}
QUESTION_COMMON_FIELDS = frozenset(
    {
        "Map",
        "Kind",
        "Question",
        "Why it matters",
        "Answerable by",
        "Origin",
        "Depends on",
        "Related to",
    }
)
QUESTION_ACTIVE_FIELDS = QUESTION_COMMON_FIELDS | {"Revisit when", "Next action"}
QUESTION_LEDGER_FIELDS = QUESTION_COMMON_FIELDS | {
    "Resolution",
    "Rationale",
    "Evidence",
    "Resolved",
    "Informs",
}
QUESTION_KINDS = frozenset({"decision", "research", "experiment", "enabling-task"})
ANSWERERS = frozenset({"user", "agent", "either"})


@dataclass(frozen=True)
class PlanningRecordFinding:
    severity: str
    message: str
    source: str | None = None


@dataclass(frozen=True)
class PlanningRecordIndex:
    findings: tuple[PlanningRecordFinding, ...]
    map_ids: frozenset[str]
    active_map_ids: frozenset[str]
    question_ids: frozenset[str]
    active_question_ids: frozenset[str]
    resolved_question_ids: frozenset[str]


@dataclass
class _Record:
    identifier: str
    state: str
    source: str
    line: int
    fields: dict[str, str]


def inspect_planning_records(root: Path) -> tuple[PlanningRecordFinding, ...]:
    """Return structural findings for the planning map and ledger."""

    return index_planning_records(root).findings


def index_planning_records(root: Path) -> PlanningRecordIndex:
    """Return validated planning identifiers for cross-record checks."""

    resolved_root = root.resolve()
    findings: list[PlanningRecordFinding] = []
    records: list[_Record] = []
    active_text = ""

    for relative, state in ((ACTIVE_PATH, "active"), (LEDGER_PATH, "ledger")):
        path = resolved_root / relative
        if path.is_symlink():
            findings.append(
                PlanningRecordFinding(
                    "ERROR",
                    f"planning source must not be a symbolic link: {relative}",
                    relative.as_posix(),
                )
            )
            continue
        if not path.is_file():
            findings.append(
                PlanningRecordFinding("ERROR", f"missing planning source: {relative}")
            )
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            findings.append(
                PlanningRecordFinding(
                    "ERROR",
                    f"cannot read planning source: {relative}: {error}",
                    relative.as_posix(),
                )
            )
            continue
        if state == "active":
            active_text = text
        records.extend(_parse_records(text, relative, state, findings))

    locations: dict[str, list[str]] = {}
    for record in records:
        locations.setdefault(record.identifier, []).append(record.source)
    for identifier, paths in sorted(locations.items()):
        if len(paths) > 1:
            findings.append(
                PlanningRecordFinding(
                    "ERROR",
                    f"planning identifier {identifier} appears multiple times: "
                    + ", ".join(paths),
                )
            )

    maps = {
        record.identifier: record
        for record in records
        if record.identifier.startswith("MAP-")
    }
    questions = {
        record.identifier: record
        for record in records
        if record.identifier.startswith("QUESTION-")
    }
    active_maps = {
        identifier for identifier, record in maps.items() if record.state == "active"
    }
    active_questions = {
        identifier
        for identifier, record in questions.items()
        if record.state == "active"
    }
    resolved_questions = set(questions) - active_questions

    dependencies: list[tuple[str, str]] = []
    issued_fog_ids: set[str] = set()
    active_fog_ids: set[str] = set()
    for record in maps.values():
        record_fog_ids = _validate_map(
            record, resolved_questions, questions, issued_fog_ids, findings
        )
        if record.state == "active":
            active_fog_ids.update(record_fog_ids)
    for record in questions.values():
        dependencies.extend(
            _validate_question(
                record,
                maps,
                questions,
                active_maps,
                active_fog_ids,
                issued_fog_ids,
                findings,
            )
        )
    for identifier in sorted(resolved_questions):
        question = questions[identifier]
        map_id = _plain(question.fields.get("Map", ""))
        map_record = maps.get(map_id)
        if map_record and identifier not in _references(
            map_record.fields.get("Resolved questions")
        ):
            findings.append(
                PlanningRecordFinding(
                    "ERROR",
                    f"{identifier} is missing from {map_id} Resolved questions",
                    f"{question.source}:{question.line}",
                )
            )

    _validate_dependency_cycles(set(questions), dependencies, findings)
    _validate_counters(
        active_text, set(maps), set(questions), issued_fog_ids, findings
    )

    return PlanningRecordIndex(
        tuple(findings),
        frozenset(maps),
        frozenset(active_maps),
        frozenset(questions),
        frozenset(active_questions),
        frozenset(resolved_questions),
    )


def _parse_records(
    text: str,
    relative: Path,
    state: str,
    findings: list[PlanningRecordFinding],
) -> list[_Record]:
    matches = list(RECORD_HEADING.finditer(text))
    records: list[_Record] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        line = text.count("\n", 0, match.start()) + 1
        fields = _parse_fields(
            text[match.end() : end], relative, line + 1, match.group(1), findings
        )
        record = _Record(
            match.group(1), state, relative.as_posix(), line, fields
        )
        _validate_fields(record, findings)
        records.append(record)
    return records


def _parse_fields(
    body: str,
    relative: Path,
    first_line: int,
    identifier: str,
    findings: list[PlanningRecordFinding],
) -> dict[str, str]:
    fields: dict[str, str] = {}
    current: str | None = None
    for offset, raw_line in enumerate(body.splitlines()):
        match = FIELD_LINE.match(raw_line)
        if match:
            key = match.group(1).strip()
            value = (match.group(2) or "").strip()
            if key in fields:
                findings.append(
                    PlanningRecordFinding(
                        "ERROR",
                        f"{identifier} contains duplicate field {key}",
                        f"{relative}:{first_line + offset}",
                    )
                )
            fields[key] = value
            current = key
            continue
        stripped = raw_line.strip()
        if stripped and current:
            fields[current] = (fields[current] + "\n" + stripped).strip()
    return fields


def _validate_fields(
    record: _Record, findings: list[PlanningRecordFinding]
) -> None:
    if record.identifier.startswith("MAP-"):
        required = MAP_ACTIVE_FIELDS if record.state == "active" else MAP_LEDGER_FIELDS
    else:
        required = (
            QUESTION_ACTIVE_FIELDS
            if record.state == "active"
            else QUESTION_LEDGER_FIELDS
        )
    for key in sorted(required):
        if not record.fields.get(key, "").strip():
            findings.append(
                PlanningRecordFinding(
                    "ERROR",
                    f"{record.identifier} is missing required field {key}",
                    f"{record.source}:{record.line}",
                )
            )
    for key in sorted(set(record.fields) - required):
        findings.append(
            PlanningRecordFinding(
                "NOTE",
                f"{record.identifier} contains unrecognised field {key}",
                f"{record.source}:{record.line}",
            )
        )


def _validate_map(
    record: _Record,
    resolved_question_ids: set[str],
    questions: dict[str, _Record],
    fog_ids: set[str],
    findings: list[PlanningRecordFinding],
) -> set[str]:
    for reference in _references(record.fields.get("Resolved questions")):
        if reference not in resolved_question_ids:
            findings.append(
                PlanningRecordFinding(
                    "ERROR",
                    f"{record.identifier} references unresolved or missing "
                    f"question {reference}",
                    f"{record.source}:{record.line}",
                )
            )
        elif _plain(questions[reference].fields.get("Map", "")) != record.identifier:
            findings.append(
                PlanningRecordFinding(
                    "ERROR",
                    f"{record.identifier} references question {reference} "
                    "from another map",
                    f"{record.source}:{record.line}",
                )
            )

    fog = record.fields.get("Fog", "")
    if _plain(fog).lower() in {"none", "not applicable"}:
        return set()
    record_fog_ids: set[str] = set()
    for line in fog.splitlines():
        entry = line.removeprefix("- ").strip()
        match = FOG_ENTRY.fullmatch(entry)
        if not match:
            findings.append(
                PlanningRecordFinding(
                    "ERROR",
                    f"{record.identifier} has malformed Fog entry {entry}",
                    f"{record.source}:{record.line}",
                )
            )
            continue
        fog_id = match.group(1)
        if fog_id in fog_ids:
            findings.append(
                PlanningRecordFinding(
                    "ERROR",
                    f"duplicate fog identifier {fog_id}",
                    f"{record.source}:{record.line}",
                )
            )
        fog_ids.add(fog_id)
        record_fog_ids.add(fog_id)
    return record_fog_ids


def _validate_question(
    record: _Record,
    maps: dict[str, _Record],
    questions: dict[str, _Record],
    active_map_ids: set[str],
    active_fog_ids: set[str],
    issued_fog_ids: set[str],
    findings: list[PlanningRecordFinding],
) -> list[tuple[str, str]]:
    map_id = _plain(record.fields.get("Map", ""))
    if map_id not in maps:
        findings.append(
            PlanningRecordFinding(
                "ERROR",
                f"{record.identifier} references missing map {map_id}",
                f"{record.source}:{record.line}",
            )
        )
    elif record.state == "active" and map_id not in active_map_ids:
        findings.append(
            PlanningRecordFinding(
                "ERROR",
                f"{record.identifier} cannot remain open under concluded map {map_id}",
                f"{record.source}:{record.line}",
            )
        )

    kind = _plain(record.fields.get("Kind", ""))
    if kind and kind not in QUESTION_KINDS:
        findings.append(
            PlanningRecordFinding(
                "ERROR",
                f"{record.identifier} has unsupported Kind {kind}",
                f"{record.source}:{record.line}",
            )
        )
    answerer = _plain(record.fields.get("Answerable by", ""))
    if answerer and answerer not in ANSWERERS:
        findings.append(
            PlanningRecordFinding(
                "ERROR",
                f"{record.identifier} has unsupported Answerable by {answerer}",
                f"{record.source}:{record.line}",
            )
        )

    origin = _plain(record.fields.get("Origin", ""))
    if (
        origin.lower() not in {"none", "not applicable", ""}
        and not FOG_ID.fullmatch(origin)
    ):
        findings.append(
            PlanningRecordFinding(
                "ERROR",
                f"{record.identifier} has malformed Origin {origin}",
                f"{record.source}:{record.line}",
            )
        )
    elif FOG_ID.fullmatch(origin):
        if origin in active_fog_ids:
            findings.append(
                PlanningRecordFinding(
                    "ERROR",
                    f"{record.identifier} origin {origin} remains active fog",
                    f"{record.source}:{record.line}",
                )
            )
        issued_fog_ids.add(origin)

    dependencies: list[tuple[str, str]] = []
    for field_name in ("Depends on", "Related to"):
        for reference in _references(record.fields.get(field_name)):
            if not QUESTION_ID.fullmatch(reference):
                findings.append(
                    PlanningRecordFinding(
                        "ERROR",
                        f"{record.identifier} has malformed {field_name} "
                        f"reference {reference}",
                        f"{record.source}:{record.line}",
                    )
                )
            elif reference == record.identifier:
                findings.append(
                    PlanningRecordFinding(
                        "ERROR",
                        f"{record.identifier} cannot reference itself",
                        f"{record.source}:{record.line}",
                    )
                )
            elif reference not in questions:
                findings.append(
                    PlanningRecordFinding(
                        "ERROR",
                        f"{record.identifier} references missing question {reference}",
                        f"{record.source}:{record.line}",
                    )
                )
            elif field_name == "Depends on":
                dependencies.append((reference, record.identifier))
    return dependencies


def _validate_dependency_cycles(
    identifiers: set[str],
    dependencies: list[tuple[str, str]],
    findings: list[PlanningRecordFinding],
) -> None:
    adjacency = {identifier: [] for identifier in identifiers}
    for source, target in dependencies:
        if source in adjacency and target in adjacency:
            adjacency[source].append(target)

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(identifier: str, trail: list[str]) -> None:
        if identifier in visiting:
            start = trail.index(identifier)
            findings.append(
                PlanningRecordFinding(
                    "ERROR",
                    "planning dependency cycle detected: "
                    + " -> ".join(trail[start:]),
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


def _validate_counters(
    text: str,
    map_ids: set[str],
    question_ids: set[str],
    fog_ids: set[str],
    findings: list[PlanningRecordFinding],
) -> None:
    counter_entries = COUNTER.findall(text)
    counters = {kind: identifier for kind, identifier in counter_entries}
    expected_prefix = {"map": "MAP", "question": "QUESTION", "fog": "FOG"}
    identifiers = {"map": map_ids, "question": question_ids, "fog": fog_ids}
    for kind, prefix in expected_prefix.items():
        if sum(entry_kind == kind for entry_kind, _ in counter_entries) > 1:
            findings.append(
                PlanningRecordFinding(
                    "ERROR", f"duplicate Next {kind} counter in {ACTIVE_PATH}"
                )
            )
        value = counters.get(kind)
        if not value:
            findings.append(
                PlanningRecordFinding(
                    "ERROR", f"missing Next {kind} counter in {ACTIVE_PATH}"
                )
            )
            continue
        pattern = {"map": MAP_ID, "question": QUESTION_ID, "fog": FOG_ID}[kind]
        match = pattern.fullmatch(value)
        if not match or not value.startswith(prefix + "-"):
            findings.append(
                PlanningRecordFinding("ERROR", f"malformed Next {kind} counter {value}")
            )
            continue
        issued = [int(identifier.rsplit("-", 1)[1]) for identifier in identifiers[kind]]
        if issued and int(match.group(1)) <= max(issued):
            findings.append(
                PlanningRecordFinding(
                    "ERROR",
                    f"Next {kind} counter {value} would reuse an issued identifier",
                )
            )


def _references(value: str | None) -> tuple[str, ...]:
    if not value or _plain(value).lower() in {"none", "not applicable"}:
        return ()
    return tuple(_plain(part) for part in value.split(",") if _plain(part))


def _plain(value: str) -> str:
    stripped = value.strip()
    if len(stripped) >= 2 and stripped[0] == stripped[-1] == "`":
        return stripped[1:-1]
    return stripped
