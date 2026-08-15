# Security policy

## Supported versions

{{SUPPORTED_VERSIONS}}

## Reporting a vulnerability

Report vulnerabilities privately through `{{SECURITY_CONTACT}}`. Do not open a
public ticket containing exploit details, credentials, private data, or unsafe
reproduction material.

Include the affected version or commit, environment, impact, and minimal safe
reproduction steps. Coordinate disclosure and remediation before publishing
details.

## Engineering boundaries

- Treat files, network responses, user input, archives, and dependency output as
  untrusted at their boundary.
- Apply least privilege to filesystem, process, network, credential, and data
  access.
- Keep secrets out of source, logs, fixtures, screenshots, generated artifacts,
  and error messages.
- Fail closed when authorization or data integrity is uncertain; preserve
  recoverable state for destructive workflows.
- Review dependency advisories and transitive or native supply-chain impact.
- Test important authorization, validation, data-exposure, and failure paths.

Security-sensitive changes require focused review and an entry under the
changelog's Security section when users need to act.
