# Style guide

Configured formatters, linters, language standards, and established local
patterns are authoritative. This guide supplies only cross-language defaults.

## Names and data

- Use domain names that communicate purpose; avoid vague managers, processors,
  helpers, and generic abbreviations.
- Put ambiguous units in names, such as `timeoutSeconds` or `fileSizeBytes`.
- Use `{{LANGUAGE_VARIANT}}` in project-owned prose and names unless an external
  API dictates spelling.
- Prefer explicit state and plain data over hidden mutation or deep hierarchy.

## Modules and boundaries

- Keep one clear responsibility per module without creating one file per
  function.
- Keep domain behavior out of presentation and infrastructure glue.
- Do not create generic dumping grounds such as `utils`, `helpers`, or `common`.
- Introduce interfaces and abstractions only for a current boundary or test seam.

## Errors, comments, and logs

- Model expected invalid input as data; reserve exceptions for failed operations
  and broken invariants.
- Preserve the failed operation, logical item, safe consequence, and underlying
  cause in useful errors.
- Comment why a constraint or workaround exists, not what obvious code does.
- Never log secrets, private payloads, or unnecessary identifying data.

## Tests and maintenance

- Name tests after behavior and cover success, invalid input, operational
  failure, compatibility, and preservation where relevant.
- Inspect deterministic fixture or snapshot changes; never regenerate blindly.
- Avoid placeholders presented as completion, blanket suppressions, speculative
  configuration, and rewrites made only for stylistic preference.
