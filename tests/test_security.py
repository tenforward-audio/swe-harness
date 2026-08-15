import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from swe_harness.install import MANIFEST_PATH, read_manifest, resolve_target
from swe_harness.template import TemplateBundle


class SecurityBoundaryTest(TestCase):
    def test_rejects_manifest_path_traversal(self) -> None:
        with TemporaryDirectory() as directory:
            target = Path(directory)
            manifest = target / MANIFEST_PATH
            manifest.parent.mkdir(parents=True)
            manifest.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "template_revision": "1.0.0",
                        "managed_files": {
                            "../../outside": hashlib.sha256(b"value").hexdigest()
                        },
                    }
                ),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "invalid managed files"):
                read_manifest(target)

    def test_rejects_template_file_symlink(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            marker = root / ".agents/HARNESS.md"
            marker.parent.mkdir(parents=True)
            marker.write_text("- Template revision: `1.0.0`\n", encoding="utf-8")
            outside = root / "outside"
            outside.write_text("outside\n", encoding="utf-8")
            (root / "linked").symlink_to(outside)

            with self.assertRaisesRegex(ValueError, "symbolic links"):
                TemplateBundle(root)

    def test_rejects_template_directory_symlink(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            marker = root / ".agents/HARNESS.md"
            marker.parent.mkdir(parents=True)
            marker.write_text("- Template revision: `1.0.0`\n", encoding="utf-8")
            outside = root / "outside"
            outside.mkdir()
            (root / "linked-directory").symlink_to(outside, target_is_directory=True)

            with self.assertRaisesRegex(ValueError, "symbolic links"):
                TemplateBundle(root)

    def test_rejects_home_as_install_target(self) -> None:
        with self.assertRaisesRegex(ValueError, "home directory"):
            resolve_target(Path.home())
