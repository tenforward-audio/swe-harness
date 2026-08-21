import os
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from swe_harness.install import apply_plan, plan_init
from swe_harness.template import TemplateBundle, default_answers, default_template_root
from swe_harness.work_cards import inspect_work_cards


class WorkCardValidationTest(TestCase):
    def test_accepts_card_relationships_and_parallel_lanes(self) -> None:
        with TemporaryDirectory() as directory:
            target = self._installed(Path(directory))
            (target / ".agents/ISSUES.md").write_text(
                """# Issue intake

### ISSUE-001 — Parser contract

- Reported: 2026-08-21
- Type: task
- Report: Parse canonical work.
- Expected outcome: One validated model.
- Acceptance notes: Not stated.
- Track: Core harness
- Depends on: None
- Related to: FEATURE-001
""",
                encoding="utf-8",
            )
            (target / ".agents/workboard/PLANNING.md").write_text(
                self._selected_card(
                    "FEATURE-001", "Structured work", depends_on="ISSUE-001"
                ),
                encoding="utf-8",
            )
            (target / ".agents/workboard/IN_PROGRESS.md").write_text(
                self._selected_card(
                    "ISSUE-002",
                    "Parallel implementation",
                    extra="""
- Common base: `abc123`
- Lanes:
  - Lane: parser
    - Branch: `codex/issue-002-parser`
    - Worktree: active
    - Depends on: None
    - Owns: Python card validation
  - Lane: docs
    - Branch: `codex/issue-002-docs`
    - Worktree: planned
    - Depends on: parser
    - Owns: Workflow documentation
""",
                ),
                encoding="utf-8",
            )

            findings = inspect_work_cards(target)

            self.assertFalse(
                [finding for finding in findings if finding.severity == "ERROR"]
            )

    def test_reports_missing_malformed_and_cyclic_references(self) -> None:
        with TemporaryDirectory() as directory:
            target = self._installed(Path(directory))
            (target / ".agents/workboard/PLANNING.md").write_text(
                self._selected_card(
                    "ISSUE-001", "First", depends_on="FEATURE-001"
                )
                + "\n"
                + self._selected_card(
                    "FEATURE-001", "Second", depends_on="ISSUE-001"
                )
                + "\n"
                + self._selected_card(
                    "ISSUE-002", "Third", related_to="ISSUE-999"
                )
                + "\n"
                + self._selected_card(
                    "FEATURE-002", "Fourth", depends_on="feature two"
                ),
                encoding="utf-8",
            )

            messages = [finding.message for finding in inspect_work_cards(target)]

            self.assertTrue(any("dependency cycle detected" in item for item in messages))
            self.assertIn("ISSUE-002 references missing live card ISSUE-999", messages)
            self.assertIn(
                "FEATURE-002 has malformed Depends on reference feature two", messages
            )

    def test_reports_invalid_lane_metadata_and_missing_required_fields(self) -> None:
        with TemporaryDirectory() as directory:
            target = self._installed(Path(directory))
            (target / ".agents/workboard/IN_PROGRESS.md").write_text(
                self._selected_card(
                    "ISSUE-001",
                    "Invalid lanes",
                    extra="""
- Lanes:
  - Lane: parser
    - Branch: `codex/issue-001-parser`
    - Worktree: unknown
    - Depends on: missing
    - Owns: Parser
  - Lane: parser
    - Branch: `codex/issue-001-parser-copy`
    - Worktree: planned
    - Depends on: None
""",
                ),
                encoding="utf-8",
            )

            messages = [finding.message for finding in inspect_work_cards(target)]

            self.assertIn(
                "ISSUE-001 with Lanes is missing required field Common base", messages
            )
            self.assertIn("ISSUE-001 contains duplicate lane parser", messages)
            self.assertIn(
                "ISSUE-001 lane parser has unsupported Worktree state unknown", messages
            )
            self.assertIn(
                "ISSUE-001 lane parser references missing lane missing", messages
            )
            self.assertIn(
                "ISSUE-001 lane parser is missing required field Owns", messages
            )

    def test_rejects_symbolic_linked_tracking_sources(self) -> None:
        with TemporaryDirectory() as directory:
            target = self._installed(Path(directory))
            issues = target / ".agents/ISSUES.md"
            issues.unlink()
            os.symlink(target / ".agents/FEATURES.md", issues)

            messages = [finding.message for finding in inspect_work_cards(target)]

            self.assertIn(
                "tracking source must not be a symbolic link: .agents/ISSUES.md",
                messages,
            )

    @staticmethod
    def _installed(target: Path) -> Path:
        bundle = TemplateBundle(default_template_root())
        apply_plan(plan_init(bundle, target, default_answers(target)))
        return target

    @staticmethod
    def _selected_card(
        identifier: str,
        title: str,
        *,
        depends_on: str = "None",
        related_to: str = "None",
        extra: str = "",
    ) -> str:
        return f"""### {identifier} — {title}

- Source: User request
- Outcome: A visible result
- Scope: Focused scope
- Constraints: None
- Exit checks: Tests pass
- Manual acceptance: Not applicable
- Track: Core harness
- Depends on: {depends_on}
- Related to: {related_to}
- Owner: Coordinating checkout
- Capabilities: None
- Next action: Implement
{extra}"""
