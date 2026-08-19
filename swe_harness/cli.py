"""Command-line interface for SWE Harness installation and validation."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

from .install import ChangePlan, apply_plan, plan_init, plan_upgrade
from .template import (
    TemplateBundle,
    default_answers,
    default_template_root,
    parse_assignments,
    prompt_specs,
    read_answers,
    unresolved_active_placeholders,
)
from .validation import inspect_harness


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="swe-harness",
        description="Install, upgrade, and validate a repository-owned SWE harness.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="install into a repository")
    _add_target(init_parser)
    _add_answers(init_parser)
    init_parser.add_argument(
        "--dry-run", action="store_true", help="show the plan without writing files"
    )

    upgrade_parser = subparsers.add_parser(
        "upgrade", help="safely reconcile a newer template"
    )
    _add_target(upgrade_parser)
    _add_answers(upgrade_parser)
    upgrade_parser.add_argument(
        "--apply",
        action="store_true",
        help="apply safe changes; the default is a dry run",
    )

    validate_parser = subparsers.add_parser(
        "validate", help="validate an installed harness"
    )
    _add_target(validate_parser)
    validate_parser.add_argument(
        "--require-manifest",
        action="store_true",
        help="treat missing installation metadata as an error",
    )
    return parser


def _add_target(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("path", nargs="?", type=Path, default=Path("."))
    parser.add_argument(
        "--template",
        type=Path,
        default=None,
        help="template root; defaults to the bundled template",
    )


def _add_answers(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--answers", type=Path, help="JSON object of template answers")
    parser.add_argument(
        "--set",
        dest="assignments",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="set one template answer; may be repeated",
    )
    parser.add_argument(
        "--defaults",
        action="store_true",
        help="fill unanswered project values with conservative defaults",
    )
    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="never prompt for missing project values",
    )
    parser.add_argument(
        "--require-complete",
        action="store_true",
        help="fail when non-ADR placeholders remain unresolved",
    )


def _bundle(template_path: Path | None) -> TemplateBundle:
    return TemplateBundle(template_path or default_template_root())


def _collect_answers(args: argparse.Namespace, bundle: TemplateBundle) -> dict[str, str]:
    answers: dict[str, str] = {}
    if args.answers:
        answers.update(read_answers(args.answers))
    answers.update(parse_assignments(args.assignments))
    if args.defaults:
        for key, value in default_answers(args.path).items():
            answers.setdefault(key, value)

    if not args.non_interactive and sys.stdin.isatty():
        for spec in prompt_specs(args.path):
            if spec.key not in bundle.active_placeholders() or spec.key in answers:
                continue
            response = input(f"{spec.label} [{spec.default}]: ").strip()
            answers[spec.key] = response or spec.default
    bundle.validate_answers(answers)
    return answers


def _print_plan(plan: ChangePlan) -> None:
    for entry in plan.entries:
        suffix = f" — {entry.reason}" if entry.reason else ""
        print(f"{entry.status.value:9} {entry.relative.as_posix()}{suffix}")
    print(f"TEMPLATE_REVISION {plan.revision}")


def _run_change(args: argparse.Namespace, mode: str) -> int:
    bundle = _bundle(args.template)
    answers = _collect_answers(args, bundle)
    rendered = bundle.render(answers)
    unresolved = sorted(unresolved_active_placeholders(rendered))
    if unresolved:
        print("UNRESOLVED " + ", ".join("{{" + key + "}}" for key in unresolved))
        if args.require_complete:
            return 2

    if mode == "init":
        plan = plan_init(bundle, args.path, answers)
        should_apply = not args.dry_run
    else:
        plan = plan_upgrade(bundle, args.path, answers)
        should_apply = args.apply
    _print_plan(plan)

    if plan.blockers:
        print("BLOCKED no files changed")
        return 2
    if should_apply:
        apply_plan(plan)
        print(f"APPLIED {len(plan.changes)} files")
    else:
        print("DRY_RUN no files changed")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            return _run_change(args, "init")
        if args.command == "upgrade":
            return _run_change(args, "upgrade")
        if args.command == "validate":
            bundle = _bundle(args.template)
            findings = inspect_harness(args.path, bundle, args.require_manifest)
            for finding in findings:
                print(f"{finding.severity:5} {finding.message}")
            errors = [finding for finding in findings if finding.severity == "ERROR"]
            if errors:
                return 1
            print("Harness check passed")
            return 0
    except (OSError, RuntimeError, ValueError) as error:
        print(f"ERROR {error}", file=sys.stderr)
        return 2
    parser.error(f"unknown command: {args.command}")
    return 2
