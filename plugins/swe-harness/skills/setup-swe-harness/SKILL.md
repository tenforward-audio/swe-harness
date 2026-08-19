---
name: setup-swe-harness
description: Safely initialise, upgrade, or validate a repository-owned SWE Harness. Use when a user wants project instructions, work cards, workflow policy, repo-local skills, or release guidance installed or reconciled without replacing ambiguous project-owned content.
---

# Set Up SWE Harness

Begin the first progress update with:

```text
Using skill: `setup-swe-harness`
└─ <Brief description of the job being performed>
```

Use the bundled deterministic CLI as the only mutating boundary. Resolve the
plugin root from this `SKILL.md`, then run:

```text
python3 PLUGIN_ROOT/scripts/swe-harness.py COMMAND
```

## Choose the operation

- Use `init` when `.agents/HARNESS.json` is absent.
- Use `upgrade` when that manifest is present and the user requests an upgrade.
- Use `doctor` for read-only validation.

Resolve the target repository from an explicit user path, then its Git root,
then the current working directory. Never target a home directory, filesystem
root, or another broad directory.

## Initialise

1. Collect known project values with repeated `--set KEY=VALUE` options.
2. Use `--defaults` only when the user explicitly accepts generic defaults.
3. Preview with `init TARGET --dry-run --non-interactive --require-complete`.
4. If the preview reports conflicts, inspect them and stop. Do not overwrite.
5. Repeat the identical command without `--dry-run` only when the plan is safe.
6. Run `doctor TARGET --require-manifest`.

Do not infer a project's stack, commands, licence, release target, supported
versions, or security contact.

## Upgrade

1. Run `upgrade TARGET` first; upgrade is a dry run by default.
2. Treat every `REVIEW` result as a project-owned merge requiring approval.
3. Add `--apply` only when every proposed update is unambiguous.
4. Run `doctor TARGET --require-manifest` after applying.

Never delete retired files during an upgrade.

## Validate only

Run `doctor TARGET`. Treat `NOTE` messages as information and `ERROR` messages
as blockers.

Do not install marketplace entries, push commits, tag versions, publish
packages, or create releases unless the user explicitly requests that action.
