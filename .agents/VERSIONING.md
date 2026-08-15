# Versioning and releases

- Version source: no authoritative version exists until the first release is
  explicitly prepared.
- Release command: no automated release command is configured.
- Tag format: `vMAJOR.MINOR.PATCH`

## Version policy

Use Semantic Versioning for public releases:

- `fix` and `perf` changes imply a patch release;
- `feat` changes imply a minor release;
- a breaking change implies a major release after `1.0.0` and a minor release
  during `0.x`;
- `docs`, `test`, `build`, `ci`, and `chore` do not independently require a
  release unless they change the distributed product.

Mark breaking Conventional Commits with `!` or a `BREAKING CHANGE:` footer.
Use the highest required bump across unreleased changes. Compatibility and
migration work must follow a concrete supported constraint or decision, not
repository history alone. If project instructions classify prototype state as
disposable, rebuild or reset it instead.

Do not infer a version before the first release is explicitly prepared and an
authoritative version source is added.

## Changelog

Keep [the changelog](../CHANGELOG.md) user-facing under `Unreleased`. Record
Added, Changed, Deprecated, Removed, Fixed, and Security changes as applicable.
Edit commit messages into user-facing release notes.

## Release workflow

1. Confirm scope, supported compatibility obligations, migrations, and bump.
2. Run the full check-and-build gate from `AGENTS.md` once on a clean checkout.
3. Review dependency notices, security implications, and supported platforms.
4. Replace `Unreleased` entries with version and ISO date, then add a fresh
   `Unreleased` section.
5. Update the authoritative version source and verify built artifacts report it.
6. Tag and publish only when the user explicitly requests those external
   actions and credentials or approvals are available.

Never present an unsigned, unverified, or development artifact as trusted.
Document deprecations before removal and include actionable migration notes for
actual supported breaking changes.
