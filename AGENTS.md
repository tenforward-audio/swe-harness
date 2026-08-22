# AGENTS.md

## Product

- Project: `SWE Harness`
- Outcome: Keep software-engineering rules, work cards, capability policy, and
  durable decisions versioned beside the project they govern.
- Primary users: Codex agents and maintainers of software projects.
- Supported platforms or environments: Codex projects backed by a local
  filesystem, with Git repositories used for durable checkpoints.

Do not execute unresolved uppercase placeholder text as a command. Treat it as
missing project setup and ask only when the current task depends on it.

## Non-negotiable rules

- Repository files are canonical. Do not silently replace their cards,
  decisions, or policy with machine-local or external service state.
- Preserve user changes and keep unrelated work out of the diff.
- Never commit secrets, credentials, private data, or unlicensed fixtures.
- Do not weaken validation, suppress failures, or update golden files blindly.

## Stack and boundaries

- Stack: Markdown and YAML, with a Python standard-library CLI and validator.
- Architecture: `templates/default/` owns reusable generic content;
  `swe_harness/` owns deterministic rendering, reconciliation, and validation;
  `plugins/swe-harness/` is a thin optional Codex interface; this root contract
  routes intent; and `.agents/` owns project policy and live work state.
- Compatibility constraints: preserve the installed generic harness contract
  recorded in `.agents/HARNESS.md`; declare real consumers before adding
  migration or legacy-compatibility behavior.
- Keep behavior in the narrowest layer that owns it; avoid speculative
  abstractions and duplicated sources of truth.

## Compatibility decisions

- Never infer legacy support from repository history alone. Preserve an old
  shape only for a concrete supported release, current consumer, authoritative
  data set, staged rollout, or explicit project constraint. Record the scope,
  failure behavior, and removal condition of a temporary obligation.
- When project instructions explicitly classify prototype state as disposable,
  update current producers, consumers, tests, and fixtures together, then
  rebuild or reset instead of adding migrations, shims, or fallback paths.
- Never assume user data is disposable. Current-state validation, atomic
  publication, crash recovery, cache invalidation, and version identifiers are
  integrity work, not proof of a legacy-compatibility obligation.

## Working method

- Keep answers, diagnosis, research, comparison, planning, and review read-only
  unless the user explicitly asks for a change.
- Begin implementation only for an explicit change request or selected work item.
- Inspect the owning code, tests, instructions, and current behavior first.
- Complete the smallest coherent outcome through focused and configured gates.
- Test important success, invalid-input, failure, preservation, and user-visible
  paths at the owning boundary.
- Update documentation, decisions, tracking, and changelog when their claims
  change.
- After verifying a coherent requested change, create a local Conventional
  Commit checkpoint unless the user opts out; follow
  [the contributing guide](.agents/CONTRIBUTING.md) for isolation and staging.
- Checkpoint authority never includes push, tag, publication, release, history
  rewriting, branch changes, merges, or remote changes.

## Parallel work

- Automatic read-only evidence workers may share a checkout and do not require
  tracked work state. Their scope and delegation depth follow the skill
  execution-mode policy below.
- For explicitly requested parallel engineering lanes, name one parent In
  progress card, the common base, bounded lanes, dependencies, and owned files
  or boundaries before dispatch. Give every concurrent mutating lane an
  isolated worktree and non-overlapping ownership.
- A branch is the durable review identity; create one before checkpoint or
  review, never check it out in multiple worktrees, and never reuse it for a
  different change.
- Keep lifecycle-tracking checkpoints on the canonical coordinating branch so
  they never advance a pinned implementation candidate.
- The coordinating checkout owns intake and canonical status. Parallel authority
  does not imply merge, deletion, push, history-rewrite, or remote authority.

## Intent routing

- Explicit support ticket or feature request:
  [capture intake](.agents/skills/capture-project-intake/SKILL.md), then stop.
- Answer, diagnose, research, compare, plan, or audit:
  [investigate read-only](.agents/skills/investigate-project/SKILL.md).
- Preserve skipped, deferred, or multi-session planning unknowns, or revisit a
  named planning map or question:
  [map project planning](.agents/skills/map-project-planning/SKILL.md).
- Work on, start, or implement a selected recorded issue or feature from its
  current state through confirmation, checks, and Reviewing:
  [deliver project work](.agents/skills/deliver-project-work/SKILL.md).
- List open tickets or review items, summarise status, make a planning-only
  transition, record acceptance, return, abandon, or close recorded work:
  [manage project work](.agents/skills/manage-project-work/SKILL.md).
- Coordinate explicitly requested parallel agents, lanes, or worktrees:
  [coordinate parallel work](.agents/skills/coordinate-parallel-work/SKILL.md).
- Implement an explicitly authorised unrecorded change or one bounded In
  progress lane:
  [develop the project](.agents/skills/develop-project/SKILL.md).
- Technically review a defined candidate commit, branch, worktree, or patch:
  [review a project change](.agents/skills/review-project-change/SKILL.md).
- Integrate or merge an already reviewed candidate after explicit approval:
  [integrate a reviewed change](.agents/skills/integrate-reviewed-change/SKILL.md).
- Remove an explicitly named local worktree and branch after completed
  integration, handoff, or deliberate abandonment:
  [clean up a worktree](.agents/skills/clean-up-worktree/SKILL.md).
- Prepare versions, release notes, tags, or publication:
  [release the project](.agents/skills/release-project/SKILL.md).

Load only the skill and references relevant to the current task.
`deliver-project-work` owns the normal recorded-item path. For parallel
implementation, it uses `coordinate-parallel-work` while each mutating lane
follows `develop-project`.

### Skill execution modes

Every routed project skill declares one execution mode immediately after its
title:

- `inline`: the agent currently assigned the workflow performs it in its current
  context, and selecting the skill does not itself cause delegation. An
  `orchestrate-explicit` coordinator may still assign an `inline` skill to a
  bounded worker in its required isolation.
- `delegate-readonly`: after reading the skill and its required project
  instructions, the active agent responsible for the user-facing outcome scopes
  the evidence work before dispatch. Use one read-only subagent when the job is
  cohesive and bounded. If one worker would need to re-delegate or the work has
  independent evidence boundaries, the active agent splits it into bounded,
  non-overlapping scopes and dispatches multiple sibling read-only subagents
  itself. Give each worker only its assigned question, repository location,
  scope, constraints, and required evidence rather than unrelated conversation
  history.
- `orchestrate-explicit`: dispatch is allowed only after the user explicitly
  requests parallel work. Follow the skill's lane, ownership, and isolation
  rules before creating agents or worktrees.

Every read-only dispatch must tell the recipient that it is a delegated worker.
A delegated worker follows the selected skill's workflow and safety rules but
treats its execution mode as `inline`: it must not dispatch another subagent. If
its assignment is too broad or blocked, it returns that evidence and a proposed
split to the active agent, which may rescope the work and dispatch siblings. The
active agent checks and synthesises returned evidence without repeating the full
investigation.

If read-only subagents are unavailable or fail, continue inline and disclose
the fallback. Delegation never broadens mutation, approval, lifecycle, branch,
worktree, integration, remote, or release authority. Subagent reports are
evidence for the active agent, not independent authority to act.

### Skill use response

When a routed project skill is selected, begin the first progress update with:

```text
Using skill: `<skill-name>`
└─ <Brief description of the job being performed>
```

Use the exact skill name from its front matter and keep the description to one
action-focused line. Omit this update when no project skill is selected.

## Work tracking

- [The workflow contract](.agents/WORKFLOW.md) is the only source for card
  fields and lifecycle transitions.
- [Active planning maps](.agents/planning/ACTIVE.md) and the
  [planning ledger](.agents/planning/LEDGER.md) preserve precise unknowns, GNDN
  notes, dependencies, and resolutions upstream of delivery work.
- Planning maps, delivery intake queues, and status boards own their respective
  live state. Load only the relevant source unless the user requests an
  overview or migration.
- [The research archive](.agents/RESEARCH.md) retains material findings from
  abandoned planning or research; it never owns live status.

## Plugin capabilities

- [The plugin capability policy](.agents/PLUGINS.md) is the only source for
  required and approved project plugins.
- Read it before declaring or relying on a project plugin capability.

## Quality commands

- Setup: `python3 --version`
- Affected-layer gates: `python3 scripts/check_harness.py`
- Format check: not configured; keep Markdown readable and Python PEP 8 aligned.
- Lint: not configured; the structural validator is the current policy gate.
- Type or static checks:
  `python3 -m compileall -q swe_harness scripts plugins/swe-harness/scripts`
- Tests: `python3 -m unittest discover -s tests`
- Build: `python3 scripts/build_plugin.py --output PATH_TO_NEW_DIRECTORY`
- Cross-stack checks without builds: `python3 scripts/check_harness.py`
- Full checkpoint and release gate:
  `python3 -m unittest discover -s tests && python3 scripts/check_harness.py && python3 -m compileall -q swe_harness scripts plugins/swe-harness/scripts`

While iterating, run focused tests and only the affected-layer gate. Run the
full gate once after the coherent change and before checkpoint or release.
Quality wrappers must preserve exit status and complete output in private
temporary logs, print one concise success line, and show a bounded failure
excerpt plus the full log location. Quiet output must not skip validation.

## Review and completion

- Prioritise correctness, security, data loss, public compatibility, race and
  failure behavior, and missing tests.
- Give actionable findings with a concrete failure scenario and safest fix.
- Done means the requested outcome works for its intended user, applicable
  checks pass, important failure paths are covered, public claims agree, and a
  clean checkout remains reproducible.
