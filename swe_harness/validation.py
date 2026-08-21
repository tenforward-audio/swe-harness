"""Validate structural and lifecycle invariants in an installed harness."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote

from .install import MANIFEST_PATH, destination_safety_error, read_manifest, sha256
from .template import PLACEHOLDER_PATTERN, TemplateBundle


TRACKING_PATHS = (
    Path(".agents/ISSUES.md"),
    Path(".agents/FEATURES.md"),
    Path(".agents/workboard/PLANNING.md"),
    Path(".agents/workboard/IN_PROGRESS.md"),
    Path(".agents/workboard/REVIEWING.md"),
)
TRACKED_ID_PATTERN = re.compile(
    r"^###\s+((?:ISSUE|FEATURE)-\d{3,})\b", re.MULTILINE
)
CARD_PATTERN = re.compile(
    r"^###\s+(?:ISSUE|FEATURE)-\d{3,}\b", re.MULTILINE
)
MARKDOWN_LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
SKILL_NAME_PATTERN = re.compile(
    r"\A---\s*\n.*?^name:\s*([^\s]+)\s*$", re.MULTILINE | re.DOTALL
)
SKILL_EXECUTION_MODE_PATTERN = re.compile(
    r"^## Execution mode\s*$\n\s*`([^`\n]+)`\s*$", re.MULTILINE
)
SKILL_EXECUTION_MODES = frozenset(
    {"inline", "delegate-readonly", "orchestrate-explicit"}
)


@dataclass(frozen=True)
class Finding:
    severity: str
    message: str


def _markdown_files(root: Path) -> list[Path]:
    files = list(root.glob("*.md"))
    agents_dir = root / ".agents"
    if agents_dir.exists():
        files.extend(agents_dir.rglob("*.md"))
    return sorted(path for path in files if path.is_file())


def inspect_harness(
    root: Path, bundle: TemplateBundle, require_manifest: bool = False
) -> list[Finding]:
    resolved_root = root.resolve()
    findings: list[Finding] = []
    required = {path.relative_to(bundle.root) for path in bundle.files()}
    for relative in sorted(required, key=Path.as_posix):
        if not (resolved_root / relative).is_file():
            findings.append(Finding("ERROR", f"missing canonical source: {relative}"))

    allowed_template = resolved_root / ".agents/decisions/0000-template.md"
    for path in _markdown_files(resolved_root):
        if path == allowed_template:
            continue
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            match = PLACEHOLDER_PATTERN.search(line)
            if match:
                relative = path.relative_to(resolved_root)
                findings.append(
                    Finding(
                        "ERROR",
                        f"unresolved placeholder in {relative}:{line_number}: "
                        f"{{{{{match.group(1)}}}}}",
                    )
                )

    for path in _markdown_files(resolved_root):
        text = path.read_text(encoding="utf-8")
        for raw_target in MARKDOWN_LINK_PATTERN.findall(text):
            stripped = raw_target.strip()
            if stripped.startswith("<") and ">" in stripped:
                target = stripped[1 : stripped.index(">")]
            else:
                target = stripped.split()[0]
            if target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            file_target = unquote(target.split("#", 1)[0])
            if file_target and not (path.parent / file_target).resolve().exists():
                relative = path.relative_to(resolved_root)
                findings.append(
                    Finding("ERROR", f"broken link in {relative}: {raw_target}")
                )

    locations: dict[str, list[str]] = {}
    for relative in TRACKING_PATHS:
        path = resolved_root / relative
        if not path.is_file():
            continue
        for identifier in TRACKED_ID_PATTERN.findall(path.read_text(encoding="utf-8")):
            locations.setdefault(identifier, []).append(relative.as_posix())
    for identifier, paths in sorted(locations.items()):
        if len(paths) > 1:
            findings.append(
                Finding(
                    "ERROR",
                    f"tracked identifier {identifier} appears in multiple sources: "
                    + ", ".join(paths),
                )
            )

    in_progress = resolved_root / ".agents/workboard/IN_PROGRESS.md"
    if in_progress.is_file():
        card_count = len(CARD_PATTERN.findall(in_progress.read_text(encoding="utf-8")))
        if card_count > 1:
            findings.append(
                Finding("ERROR", f"WIP limit exceeded: found {card_count} in-progress cards")
            )

    names: dict[str, list[str]] = {}
    skills_dir = resolved_root / ".agents/skills"
    if skills_dir.exists():
        for path in sorted(skills_dir.glob("*/SKILL.md")):
            text = path.read_text(encoding="utf-8")
            match = SKILL_NAME_PATTERN.search(text)
            relative = path.relative_to(resolved_root).as_posix()
            if not match:
                findings.append(
                    Finding("ERROR", f"missing skill name frontmatter: {relative}")
                )
            else:
                names.setdefault(match.group(1), []).append(relative)

            if Path(relative) in required:
                execution_modes = SKILL_EXECUTION_MODE_PATTERN.findall(text)
                if not execution_modes:
                    findings.append(
                        Finding("ERROR", f"missing skill execution mode: {relative}")
                    )
                elif len(execution_modes) > 1:
                    findings.append(
                        Finding("ERROR", f"duplicate skill execution mode: {relative}")
                    )
                elif execution_modes[0] not in SKILL_EXECUTION_MODES:
                    findings.append(
                        Finding(
                            "ERROR",
                            f"unsupported skill execution mode "
                            f"{execution_modes[0]}: {relative}",
                        )
                    )
    for name, paths in sorted(names.items()):
        if len(paths) > 1:
            findings.append(
                Finding("ERROR", f"duplicate skill name {name}: " + ", ".join(paths))
            )

    manifest_path = resolved_root / MANIFEST_PATH
    if not manifest_path.exists():
        severity = "ERROR" if require_manifest else "NOTE"
        findings.append(Finding(severity, "installation manifest is not present"))
    else:
        try:
            manifest = read_manifest(resolved_root)
        except ValueError as error:
            findings.append(Finding("ERROR", str(error)))
        else:
            managed = manifest["managed_files"]
            assert isinstance(managed, dict)
            for relative_text, installed_checksum in sorted(managed.items()):
                relative = Path(relative_text)
                unsafe_reason = destination_safety_error(resolved_root, relative)
                if unsafe_reason:
                    findings.append(
                        Finding(
                            "ERROR",
                            f"managed path is unsafe: {relative_text}: {unsafe_reason}",
                        )
                    )
                    continue
                path = resolved_root / relative
                if not path.is_file():
                    continue
                if sha256(path.read_bytes()) != installed_checksum:
                    findings.append(
                        Finding(
                            "NOTE",
                            f"project-owned file changed since installation: {relative_text}",
                        )
                    )
    return findings
