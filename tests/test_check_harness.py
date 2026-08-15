import io
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from scripts.check_harness import compatibility_main
from swe_harness.install import apply_plan, plan_init
from swe_harness.template import TemplateBundle, default_answers, default_template_root


class CompatibilityWrapperTest(TestCase):
    def test_root_option_validates_selected_repository(self) -> None:
        with TemporaryDirectory() as directory:
            target = Path(directory)
            bundle = TemplateBundle(default_template_root())
            apply_plan(plan_init(bundle, target, default_answers(target)))
            stdout = io.StringIO()
            stderr = io.StringIO()

            with redirect_stdout(stdout), redirect_stderr(stderr):
                code = compatibility_main(["--root", str(target)])

            self.assertEqual(0, code, stdout.getvalue() + stderr.getvalue())
            self.assertIn("Harness check passed", stdout.getvalue())
