# Plugin capability policy

This file is the canonical project record of required and approved plugin
capabilities. It records desired state and authority, not whether a plugin is
installed, connected, or signed in on a particular machine.

## Operating rules

- Prefer repository files, repo-local skills, and built-in tools when they own
  the needed capability.
- Add a plugin only for a concrete external system or capability that materially
  improves a named workflow.
- Keep this repository authoritative for cards, decisions, and policy. A plugin
  must not silently make an external tracker a competing source of truth.
- Grant the smallest practical read/write scope. External writes, messages,
  deployments, releases, and destructive actions remain explicitly gated.
- Never record credentials, tokens, connection identifiers, or private runtime
  state here.
- Record a consequential write-capable integration in an ADR before declaring
  it required.

Runtime availability is evidence to report during a task, not a versioned
project fact. Discover current marketplace choices at the point of need instead
of copying a changing marketplace catalog into this repository.

## Required plugins

None. The core harness is portable Markdown, YAML, and Python standard-library
validation.

## Approved optional plugins

None declared. Built-in capabilities and currently available plugins may be used
when a task calls for them, but that does not make them a project dependency.

## Declaration shape

When a plugin becomes a project capability, replace the empty marker above with
one entry per plugin:

```markdown
### Plugin name (`plugin-id@marketplace`)

- Status: required | approved optional
- Workflow and purpose:
- Data authority: repository | external system, with the exact boundary
- Allowed actions: read, write, or explicitly gated operations
- Required permissions:
- Fallback when unavailable:
- Decision: ADR link, or "Not required" for a low-risk optional capability
```

Do not include observed installation or connection status in the declaration.
