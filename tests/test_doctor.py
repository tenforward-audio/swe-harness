from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from swe_harness.doctor import inspect_harness
from swe_harness.install import apply_plan, plan_init
from swe_harness.template import TemplateBundle, default_answers, default_template_root


class DoctorTest(TestCase):
    def test_installed_harness_passes(self) -> None:
        with TemporaryDirectory() as directory:
            target = Path(directory)
            bundle = TemplateBundle(default_template_root())
            apply_plan(plan_init(bundle, target, default_answers(target)))

            findings = inspect_harness(target, bundle, require_manifest=True)

            self.assertFalse(
                [finding for finding in findings if finding.severity == "ERROR"]
            )

    def test_reports_duplicate_tracking_identifier(self) -> None:
        with TemporaryDirectory() as directory:
            target = Path(directory)
            bundle = TemplateBundle(default_template_root())
            apply_plan(plan_init(bundle, target, default_answers(target)))
            (target / ".agents/ISSUES.md").write_text(
                "### ISSUE-001 — Queue item\n", encoding="utf-8"
            )
            (target / ".agents/workboard/PLANNING.md").write_text(
                "### ISSUE-001 — Copied card\n", encoding="utf-8"
            )

            findings = inspect_harness(target, bundle)

            self.assertTrue(
                any("appears in multiple sources" in finding.message for finding in findings)
            )

    def test_reports_broken_relative_link(self) -> None:
        with TemporaryDirectory() as directory:
            target = Path(directory)
            bundle = TemplateBundle(default_template_root())
            apply_plan(plan_init(bundle, target, default_answers(target)))
            (target / "README.md").write_text(
                "[missing](nowhere.md)\n", encoding="utf-8"
            )

            findings = inspect_harness(target, bundle)

            self.assertTrue(
                any("broken link in README.md" in finding.message for finding in findings)
            )

    def test_reports_more_than_one_in_progress_card(self) -> None:
        with TemporaryDirectory() as directory:
            target = Path(directory)
            bundle = TemplateBundle(default_template_root())
            apply_plan(plan_init(bundle, target, default_answers(target)))
            (target / ".agents/workboard/IN_PROGRESS.md").write_text(
                "### ISSUE-001 — One\n\n### FEATURE-001 — Two\n",
                encoding="utf-8",
            )

            findings = inspect_harness(target, bundle)

            self.assertTrue(
                any("WIP limit exceeded" in finding.message for finding in findings)
            )
