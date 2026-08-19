# SWE Harness

SWE Harness gives Codex and project maintainers a shared, repository-owned way
to organise software work. Project rules, tickets, decisions, and engineering
guidance stay beside the code instead of disappearing into chat history.

## How to use it

Once SWE Harness is installed, talk to Codex normally. Clear phrases at the
start of a request help it choose the right workflow:

| What you say | What happens |
| --- | --- |
| `Support ticket: checkout fails after applying a discount` | Records an issue without starting work on it |
| `Feature request: add an order history page` | Records a feature idea without implementing it |
| `Show me the open tickets` | Lists the current issue and feature queues |
| `Promote ISSUE-001 to Planning` | Turns the selected ticket into a scoped work card |
| `Start ISSUE-001` | Moves it into the single In progress slot |
| `Implement ISSUE-001` | Makes the change and runs the project checks |
| `Review commit abc123` | Reviews that candidate without changing it |
| `Accept ISSUE-001` | Records the result and removes the completed card |
| `Prepare a release` | Checks versioning and release readiness without publishing |

Support tickets and feature requests are capture-only: Codex records them and
stops. Ask it to promote or implement an item when you are ready to act on it.

## Workflow

The file containing a card is its status, so there is never a second status
field to keep in sync.

```mermaid
flowchart LR
    issue["Support ticket<br/>ISSUES.md"]
    feature["Feature request<br/>FEATURES.md"]
    planning["Planning<br/>scoped and prioritised"]
    progress["In progress<br/>one WIP slot"]
    review["Reviewing<br/>evidence and acceptance"]
    outcome["Durable result<br/>Git · changelog · docs · ADR"]

    issue -->|promote| planning
    feature -->|promote| planning
    planning -->|start| progress
    progress -->|checks complete| review
    review -->|accept| outcome
    review -->|changes needed| planning
    issue -->|close| outcome
    feature -->|reject| outcome
```

There is no completed board. Accepted results live in Git history and, when
useful, the changelog, documentation, or an architectural decision record.
Small, explicitly authorised changes can be completed without creating a card.

The full lifecycle is defined in [`.agents/WORKFLOW.md`](.agents/WORKFLOW.md).

## What it adds

- A root [`AGENTS.md`](AGENTS.md) that routes each request to one focused skill.
- Repository-local skills for intake, investigation, implementation, review,
  integration, parallel work, and releases.
- Markdown queues and Planning, In progress, and Reviewing boards.
- Engineering, dependency, security, plugin, versioning, and contribution
  policy under [`.agents/`](.agents/).
- A standard-library Python CLI for safe installation, upgrade, and validation.
- A checksum manifest that protects project-owned edits during upgrades.

Repository files remain canonical. Local agent state and external trackers may
help perform work, but they do not silently replace project policy or cards.

## Install and maintain

Run the interactive initialiser from this checkout:

```sh
python3 -m swe_harness init /path/to/project
```

For automated setup, preview before applying:

```sh
python3 -m swe_harness init /path/to/project --defaults --non-interactive --require-complete --dry-run
python3 -m swe_harness init /path/to/project --defaults --non-interactive --require-complete
```

Validate or safely upgrade an installed harness:

```sh
python3 -m swe_harness validate /path/to/project --require-manifest
python3 -m swe_harness upgrade /path/to/project --defaults --non-interactive --require-complete
python3 -m swe_harness upgrade /path/to/project --defaults --non-interactive --require-complete --apply
```

Upgrade is a dry run unless `--apply` is present. Unchanged generic files can be
updated automatically; project-edited files are marked `REVIEW`, conflicts
block application, and retired files are never deleted.

## Optional Codex plugin

The optional `setup-swe-harness` skill is a thin interface over the same CLI and
template. Build the self-contained plugin with:

```sh
python3 scripts/build_plugin.py
```

The generated `dist/swe-harness/` directory is intentionally untracked.

## Maintainer map

| Concern | Canonical source |
| --- | --- |
| Reusable generic harness | [`templates/default/`](templates/default/) |
| Installation, reconciliation, and validation | [`swe_harness/`](swe_harness/) |
| Optional Codex plugin | [`plugins/swe-harness/`](plugins/swe-harness/) |
| Product contract and intent routing | [`AGENTS.md`](AGENTS.md) |
| Policy, cards, and decisions | [`.agents/`](.agents/) |

[ADR 0001](.agents/decisions/0001-repository-authority.md) explains repository
authority. [ADR 0002](.agents/decisions/0002-distribution-and-reconciliation.md)
explains distribution and safe reconciliation.

## Develop and validate

```sh
python3 -m unittest discover -s tests
python3 scripts/check_harness.py
python3 -m compileall -q swe_harness scripts plugins/swe-harness/scripts
```

## Licence

SWE Harness is available under the [MIT License](LICENSE).
