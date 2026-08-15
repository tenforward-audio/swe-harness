from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from scripts.check_harness import HarnessValidator


class HarnessValidatorTest(TestCase):
    def test_reports_duplicate_tracking_identifier(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            self._write_required_files(root)
            self._write(root, ".agents/ISSUES.md", "### ISSUE-001 — Queue item\n")
            self._write(
                root,
                ".agents/workboard/PLANNING.md",
                "### ISSUE-001 — Copied card\n",
            )

            errors = HarnessValidator(root).validate()

            self.assertTrue(any("appears in multiple sources" in error for error in errors))

    def test_reports_broken_relative_link(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            self._write_required_files(root)
            self._write(root, "README.md", "[missing](nowhere.md)\n")

            errors = HarnessValidator(root).validate()

            self.assertIn("broken link in README.md: nowhere.md", errors)

    def test_allows_placeholders_only_in_adr_template(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            self._write_required_files(root)
            self._write(root, "AGENTS.md", "{{PROJECT_NAME}}\n")
            self._write(
                root,
                ".agents/decisions/0000-template.md",
                "{{DECISION_TITLE}}\n",
            )

            errors = HarnessValidator(root).validate()

            placeholder_errors = [error for error in errors if "placeholder" in error]
            self.assertEqual(1, len(placeholder_errors))
            self.assertIn("AGENTS.md:1", placeholder_errors[0])

    def test_reports_more_than_one_in_progress_card(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            self._write_required_files(root)
            self._write(
                root,
                ".agents/workboard/IN_PROGRESS.md",
                "### ISSUE-001 — One\n\n### FEATURE-001 — Two\n",
            )

            errors = HarnessValidator(root).validate()

            self.assertIn("WIP limit exceeded: found 2 in-progress cards", errors)

    @staticmethod
    def _write(root: Path, relative: str, content: str = "") -> None:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    @classmethod
    def _write_required_files(cls, root: Path) -> None:
        for relative in (
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
        ):
            cls._write(root, relative)
