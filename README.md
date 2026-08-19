# SWE Harness

SWE Harness is a repository-native operating model for software engineering
with Codex. This repository is the single source for the reusable template,
installer behavior, validation rules, and optional Codex plugin. Each installed
project then owns its rendered rules, work cards, capability policy, and durable
decisions beside the code they govern.

## Start a project

Run the interactive initializer from this checkout:

```sh
python3 -m swe_harness init /path/to/project
```

It asks only for missing project facts, refuses to overwrite different existing
content, and records installed checksums in `.agents/HARNESS.json`. For an
automated setup, preview conservative defaults before applying them:

```sh
python3 -m swe_harness init /path/to/project --defaults --non-interactive --require-complete --dry-run
python3 -m swe_harness init /path/to/project --defaults --non-interactive --require-complete
```

Validate or safely reconcile an installed project:

```sh
python3 -m swe_harness doctor /path/to/project --require-manifest
python3 -m swe_harness upgrade /path/to/project --defaults --non-interactive --require-complete
python3 -m swe_harness upgrade /path/to/project --defaults --non-interactive --require-complete --apply
```

`upgrade` is a dry run unless `--apply` is present. It automatically replaces
only files that still match their recorded installation checksum. Project-edited
files are marked `REVIEW`, and retired template files are never deleted.

## Source-of-truth map

Each kind of fact has exactly one canonical owner. Other documents link to that
owner instead of restating it. [ADR 0001](.agents/decisions/0001-repository-authority.md)
records why authority stays in the repository.

| Concern | Canonical source |
| --- | --- |
| Reusable generic harness content | [`templates/default/`](templates/default/) |
| Rendering, reconciliation, and validation behavior | [`swe_harness/`](swe_harness/) |
| Optional Codex plugin surface | [`plugins/swe-harness/`](plugins/swe-harness/) |
| Product contract, safety boundaries, and intent routing | [`AGENTS.md`](AGENTS.md) |
| Harness navigation and authority map | [`.agents/README.md`](.agents/README.md) |
| Card schema and lifecycle transitions | [`.agents/WORKFLOW.md`](.agents/WORKFLOW.md) |
| Unselected issues and ideas | [`.agents/ISSUES.md`](.agents/ISSUES.md) and [`.agents/FEATURES.md`](.agents/FEATURES.md) |
| Selected work status | [`.agents/workboard/`](.agents/workboard/) |
| Required and approved plugin capabilities | [`.agents/PLUGINS.md`](.agents/PLUGINS.md) |
| Reusable template parity | [`.agents/HARNESS.md`](.agents/HARNESS.md) |
| Durable architectural rationale | [`.agents/decisions/`](.agents/decisions/) |
| Delivered user-visible changes | [`CHANGELOG.md`](CHANGELOG.md) |

The reusable sources above are never copied back from an installed project or a
personal skill directory. Once rendered, a target repository owns its project
choices. Its checksum manifest is provenance for safe reconciliation, not a
claim that generated files outrank project edits. [ADR 0002](.agents/decisions/0002-distribution-and-reconciliation.md)
records this boundary and the choice to make the CLI the core product while the
plugin remains a convenience layer.

The location of a card is its status. Plugin installation and connection state
are local runtime observations; the repository records only the desired
capability and its authority boundary.

## Workflow at a glance

```text
issue or idea -> Planning -> In progress -> Reviewing -> accepted history
                     ^                            |
                     +------ changes needed -----+
```

Read [the workflow contract](.agents/WORKFLOW.md) before changing a queue or
board. Use the narrow intent-specific skill linked from [`AGENTS.md`](AGENTS.md)
before investigating, listing or transitioning work, coordinating parallel
lanes, implementing, reviewing, integrating, or releasing work.

## Optional Codex plugin

The plugin adds one setup skill; it does not add an MCP server, external
tracker, custom interface, or second template copy. Build a self-contained
plugin directory from the canonical repository sources:

```sh
python3 scripts/build_plugin.py
```

The generated `dist/swe-harness/` directory is intentionally untracked. Install
or publish it only as a separate, explicit action. The source checkout and the
built plugin expose the same `init`, `upgrade`, and `doctor` commands.

## Develop and validate

The project uses only Python's standard library:

```sh
python3 -m unittest discover -s tests
python3 scripts/check_harness.py
python3 -m compileall -q swe_harness scripts plugins/swe-harness/scripts
```

The tests include a clean, self-contained plugin build and install. The validator
checks authority structure without treating prose as a second database. It
verifies required sources, internal links, resolved project setup, unique tracked
identifiers, the work-in-progress limit, unique skill names, and installation
metadata integrity.
