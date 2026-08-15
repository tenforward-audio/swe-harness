import json
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class PluginBuildTest(TestCase):
    def test_built_plugin_is_self_contained(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            plugin = root / "plugin"
            target = root / "target"
            target.mkdir()

            self._run(
                PROJECT_ROOT / "scripts/build_plugin.py",
                "--output",
                plugin,
            )
            self._run(
                plugin / "scripts/swe-harness.py",
                "init",
                target,
                "--defaults",
                "--non-interactive",
                "--require-complete",
            )
            self._run(
                plugin / "scripts/swe-harness.py",
                "doctor",
                target,
                "--require-manifest",
            )

            manifest = json.loads(
                (plugin / ".codex-plugin/plugin.json").read_text(encoding="utf-8")
            )
            self.assertEqual("swe-harness", manifest["name"])
            self.assertTrue((plugin / "lib/swe_harness/cli.py").is_file())
            self.assertTrue((plugin / "templates/default/AGENTS.md").is_file())

    def test_build_refuses_to_replace_output(self) -> None:
        with TemporaryDirectory() as directory:
            output = Path(directory) / "existing"
            output.mkdir()

            result = subprocess.run(
                [
                    sys.executable,
                    str(PROJECT_ROOT / "scripts/build_plugin.py"),
                    "--output",
                    str(output),
                ],
                cwd=PROJECT_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertNotEqual(0, result.returncode)
            self.assertIn("Refusing to replace existing output", result.stderr)

    def _run(self, script: Path, *arguments: object) -> None:
        result = subprocess.run(
            [sys.executable, str(script), *(str(value) for value in arguments)],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
