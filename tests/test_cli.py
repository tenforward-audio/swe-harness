import io
import json
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import patch

from swe_harness.cli import main
from swe_harness.template import default_answers


class CliTest(TestCase):
    def test_init_and_doctor_commands(self) -> None:
        with TemporaryDirectory() as directory:
            target = Path(directory)

            init_code, init_output = self._run(
                ["init", str(target), "--defaults", "--require-complete"]
            )
            doctor_code, doctor_output = self._run(
                ["doctor", str(target), "--require-manifest"]
            )

            self.assertEqual(0, init_code, init_output)
            self.assertIn("APPLIED", init_output)
            self.assertEqual(0, doctor_code, doctor_output)
            self.assertIn("Harness check passed", doctor_output)

    def test_interactive_prompt_fills_only_missing_answer(self) -> None:
        with TemporaryDirectory() as directory:
            target = Path(directory)
            answers = default_answers(target)
            answers.pop("PROJECT_NAME")
            answers_path = target / "answers.json"
            answers_path.write_text(json.dumps(answers), encoding="utf-8")

            with patch("sys.stdin.isatty", return_value=True), patch(
                "builtins.input", return_value="Prompted Project"
            ) as prompt:
                code, output = self._run(
                    [
                        "init",
                        str(target),
                        "--answers",
                        str(answers_path),
                        "--dry-run",
                        "--require-complete",
                    ]
                )

            self.assertEqual(0, code, output)
            prompt.assert_called_once()
            self.assertIn("DRY_RUN", output)

    def test_noninteractive_incomplete_answers_fail_when_required(self) -> None:
        with TemporaryDirectory() as directory:
            code, output = self._run(
                [
                    "init",
                    directory,
                    "--non-interactive",
                    "--require-complete",
                    "--dry-run",
                ]
            )

            self.assertEqual(2, code)
            self.assertIn("UNRESOLVED", output)

    @staticmethod
    def _run(arguments: list[str]) -> tuple[int, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            code = main(arguments)
        return code, stdout.getvalue() + stderr.getvalue()
