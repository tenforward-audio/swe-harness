#!/usr/bin/env python3
"""Validate the repository-owned SWE harness contract."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote


REQUIRED_PATHS = (
    "AGENTS.md",
    "CHANGELOG.md",
    ".agents/README.md",
    ".agents/HARNESS.md",
    ".agents/WORKFLOW.md",
    ".agents/PLUGINS.md",
    ".agents/ISSUES.md",
    ".agents/FEATURES.md",
    ".agents/workboard/PLANNING.md",
    ".agents/workboard/IN_PROGRESS.md",
    ".agents/workboard/REVIEWING.md",
)

TRACKING_PATHS = (
    ".agents/ISSUES.md",
    ".agents/FEATURES.md",
    ".agents/workboard/PLANNING.md",
    ".agents/workboard/IN_PROGRESS.md",
    ".agents/workboard/REVIEWING.md",
)

PLACEHOLDER_PATTERN = re.compile(r"\{\{[A-Z][A-Z0-9_]*\}\}")
TRACKED_ID_PATTERN = re.compile(r"^###\s+((?:ISSUE|FEATURE)-\d{3,})\b", re.MULTILINE)
CARD_PATTERN = re.compile(r"^###\s+(?:ISSUE|FEATURE)-\d{3,}\b", re.MULTILINE)
MARKDOWN_LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
SKILL_NAME_PATTERN = re.compile(r"\A---\s*\n.*?^name:\s*([^\s]+)\s*$", re.MULTILINE | re.DOTALL)


class HarnessValidator:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.errors: list[str] = []

    def validate(self) -> list[str]:
        self._check_required_paths()
        self._check_placeholders()
        self._check_internal_links()
        self._check_tracking_ids()
        self._check_wip_limit()
        self._check_skill_names()
        return self.errors

    def _markdown_files(self) -> list[Path]:
        files = list(self.root.glob("*.md"))
        agents_dir = self.root / ".agents"
        if agents_dir.exists():
            files.extend(agents_dir.rglob("*.md"))
        return sorted(path for path in files if path.is_file())

    def _check_required_paths(self) -> None:
        for relative in REQUIRED_PATHS:
            if not (self.root / relative).is_file():
                self.errors.append(f"missing canonical source: {relative}")

    def _check_placeholders(self) -> None:
        allowed_template = self.root / ".agents/decisions/0000-template.md"
        for path in self._markdown_files():
            if path == allowed_template:
                continue
            for line_number, line in enumerate(path.read_text().splitlines(), start=1):
                match = PLACEHOLDER_PATTERN.search(line)
                if match:
                    relative = path.relative_to(self.root)
                    self.errors.append(
                        f"unresolved placeholder in {relative}:{line_number}: {match.group()}"
                    )

    def _check_internal_links(self) -> None:
        for path in self._markdown_files():
            text = path.read_text()
            for raw_target in MARKDOWN_LINK_PATTERN.findall(text):
                target = raw_target.strip().split()[0].strip("<>")
                if target.startswith(("#", "http://", "https://", "mailto:")):
                    continue
                file_target = unquote(target.split("#", 1)[0])
                if not file_target:
                    continue
                resolved = (path.parent / file_target).resolve()
                if not resolved.exists():
                    relative = path.relative_to(self.root)
                    self.errors.append(f"broken link in {relative}: {raw_target}")

    def _check_tracking_ids(self) -> None:
        locations: dict[str, list[str]] = {}
        for relative in TRACKING_PATHS:
            path = self.root / relative
            if not path.is_file():
                continue
            for identifier in TRACKED_ID_PATTERN.findall(path.read_text()):
                locations.setdefault(identifier, []).append(relative)
        for identifier, paths in sorted(locations.items()):
            if len(paths) > 1:
                self.errors.append(
                    f"tracked identifier {identifier} appears in multiple sources: "
                    + ", ".join(paths)
                )

    def _check_wip_limit(self) -> None:
        path = self.root / ".agents/workboard/IN_PROGRESS.md"
        if not path.is_file():
            return
        card_count = len(CARD_PATTERN.findall(path.read_text()))
        if card_count > 1:
            self.errors.append(f"WIP limit exceeded: found {card_count} in-progress cards")

    def _check_skill_names(self) -> None:
        skills_dir = self.root / ".agents/skills"
        if not skills_dir.exists():
            return
        names: dict[str, list[str]] = {}
        for path in sorted(skills_dir.glob("*/SKILL.md")):
            match = SKILL_NAME_PATTERN.search(path.read_text())
            relative = str(path.relative_to(self.root))
            if not match:
                self.errors.append(f"missing skill name frontmatter: {relative}")
                continue
            names.setdefault(match.group(1), []).append(relative)
        for name, paths in sorted(names.items()):
            if len(paths) > 1:
                self.errors.append(f"duplicate skill name {name}: " + ", ".join(paths))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root (defaults to the parent of this script directory)",
    )
    args = parser.parse_args()

    errors = HarnessValidator(args.root).validate()
    if errors:
        for error in errors:
            print(f"ERROR {error}")
        return 1

    print("Harness check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
