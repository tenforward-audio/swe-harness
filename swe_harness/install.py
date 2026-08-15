"""Plan and apply safe harness installation and upgrades."""

from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Mapping

from .template import TemplateBundle


MANIFEST_PATH = Path(".agents/HARNESS.json")
MANIFEST_SCHEMA_VERSION = 1
CHECKSUM_PATTERN = re.compile(r"^[0-9a-f]{64}$")


class Status(str, Enum):
    CREATE = "CREATE"
    UNCHANGED = "UNCHANGED"
    CONFLICT = "CONFLICT"
    UPDATE = "UPDATE"
    REVIEW = "REVIEW"
    UNSAFE = "UNSAFE"


@dataclass(frozen=True)
class PlanEntry:
    relative: Path
    status: Status
    content: bytes | None
    reason: str = ""
    expected: bytes | None = None


@dataclass(frozen=True)
class ChangePlan:
    target: Path
    revision: str
    entries: tuple[PlanEntry, ...]
    mode: str

    @property
    def blockers(self) -> tuple[PlanEntry, ...]:
        blocking = {Status.CONFLICT, Status.REVIEW, Status.UNSAFE}
        return tuple(entry for entry in self.entries if entry.status in blocking)

    @property
    def changes(self) -> tuple[PlanEntry, ...]:
        changing = {Status.CREATE, Status.UPDATE}
        return tuple(entry for entry in self.entries if entry.status in changing)


def sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def destination_safety_error(target: Path, relative: Path) -> str | None:
    current = target
    for part in relative.parts[:-1]:
        current = current / part
        if current.is_symlink():
            return f"parent is a symbolic link: {current}"
        if current.exists() and not current.is_dir():
            return f"parent is not a directory: {current}"
    destination = target / relative
    if destination.is_symlink():
        return f"destination is a symbolic link: {destination}"
    return None


def resolve_target(raw_target: Path) -> Path:
    expanded = raw_target.expanduser()
    if expanded.is_symlink():
        raise ValueError("target directory must not be a symbolic link")
    if not expanded.exists() or not expanded.is_dir():
        raise ValueError("target must be an existing directory")
    resolved = expanded.resolve()
    filesystem_root = Path(resolved.anchor)
    if resolved in {filesystem_root, Path.home().resolve()}:
        raise ValueError("target must not be a filesystem root or home directory")
    return resolved


def _manifest_bytes(revision: str, rendered: Mapping[Path, bytes]) -> bytes:
    value = {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "template_revision": revision,
        "managed_files": {
            relative.as_posix(): sha256(content)
            for relative, content in sorted(
                rendered.items(), key=lambda item: item[0].as_posix()
            )
        },
    }
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def read_manifest(target: Path) -> dict[str, object]:
    path = target / MANIFEST_PATH
    unsafe_reason = destination_safety_error(target.resolve(), MANIFEST_PATH)
    if unsafe_reason:
        raise ValueError(f"installation manifest is unsafe: {unsafe_reason}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise ValueError(f"installation manifest is missing: {path}") from error
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError(f"installation manifest is unreadable: {path}: {error}") from error
    if not isinstance(value, dict):
        raise ValueError(f"installation manifest must be a JSON object: {path}")
    if value.get("schema_version") != MANIFEST_SCHEMA_VERSION:
        raise ValueError(f"unsupported installation manifest schema: {path}")
    managed = value.get("managed_files")
    if not isinstance(managed, dict) or not all(
        isinstance(key, str)
        and _safe_relative(Path(key))
        and isinstance(checksum, str)
        and CHECKSUM_PATTERN.fullmatch(checksum)
        for key, checksum in managed.items()
    ):
        raise ValueError(f"installation manifest has invalid managed files: {path}")
    return value


def _safe_relative(relative: Path) -> bool:
    return (
        not relative.is_absolute()
        and bool(relative.parts)
        and all(part not in {"", ".", ".."} for part in relative.parts)
    )


def plan_init(
    bundle: TemplateBundle, target: Path, answers: Mapping[str, str]
) -> ChangePlan:
    resolved_target = resolve_target(target)
    rendered = bundle.render(answers)
    entries: list[PlanEntry] = []
    for relative, content in rendered.items():
        unsafe_reason = destination_safety_error(resolved_target, relative)
        destination = resolved_target / relative
        if unsafe_reason:
            status = Status.UNSAFE
            reason = unsafe_reason
        elif not destination.exists():
            status = Status.CREATE
            reason = ""
        elif destination.is_file() and destination.read_bytes() == content:
            status = Status.UNCHANGED
            reason = ""
        else:
            status = Status.CONFLICT
            reason = "existing content differs"
        entries.append(PlanEntry(relative, status, content, reason))

    manifest_reason = destination_safety_error(resolved_target, MANIFEST_PATH)
    manifest_destination = resolved_target / MANIFEST_PATH
    manifest_content = _manifest_bytes(bundle.revision, rendered)
    if manifest_reason:
        entries.append(
            PlanEntry(MANIFEST_PATH, Status.UNSAFE, manifest_content, manifest_reason)
        )
    elif not manifest_destination.exists():
        entries.append(PlanEntry(MANIFEST_PATH, Status.CREATE, manifest_content))
    elif manifest_destination.is_file() and manifest_destination.read_bytes() == manifest_content:
        entries.append(PlanEntry(MANIFEST_PATH, Status.UNCHANGED, manifest_content))
    else:
        entries.append(
            PlanEntry(
                MANIFEST_PATH,
                Status.CONFLICT,
                manifest_content,
                "existing installation metadata differs",
            )
        )
    return ChangePlan(resolved_target, bundle.revision, tuple(entries), "init")


def plan_upgrade(
    bundle: TemplateBundle, target: Path, answers: Mapping[str, str]
) -> ChangePlan:
    resolved_target = resolve_target(target)
    manifest = read_manifest(resolved_target)
    managed = manifest["managed_files"]
    assert isinstance(managed, dict)
    rendered = bundle.render(answers)
    entries: list[PlanEntry] = []

    for relative, content in rendered.items():
        unsafe_reason = destination_safety_error(resolved_target, relative)
        destination = resolved_target / relative
        old_checksum = managed.get(relative.as_posix())
        if unsafe_reason:
            status = Status.UNSAFE
            reason = unsafe_reason
        elif not destination.exists():
            status = Status.CREATE
            reason = ""
        elif not destination.is_file():
            status = Status.REVIEW
            reason = "destination is not a regular file"
        else:
            current = destination.read_bytes()
            if current == content:
                status = Status.UNCHANGED
                reason = ""
            elif isinstance(old_checksum, str) and sha256(current) == old_checksum:
                status = Status.UPDATE
                reason = "unchanged since the previous installation"
            else:
                status = Status.REVIEW
                reason = "project-owned content differs from its recorded installation"
        expected = current if status == Status.UPDATE else None
        entries.append(PlanEntry(relative, status, content, reason, expected))

    rendered_names = {relative.as_posix() for relative in rendered}
    for old_relative in sorted(set(managed) - rendered_names):
        entries.append(
            PlanEntry(
                Path(old_relative),
                Status.REVIEW,
                None,
                "managed path was retired by the new template; it will not be deleted",
            )
        )

    manifest_reason = destination_safety_error(resolved_target, MANIFEST_PATH)
    manifest_content = _manifest_bytes(bundle.revision, rendered)
    manifest_destination = resolved_target / MANIFEST_PATH
    if manifest_reason:
        entries.append(
            PlanEntry(MANIFEST_PATH, Status.UNSAFE, None, manifest_reason)
        )
    elif manifest_destination.read_bytes() == manifest_content:
        entries.append(
            PlanEntry(MANIFEST_PATH, Status.UNCHANGED, manifest_content)
        )
    else:
        entries.append(
            PlanEntry(
                MANIFEST_PATH,
                Status.UPDATE,
                manifest_content,
                "record the verified installation state",
                manifest_destination.read_bytes(),
            )
        )
    return ChangePlan(resolved_target, bundle.revision, tuple(entries), "upgrade")


def _create_file(destination: Path, content: bytes) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        with destination.open("xb") as output:
            output.write(content)
    except FileExistsError as error:
        raise RuntimeError(f"destination appeared during installation: {destination}") from error


def _replace_file(destination: Path, content: bytes) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.", dir=destination.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as output:
            output.write(content)
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary, destination)
    finally:
        if temporary.exists():
            temporary.unlink()


def apply_plan(plan: ChangePlan) -> None:
    if plan.blockers:
        statuses = ", ".join(
            f"{entry.status.value} {entry.relative.as_posix()}"
            for entry in plan.blockers
        )
        raise ValueError(f"change plan is blocked: {statuses}")

    manifest_entry: PlanEntry | None = None
    created: list[tuple[Path, bytes]] = []
    replaced: list[tuple[Path, bytes, bytes]] = []
    try:
        for entry in plan.entries:
            if entry.relative == MANIFEST_PATH:
                manifest_entry = entry
                continue
            destination = plan.target / entry.relative
            unsafe_reason = destination_safety_error(plan.target, entry.relative)
            if unsafe_reason:
                raise RuntimeError(
                    f"destination became unsafe during installation: {unsafe_reason}"
                )
            if entry.status == Status.CREATE:
                assert entry.content is not None
                _create_file(destination, entry.content)
                created.append((destination, entry.content))
            elif entry.status == Status.UPDATE:
                assert entry.content is not None
                current = destination.read_bytes()
                if entry.expected is not None and current != entry.expected:
                    raise RuntimeError(
                        f"destination changed after planning: {entry.relative.as_posix()}"
                    )
                replaced.append((destination, current, entry.content))
                _replace_file(destination, entry.content)

        if manifest_entry and manifest_entry.status in {Status.CREATE, Status.UPDATE}:
            assert manifest_entry.content is not None
            destination = plan.target / MANIFEST_PATH
            unsafe_reason = destination_safety_error(plan.target, MANIFEST_PATH)
            if unsafe_reason:
                raise RuntimeError(
                    f"manifest became unsafe during installation: {unsafe_reason}"
                )
            if manifest_entry.status == Status.CREATE:
                _create_file(destination, manifest_entry.content)
                created.append((destination, manifest_entry.content))
            else:
                current = destination.read_bytes()
                if (
                    manifest_entry.expected is not None
                    and current != manifest_entry.expected
                ):
                    raise RuntimeError("installation manifest changed after planning")
                replaced.append((destination, current, manifest_entry.content))
                _replace_file(destination, manifest_entry.content)
    except Exception:
        for destination, original, written in reversed(replaced):
            if (
                destination.is_file()
                and not destination.is_symlink()
                and destination.read_bytes() == written
            ):
                _replace_file(destination, original)
        for destination, written in reversed(created):
            try:
                if (
                    destination.is_file()
                    and not destination.is_symlink()
                    and destination.read_bytes() == written
                ):
                    destination.unlink()
            except FileNotFoundError:
                pass
        _remove_empty_created_parents(plan.target, created)
        raise


def _remove_empty_created_parents(
    target: Path, created: list[tuple[Path, bytes]]
) -> None:
    candidates = {
        parent
        for destination, _content in created
        for parent in destination.parents
        if parent != target and target in parent.parents
    }
    for directory in sorted(candidates, key=lambda path: len(path.parts), reverse=True):
        try:
            directory.rmdir()
        except OSError:
            pass
