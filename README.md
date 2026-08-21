# SWE Harness

**Give Codex a shared playbook for shipping software, not another chat to
remember.**

SWE Harness keeps the rules, work, and decisions that matter beside your code.
Codex knows how your project works, maintainers can see what is happening, and
the useful context survives long after the conversation ends.

## Why use it?

- **Talk normally.** Capture an idea, pick up a ticket, review a change, or
  prepare a release with plain-language requests.
- **Keep everyone aligned.** Project policy, active work, and durable decisions
  live in the repository as one shared source of truth.
- **Use sub-agents with purpose.** Focused workers can gather evidence or tackle
  explicitly requested parallel lanes without turning the main conversation
  into a wall of detail.
- **Stay in control.** Reviews, integration, releases, and destructive clean-up
  remain separate, deliberate actions.

## Just ask

| What you say | What SWE Harness does |
| --- | --- |
| `Support ticket: checkout fails after applying a discount` | Records an issue for later |
| `Feature request: add an order history page` | Captures the idea without starting implementation |
| `Show me the open tickets` | Lists open issues across intake and active boards |
| `Show me the open work` | Lists open issues and feature ideas in every live state |
| `Work on ISSUE-001` | Confirms the plan, implements it, checks it, and hands it over for review |
| `Work on FEATURE-001 with API and UI lanes in parallel` | Coordinates one outcome across isolated implementation lanes |
| `Review commit abc123` | Reviews the candidate without changing it |
| `Accept ISSUE-001` | Accepts an item from Reviewing and records the durable result |

Support tickets and feature requests are capture-only. When you say `Work on
ISSUE-001`, Codex confirms the scope before making changes, then takes the item
through implementation and checks. Passing work moves to Reviewing.
Codex stops there until you accept the result or request changes.

## Sub-agents, sensibly

Investigation and code review can use bounded, read-only sub-agents to gather
the detailed evidence. The active agent stays responsible for the answer, and a
delegated worker cannot create a chain of more workers.

Parallel implementation happens only when you ask for it. Each code-changing
lane gets its own Git worktree and branch, with clear ownership under one parent
outcome. Integration is still a separate decision.

## A lightweight workflow

`Capture → Plan → Build → Review → Accept`

There is no completed-work graveyard to maintain. Accepted results live where
they are useful: in Git history, documentation, the changelog, or a decision
record. Small, explicitly authorised changes can skip the card workflow
entirely.

The repository remains canonical throughout. Local agent state and external
trackers can help with the work, but they never silently replace project policy
or cards. The full lifecycle lives in [`.agents/WORKFLOW.md`](.agents/WORKFLOW.md).

## Install

Start the interactive setup from this checkout:

```sh
python3 -m swe_harness init /path/to/project
```

Validation is read-only. Upgrades preview by default and only change files when
you add `--apply`:

```sh
python3 -m swe_harness validate /path/to/project --require-manifest
python3 -m swe_harness upgrade /path/to/project --defaults --non-interactive --require-complete
python3 -m swe_harness upgrade /path/to/project --defaults --non-interactive --require-complete --apply
```

Project edits are preserved and conflicts stop the upgrade. Automated setup is
also supported; run `python3 -m swe_harness init --help` for the available
options.

The installer adds the shared playbook, focused workflow skills, simple
Markdown boards, and project policy. The optional Codex plugin wraps the same
harness; build it with:

```sh
python3 scripts/build_plugin.py
```

## Develop

```sh
python3 -m unittest discover -s tests
python3 scripts/check_harness.py
python3 -m compileall -q swe_harness scripts plugins/swe-harness/scripts
```

Architecture and repository authority are documented in
[`.agents/decisions/`](.agents/decisions/).

## Licence

SWE Harness is available under the [MIT License](LICENSE).
