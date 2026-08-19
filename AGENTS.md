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

- Read-only lanes may share a checkout. Give every concurrent mutating lane an
  isolated worktree and non-overlapping ownership.
- Before dispatch, name one parent In progress card, the common base, bounded
  lanes, dependencies, and owned files or boundaries.
- A branch is the durable review identity; create one before checkpoint or
  review, never check it out in multiple worktrees, and never reuse it for a
  different change.
- The coordinating checkout owns intake and canonical status. Parallel authority
  does not imply merge, deletion, push, history-rewrite, or remote authority.

## Intent routing

- Explicit support ticket or feature request:
  [capture intake](.agents/skills/capture-project-intake/SKILL.md), then stop.
- Answer, diagnose, research, compare, plan, or audit:
  [investigate read-only](.agents/skills/investigate-project/SKILL.md).
- Work on, start, or implement a selected recorded issue or feature from its
  current state through confirmation, checks, and Reviewing:
  [deliver project work](.agents/skills/deliver-project-work/SKILL.md).
- List open tickets or review items, summarise status, make a planning-only
  transition, record acceptance, return, or close recorded work:
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
- Prepare versions, release notes, tags, or publication:
  [release the project](.agents/skills/release-project/SKILL.md).

Load only the skill and references relevant to the current task.
`deliver-project-work` owns the normal recorded-item path. For parallel
implementation, it uses `coordinate-parallel-work` while each mutating lane
follows `develop-project`.

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
- Intake queues and status boards own live state. Load only the relevant source
  unless the user requests an overview or migration.

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
