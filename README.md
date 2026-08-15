# SWE Harness

SWE Harness is a repository-native operating model for software engineering
with Codex. It keeps project rules, work cards, capability policy, verification,
and durable decisions versioned beside the code they govern.

## Source-of-truth map

Each kind of fact has exactly one canonical owner. Other documents link to that
owner instead of restating it. [ADR 0001](.agents/decisions/0001-repository-authority.md)
records why authority stays in the repository.

| Concern | Canonical source |
| --- | --- |
| Product contract, safety boundaries, and intent routing | [`AGENTS.md`](AGENTS.md) |
| Harness navigation and authority map | [`.agents/README.md`](.agents/README.md) |
| Card schema and lifecycle transitions | [`.agents/WORKFLOW.md`](.agents/WORKFLOW.md) |
| Unselected issues and ideas | [`.agents/ISSUES.md`](.agents/ISSUES.md) and [`.agents/FEATURES.md`](.agents/FEATURES.md) |
| Selected work status | [`.agents/workboard/`](.agents/workboard/) |
| Required and approved plugin capabilities | [`.agents/PLUGINS.md`](.agents/PLUGINS.md) |
| Reusable template parity | [`.agents/HARNESS.md`](.agents/HARNESS.md) |
| Durable architectural rationale | [`.agents/decisions/`](.agents/decisions/) |
| Delivered user-visible changes | [`CHANGELOG.md`](CHANGELOG.md) |

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
before investigating, implementing, coordinating, or releasing work.

## Validate the harness

The project uses only Python's standard library:

```sh
python3 -m unittest discover -s tests
python3 scripts/check_harness.py
```

The validator checks the authority structure without treating prose as a second
database. It verifies required sources, internal links, resolved project setup,
unique tracked identifiers, the work-in-progress limit, and unique skill names.
