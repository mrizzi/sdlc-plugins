# Changes Log

## Preserved

- No existing Project Configuration section was present, so nothing was preserved.

## Added

- **Repository Registry** — New table with 2 entries:
  - `trustify-backend` (Rust backend service) mapped to Serena instance `serena_backend`
  - `trustify-ui` (TypeScript frontend) mapped to Serena instance `serena_ui`
- **Jira Configuration** — New section with project key, cloud ID, feature issue type ID, and custom field mappings for Git Pull Request and GitHub Issue.
- **Code Intelligence** — New section documenting the `mcp__<instance>__<tool>` naming convention, with a concrete example using `serena_backend`, and a Limitations subsection listing no known limitations for either instance.

## Not Added

- **Security Configuration** — User declined to enable security triage; section omitted.
