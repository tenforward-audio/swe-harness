"""Load and render the canonical harness template."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping


PLACEHOLDER_PATTERN = re.compile(r"\{\{([A-Z][A-Z0-9_]*)\}\}")
REVISION_PATTERN = re.compile(
    r"^- Template revision: `([^`]+)`$", re.MULTILINE
)
ADR_PLACEHOLDERS = {
    "CONSEQUENCES",
    "DECISION",
    "DECISION_CONTEXT",
    "DECISION_TITLE",
    "OPTION_ONE",
    "OPTION_TWO",
    "REVERSAL_CONDITIONS",
}


@dataclass(frozen=True)
class PromptSpec:
    key: str
    label: str
    default: str


def prompt_specs(target: Path) -> tuple[PromptSpec, ...]:
    project_name = target.resolve().name.replace("_", " ").replace("-", " ").title()
    return (
        PromptSpec("PROJECT_NAME", "Project name", project_name),
        PromptSpec(
            "PROJECT_OUTCOME",
            "Project outcome",
            "Deliver the project's documented user and maintainer outcomes.",
        ),
        PromptSpec("PRIMARY_USERS", "Primary users", "Project users and maintainers."),
        PromptSpec(
            "SUPPORTED_PLATFORMS",
            "Supported platforms",
            "Platforms explicitly supported by the project.",
        ),
        PromptSpec(
            "PROJECT_SAFETY_RULES",
            "Project-specific safety rule",
            "Follow the project's documented safety and data boundaries.",
        ),
        PromptSpec("PROJECT_STACK", "Project stack", "Not yet specified."),
        PromptSpec(
            "PROJECT_ARCHITECTURE", "Project architecture", "Not yet specified."
        ),
        PromptSpec(
            "COMPATIBILITY_CONSTRAINTS",
            "Compatibility constraints",
            "No project-specific constraints are currently declared.",
        ),
        PromptSpec("SETUP_COMMAND", "Setup command", "not configured"),
        PromptSpec(
            "AFFECTED_LAYER_CHECK_COMMANDS",
            "Affected-layer check command",
            "not configured",
        ),
        PromptSpec("FORMAT_CHECK_COMMAND", "Format-check command", "not configured"),
        PromptSpec("LINT_COMMAND", "Lint command", "not configured"),
        PromptSpec("TYPECHECK_COMMAND", "Type-check command", "not configured"),
        PromptSpec("TEST_COMMAND", "Test command", "not configured"),
        PromptSpec("BUILD_COMMAND", "Build command", "not configured"),
        PromptSpec("CHECK_COMMAND", "Cross-stack check command", "not configured"),
        PromptSpec("FULL_CHECK_COMMAND", "Full gate command", "not configured"),
        PromptSpec("PROJECT_LICENSE", "Project licence", "not yet selected"),
        PromptSpec(
            "SUPPORTED_VERSIONS",
            "Supported versions",
            "Only the current development version is supported.",
        ),
        PromptSpec(
            "SECURITY_CONTACT",
            "Private security contact",
            "the project owner through a private channel",
        ),
        PromptSpec("LANGUAGE_VARIANT", "Prose language variant", "British English"),
        PromptSpec("VERSION_SOURCE", "Authoritative version source", "not configured"),
        PromptSpec("RELEASE_COMMAND", "Release command", "not configured"),
    )


def default_answers(target: Path) -> dict[str, str]:
    return {spec.key: spec.default for spec in prompt_specs(target)}


def read_answers(path: Path) -> dict[str, str]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError(f"cannot read answers from {path}: {error}") from error
    if not isinstance(value, dict):
        raise ValueError(f"answers in {path} must be a JSON object")
    answers: dict[str, str] = {}
    for key, answer in value.items():
        if not isinstance(key, str) or not isinstance(answer, str):
            raise ValueError(f"answer keys and values in {path} must be strings")
        answers[key] = answer
    return answers


def parse_assignments(assignments: list[str]) -> dict[str, str]:
    answers: dict[str, str] = {}
    for assignment in assignments:
        if "=" not in assignment:
            raise ValueError(f"answer must use KEY=VALUE: {assignment}")
        key, value = assignment.split("=", 1)
        if not key or not value:
            raise ValueError(f"answer must use non-empty KEY=VALUE: {assignment}")
        answers[key] = value
    return answers


def default_template_root() -> Path:
    package_path = Path(__file__).resolve()
    candidates = (
        package_path.parents[1] / "templates" / "default",
        package_path.parents[2] / "templates" / "default",
    )
    for candidate in candidates:
        if candidate.is_dir():
            return candidate
    raise RuntimeError("cannot locate the bundled default harness template")


class TemplateBundle:
    def __init__(self, root: Path) -> None:
        if root.is_symlink():
            raise ValueError(f"template must not be a symbolic link: {root}")
        self.root = root.resolve()
        self._reject_symlinks()
        marker = self.root / ".agents" / "HARNESS.md"
        if not marker.is_file():
            raise ValueError(f"template marker is missing: {marker}")
        marker_text = marker.read_text(encoding="utf-8")
        revision_match = REVISION_PATTERN.search(marker_text)
        if revision_match is None:
            raise ValueError(f"template revision is missing or malformed: {marker}")
        self.revision = revision_match.group(1)

    def files(self) -> tuple[Path, ...]:
        self._reject_symlinks()
        return tuple(
            sorted(
                (path for path in self.root.rglob("*") if path.is_file()),
                key=lambda path: path.relative_to(self.root).as_posix(),
            )
        )

    def _reject_symlinks(self) -> None:
        symlinks = [path for path in self.root.rglob("*") if path.is_symlink()]
        if symlinks:
            raise ValueError(f"template must not contain symbolic links: {symlinks[0]}")

    def placeholders(self) -> set[str]:
        found: set[str] = set()
        for path in self.files():
            found.update(PLACEHOLDER_PATTERN.findall(path.read_text(encoding="utf-8")))
        return found

    def active_placeholders(self) -> set[str]:
        return self.placeholders() - ADR_PLACEHOLDERS

    def validate_answers(self, answers: Mapping[str, str]) -> None:
        unknown = sorted(set(answers) - self.active_placeholders())
        if unknown:
            raise ValueError("unknown template answer keys: " + ", ".join(unknown))

    def render(self, answers: Mapping[str, str]) -> dict[Path, bytes]:
        self.validate_answers(answers)
        rendered: dict[Path, bytes] = {}
        for source in self.files():
            relative = source.relative_to(self.root)
            text = source.read_text(encoding="utf-8")
            for key, value in answers.items():
                text = text.replace("{{" + key + "}}", value)
            rendered[relative] = text.encode("utf-8")
        return rendered


def unresolved_active_placeholders(rendered: Mapping[Path, bytes]) -> set[str]:
    found: set[str] = set()
    for relative, content in rendered.items():
        if relative == Path(".agents/decisions/0000-template.md"):
            continue
        found.update(PLACEHOLDER_PATTERN.findall(content.decode("utf-8")))
    return found
