# Contributing

Read [the root instructions](../AGENTS.md) and use the relevant skill under
`.agents/skills` before making changes.

Before changing tracked work, read the canonical [workflow](WORKFLOW.md).
Before adding or relying on an external capability, read the
[plugin policy](PLUGINS.md). Do not duplicate either contract in a card or ADR.

## Change workflow

1. Confirm the intended user or project outcome and owning boundary.
2. Inspect current behavior and tests before selecting an approach.
3. Keep the change coherent and preserve unrelated work.
4. Add or update focused tests and documentation.
5. Run focused tests and the configured affected-layer gate while iterating,
   then run the configured full check-and-build gate once before checkpoint.
6. Review the working tree, stage only files owned by the completed change, and
   inspect the staged diff.
7. Create a Conventional Commit checkpoint automatically unless the user opts
   out or the scope cannot be isolated safely.

Use Conventional Commits. Explain breaking behavior and required migration in
the commit body and [changelog](../CHANGELOG.md) only when a concrete supported
compatibility obligation exists. Repository history alone does not create one.

Do not commit generated artifacts unless the repository explicitly tracks them.
Never include secrets, unrelated or pre-existing user changes, or failing work.
Automatic checkpoints do not authorise a push, tag, publication, or release.
Do not bypass failed checks, hooks, signing, or author identity. Report the
blocker instead. Never amend or rewrite history, rebase, merge, switch branches,
or alter remotes without an explicit request.

Dependency changes must follow [the dependency policy](DEPENDENCIES.md).
Durable architectural choices require an ADR; ordinary implementation details
do not.
