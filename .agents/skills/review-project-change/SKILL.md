---
name: review-project-change
description: Technically review a defined candidate commit, branch, worktree, or patch without changing product behavior, tracking state, branches, or external systems. Use for pre-integration code review, candidate-versus-base comparison, verification evidence, and actionable findings. Do not use for general investigation, implementation, lifecycle transitions, acceptance, or integration.
---

# Review a Project Change

## Execution mode

`delegate-readonly`

## Pin the review target

1. Read the root `AGENTS.md`, relevant policies, owning implementation, and
   existing tests.
2. Resolve the exact candidate commit or supplied patch and its intended common
   base. A moving branch or worktree name is not a stable review target.
3. Inspect candidate commits, changed paths, the complete diff from the common
   base, and interaction with current canonical state.
4. If the candidate cannot be pinned or its base is ambiguous, report that
   uncertainty instead of reviewing an inferred target.

Keep the review read-only. Do not edit files, queues, boards, branches, commits,
worktrees, dependencies, releases, or external systems.

## Review risk and evidence

- Prioritise correctness, security, data loss, public compatibility,
  concurrency, operational failure behavior, preservation guarantees, and
  missing tests.
- Trace changed inputs, state transitions, failures, and outputs through the
  owning boundary. Review important success, invalid-input, failure,
  preservation, and supported-compatibility paths.
- Audit changes to root instructions and `.agents/` separately. Identify stale
  queue, board, policy, or evidence copies that must not displace the
  coordinating checkout's canonical state.
- Run only non-mutating focused checks that materially improve confidence.
  Distinguish automated results, manually observed behavior, unobserved manual
  acceptance, and checks that could not be run.
- Do not infer compatibility obligations from repository history alone. Tie any
  obligation to a supported release, current consumer, authoritative data set,
  staged rollout, or explicit constraint.

## Return a review decision aid

- Lead with actionable findings ordered by severity. For each finding, name the
  concrete failure scenario, affected boundary, evidence, and safest fix.
- Say plainly when no material finding is present and record residual risks or
  unobserved evidence.
- Identify the exact reviewed commit, common base, checks run, and whether the
  candidate changed after review began.
- Return the evidence without accepting, integrating, or changing lifecycle
  state. Use [`manage-project-work`](../manage-project-work/SKILL.md) for an
  explicit acceptance or return decision, and
  [`integrate-reviewed-change`](../integrate-reviewed-change/SKILL.md) for a
  separately authorised integration.
