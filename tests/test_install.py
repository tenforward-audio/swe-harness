from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import patch

from swe_harness.install import Status, apply_plan, plan_init, plan_upgrade
from swe_harness.template import TemplateBundle, default_answers, default_template_root


class InstallTest(TestCase):
    def test_default_template_installs_concise_test_output_guidance(self) -> None:
        with TemporaryDirectory() as directory:
            target = Path(directory)
            bundle = TemplateBundle(default_template_root())
            apply_plan(plan_init(bundle, target, default_answers(target)))

            style_guide = (target / ".agents/STYLE_GUIDE.md").read_text(
                encoding="utf-8"
            )

            self.assertIn("Keep expected-success paths silent", style_guide)
            self.assertIn("compact aggregate pass summary", style_guide)
            self.assertIn("diagnose failures", style_guide)

    def test_default_template_installs_and_routes_specialised_workflow_skills(
        self,
    ) -> None:
        with TemporaryDirectory() as directory:
            target = Path(directory)
            bundle = TemplateBundle(default_template_root())
            apply_plan(plan_init(bundle, target, default_answers(target)))

            expected_skills = (
                "clean-up-worktree",
                "coordinate-parallel-work",
                "deliver-project-work",
                "integrate-reviewed-change",
                "review-project-change",
            )
            agents = (target / "AGENTS.md").read_text(encoding="utf-8")
            for name in expected_skills:
                relative = Path(f".agents/skills/{name}/SKILL.md")
                skill = (target / relative).read_text(encoding="utf-8")
                self.assertIn(f"name: {name}", skill)
                self.assertIn(relative.as_posix(), agents)

            manage = (
                target / ".agents/skills/manage-project-work/SKILL.md"
            ).read_text(encoding="utf-8")
            self.assertIn("List open tickets", manage)
            self.assertIn("items for review", manage)
            self.assertIn("open tickets” as every unclosed `ISSUE-*`", manage)
            self.assertIn("Treat “open work” as both issue and", manage)

            deliver = (
                target / ".agents/skills/deliver-project-work/SKILL.md"
            ).read_text(encoding="utf-8")
            workflow = (target / ".agents/WORKFLOW.md").read_text(encoding="utf-8")
            self.assertIn("Ask for explicit confirmation", deliver)
            self.assertIn("Finish at Reviewing", deliver)
            self.assertIn("Do not turn a second tracked identifier", deliver)
            self.assertIn("candidate branch must remain pinned", deliver)
            self.assertIn(
                "Never create that checkpoint on the candidate branch", manage
            )
            self.assertIn("separate checkpoint on the canonical", workflow)
            self.assertIn("do not combine\nmultiple tracked identifiers", workflow)

            cleanup = (
                target / ".agents/skills/clean-up-worktree/SKILL.md"
            ).read_text(encoding="utf-8")
            integration = (
                target / ".agents/skills/integrate-reviewed-change/SKILL.md"
            ).read_text(encoding="utf-8")
            research = (target / ".agents/RESEARCH.md").read_text(encoding="utf-8")
            self.assertIn("remote branch deletion", cleanup)
            self.assertIn("independent durable reference", cleanup)
            self.assertIn("clean-up-worktree", integration)
            self.assertIn("knowledge archive", research)

    def test_default_template_installs_declared_skill_execution_modes(
        self,
    ) -> None:
        with TemporaryDirectory() as directory:
            target = Path(directory)
            bundle = TemplateBundle(default_template_root())
            apply_plan(plan_init(bundle, target, default_answers(target)))

            expected_modes = {
                "capture-project-intake": "inline",
                "clean-up-worktree": "inline",
                "coordinate-parallel-work": "orchestrate-explicit",
                "deliver-project-work": "inline",
                "develop-project": "inline",
                "integrate-reviewed-change": "inline",
                "investigate-project": "delegate-readonly",
                "manage-project-work": "inline",
                "release-project": "inline",
                "review-project-change": "delegate-readonly",
            }
            for name, mode in expected_modes.items():
                skill = (
                    target / f".agents/skills/{name}/SKILL.md"
                ).read_text(encoding="utf-8")
                self.assertIn("## Execution mode", skill)
                self.assertIn(f"`{mode}`", skill)

            agents = (target / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("Use one read-only subagent", agents)
            self.assertIn("dispatches multiple sibling read-only subagents", agents)
            self.assertIn("must not dispatch another subagent", agents)
            self.assertIn("returns that evidence and a proposed", agents)
            self.assertIn("continue inline and disclose", agents)
            for name in ("investigate-project", "review-project-change"):
                skill = (
                    target / f".agents/skills/{name}/SKILL.md"
                ).read_text(encoding="utf-8")
                self.assertIn("worker already delegated", skill)
                self.assertIn("must not dispatch another subagent", skill)

    def test_readme_examples_match_workflow_vocabulary_and_states(
        self,
    ) -> None:
        readme = (Path(__file__).resolve().parents[1] / "README.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("Show me the open tickets", readme)
        self.assertIn("Lists open issues across intake", readme)
        self.assertIn("Show me the open work", readme)
        self.assertIn("open issues and feature ideas", readme)
        self.assertIn("FEATURE-001 with API and UI lanes in parallel", readme)
        self.assertNotIn("FEATURE-001 and FEATURE-002 in parallel", readme)
        self.assertIn("Accepts an item from Reviewing", readme)
        self.assertIn("Codex stops there until you accept", readme)

    def test_fresh_install_is_complete_and_idempotent(self) -> None:
        with TemporaryDirectory() as directory:
            target = Path(directory)
            bundle = TemplateBundle(default_template_root())
            answers = default_answers(target)

            first_plan = plan_init(bundle, target, answers)
            self.assertFalse(first_plan.blockers)
            apply_plan(first_plan)

            second_plan = plan_init(bundle, target, answers)
            self.assertFalse(second_plan.changes)
            self.assertTrue(
                all(entry.status == Status.UNCHANGED for entry in second_plan.entries)
            )
            self.assertTrue((target / ".agents/HARNESS.json").is_file())

    def test_conflict_blocks_every_write(self) -> None:
        with TemporaryDirectory() as directory:
            target = Path(directory)
            existing = target / "AGENTS.md"
            existing.write_text("project-owned\n", encoding="utf-8")
            bundle = TemplateBundle(default_template_root())

            plan = plan_init(bundle, target, default_answers(target))

            self.assertTrue(
                any(entry.status == Status.CONFLICT for entry in plan.entries)
            )
            with self.assertRaisesRegex(ValueError, "change plan is blocked"):
                apply_plan(plan)
            self.assertEqual("project-owned\n", existing.read_text(encoding="utf-8"))
            self.assertFalse((target / "CHANGELOG.md").exists())

    def test_operational_failure_rolls_back_created_files(self) -> None:
        with TemporaryDirectory() as directory:
            target = Path(directory)
            bundle = TemplateBundle(default_template_root())
            plan = plan_init(bundle, target, default_answers(target))
            real_create = __import__(
                "swe_harness.install", fromlist=["_create_file"]
            )._create_file
            calls = 0

            def fail_after_first(destination: Path, content: bytes) -> None:
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise OSError("simulated write failure")
                real_create(destination, content)

            with patch("swe_harness.install._create_file", side_effect=fail_after_first):
                with self.assertRaisesRegex(OSError, "simulated write failure"):
                    apply_plan(plan)

            self.assertFalse((target / ".agents/CONTRIBUTING.md").exists())

    def test_upgrade_replaces_only_unchanged_installed_files(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target"
            target.mkdir()
            first_template = self._template(root / "one", "1.0.0", "first\n")
            second_template = self._template(root / "two", "1.1.0", "second\n")
            apply_plan(plan_init(first_template, target, {}))

            plan = plan_upgrade(second_template, target, {})

            self.assertFalse(plan.blockers)
            self.assertEqual(
                Status.UPDATE,
                next(entry for entry in plan.entries if entry.relative == Path("AGENTS.md")).status,
            )
            apply_plan(plan)
            self.assertEqual("second\n", (target / "AGENTS.md").read_text())

    def test_upgrade_stops_for_project_owned_modification(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target"
            target.mkdir()
            first_template = self._template(root / "one", "1.0.0", "first\n")
            second_template = self._template(root / "two", "1.1.0", "second\n")
            apply_plan(plan_init(first_template, target, {}))
            (target / "AGENTS.md").write_text("custom\n", encoding="utf-8")

            plan = plan_upgrade(second_template, target, {})

            entry = next(
                entry for entry in plan.entries if entry.relative == Path("AGENTS.md")
            )
            self.assertEqual(Status.REVIEW, entry.status)
            with self.assertRaisesRegex(ValueError, "change plan is blocked"):
                apply_plan(plan)
            self.assertEqual("custom\n", (target / "AGENTS.md").read_text())

    def test_unchanged_upgrade_is_idempotent(self) -> None:
        with TemporaryDirectory() as directory:
            target = Path(directory)
            bundle = TemplateBundle(default_template_root())
            answers = default_answers(target)
            apply_plan(plan_init(bundle, target, answers))

            plan = plan_upgrade(bundle, target, answers)

            self.assertFalse(plan.blockers)
            self.assertFalse(plan.changes)
            self.assertTrue(
                all(entry.status == Status.UNCHANGED for entry in plan.entries)
            )

    def test_upgrade_stops_when_file_changes_after_planning(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target"
            target.mkdir()
            first_template = self._template(root / "one", "1.0.0", "first\n")
            second_template = self._template(root / "two", "1.1.0", "second\n")
            apply_plan(plan_init(first_template, target, {}))
            original_marker = (target / ".agents/HARNESS.md").read_text()
            plan = plan_upgrade(second_template, target, {})
            (target / "AGENTS.md").write_text("concurrent edit\n", encoding="utf-8")

            with self.assertRaisesRegex(RuntimeError, "changed after planning"):
                apply_plan(plan)

            self.assertEqual(
                "concurrent edit\n", (target / "AGENTS.md").read_text()
            )
            self.assertEqual(
                original_marker,
                (target / ".agents/HARNESS.md").read_text(),
            )

    @staticmethod
    def _template(root: Path, revision: str, agents_content: str) -> TemplateBundle:
        marker = root / ".agents/HARNESS.md"
        marker.parent.mkdir(parents=True)
        marker.write_text(
            "# Harness state\n\n" f"- Template revision: `{revision}`\n",
            encoding="utf-8",
        )
        (root / "AGENTS.md").write_text(agents_content, encoding="utf-8")
        return TemplateBundle(root)
