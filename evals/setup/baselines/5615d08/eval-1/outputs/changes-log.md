# Changes Log

## Preserved (from existing CLAUDE.md)

The existing CLAUDE.md content was not modified. It contained:

- `# my-project` heading and project description
- `## Documentation` section with architecture and API links
- `## Getting Started` section with setup instructions

These sections remain unchanged; the Project Configuration section is generated as a new addition.

## Added (new Project Configuration section)

The following sections were added as the new `# Project Configuration` block:

### Repository Registry

- Added table with 2 repository entries:
  - `trustify-backend` (Rust backend service) mapped to Serena instance `serena_backend` at `/home/user/trustify-backend`
  - `trustify-ui` (TypeScript frontend) mapped to Serena instance `serena_ui` at `/home/user/trustify-ui`

### Jira Configuration

- Added Jira project settings with 5 fields:
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Feature issue type ID: 10142
  - Git Pull Request custom field: customfield_10875
  - GitHub Issue custom field: customfield_10747

### Code Intelligence

- Added tool naming convention explanation (`mcp__<instance>__<tool>`)
- Added usage examples for both `serena_backend` and `serena_ui` instances using `find_symbol`

### Limitations

- Added Limitations subsection noting no known limitations for either Serena instance
