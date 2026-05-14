# Changes Log

This is a greenfield setup -- all Project Configuration sections are newly added.

## Added

- **# Project Configuration** -- top-level configuration section
- **## Repository Registry** -- table with 2 entries:
  - trustify-backend (Rust backend service, serena_backend, /home/user/trustify-backend)
  - trustify-ui (TypeScript frontend, serena_ui, /home/user/trustify-ui)
- **## Jira Configuration** -- 5 fields:
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Feature issue type ID: 10142
  - Git Pull Request custom field: customfield_10875
  - GitHub Issue custom field: customfield_10747
- **## Code Intelligence** -- with MCP tool naming convention (`mcp__<instance>__<tool>`) and usage example
- **### Limitations** -- no known limitations for either Serena instance

## Preserved

- Non-configuration content from existing CLAUDE.md:
  - `# my-project` heading and description
  - `## Documentation` section with architecture and API links
  - `## Getting Started` section with setup instructions

## Removed

Nothing.

## Modified

Nothing.
