---
name: release-project
description: Plan, prepare, review, version, document, tag, or publish this project's releases using Semantic Versioning, Conventional Commits, changelog, supported compatibility, dependency, and security gates. Use for version bumps, release notes, release readiness, deprecations, tags, or publishing. Never tag or publish without explicit authorisation.
---

# Release the Project

## Execution mode

`inline`

## Establish release scope

1. Read [the versioning policy](../../VERSIONING.md) and relevant Unreleased
   entries in [the changelog](../../../CHANGELOG.md).
2. Read only cards and decisions that affect this release.
3. Resolve the configured version source; do not guess while its placeholder is
   unresolved.
4. Classify user-visible changes, concrete supported compatibility obligations,
   deprecations, migrations, dependency notices, and security implications.

Do not add migration or deprecation work merely because an older repository
shape exists. Tie it to a supported release, current consumer, authoritative
data set, staged rollout, or explicit constraint.

## Choose the SemVer bump

- Use patch for `fix` or `perf`, minor for `feat`, and the highest required
  bump across unreleased changes.
- Use major for breaking changes after `1.0.0`, and minor during `0.x`.
- Do not bump solely for `docs`, `test`, `build`, `ci`, or `chore` unless
  the distributed product changes.
- Verify actual public compatibility rather than trusting commit text alone.

## Prepare and verify

- Edit changelog entries into concise user-facing notes.
- Include actionable migration guidance before an actual supported removal.
- Run the clean-checkout full gate once, plus required platform or artifact
  checks.
- Review dependency licences and notices, advisories, and security notes.
- Update the authoritative version source and verify built artifacts report it.
- Roll `Unreleased` into a dated version and create a fresh section only when
  the release is actually being prepared.

## Keep external actions gated

Do not create or push a tag, publish a package, upload an artifact, deploy, sign,
notarise, or send release communications unless the user explicitly asks for
that action. Report missing credentials, human verification, or platform
evidence as blockers without weakening the gate.
