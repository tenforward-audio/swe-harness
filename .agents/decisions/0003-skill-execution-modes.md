# ADR 0003: Declare skill execution modes

- Status: Accepted
- Date: 2026-08-21
- Decision owners: Project maintainers

## Context

Running every skill in the active conversation makes detailed investigation
and review output compete with the user's context. Automatically delegating all
skills would instead move authoritative state changes and permission-sensitive
operations into background contexts, while unrestricted orchestration could
create agents, branches, or worktrees the user did not request.

The harness needs a predictable policy that identifies which workflows benefit
from context isolation without weakening their authority or safety boundaries.

## Options considered

- Run every skill inline in the active conversation.
- Let the active agent decide whether to delegate each skill without a declared
  policy.
- Declare inline, single read-only delegation, and explicit orchestration modes
  for the canonical project skills.
- Run every skill in a subagent and return only its final report.

## Decision

Every canonical project skill declares one of three execution modes in its
`SKILL.md`:

- `inline` keeps authoritative, mutating, approval-sensitive, and compact
  workflows in the active agent.
- `delegate-readonly` automatically gives one bounded read-only subagent the
  evidence-gathering task when subagents are available. Investigation and
  candidate review use this mode. The active agent retains responsibility for
  reading the governing instructions, checking the returned evidence, and
  answering the user.
- `orchestrate-explicit` permits multi-agent dispatch only after the user asks
  for parallel work and the coordination skill establishes lanes, ownership,
  dependencies, and isolation.

If a read-only subagent is unavailable or fails, the active agent performs the
work inline and discloses the fallback. Delegation does not add mutation,
approval, lifecycle, branch, worktree, integration, remote, or release
authority. The structural validator requires valid execution declarations only
for canonical skills supplied by the selected template, preserving unmanaged
project-specific skills during validation and upgrades.

## Consequences

- Detailed read-only evidence gathering no longer has to consume the active
  conversation's working context.
- Investigation and review behavior becomes predictable across installed
  harnesses instead of depending on ad hoc model judgment.
- Canonical-state changes remain owned by the active agent, and parallel
  mutation still requires explicit user intent and worktree isolation.
- Hosts without subagent support retain a defined inline fallback.
- New canonical skills must select a valid execution mode; custom project skills
  may adopt the convention without being rejected if they do not.

## Reversal conditions

Reconsider the three modes if the host exposes a stable native execution-policy
schema, if subagent reports cannot preserve sufficient review evidence, or if a
workflow needs a different isolation model. A replacement must keep delegation
bounded, preserve active-agent authority, and define behavior when the requested
execution capability is unavailable.
