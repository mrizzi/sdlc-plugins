# Changes Log

## Existing Content Preserved

The following sections from the original CLAUDE.md were preserved unchanged:

- `# my-project` heading and description
- `## Documentation` section (architecture.md, api.md links)
- `## Getting Started` section (clone, npm install, npm start steps)

## New Content Added

The entire `# Project Configuration` section was added, since no prior configuration existed. This includes:

### 1. Repository Registry (new)

Added a table with two repository entries:
- `trustify-backend` -- Rust backend service, Serena instance `serena_backend`, path `/home/user/trustify-backend`
- `trustify-ui` -- TypeScript frontend, Serena instance `serena_ui`, path `/home/user/trustify-ui`

### 2. Jira Configuration (new)

Added all five configuration fields:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### 3. Code Intelligence (new)

Added the standard tool naming convention explanation with `mcp__<instance>__<tool>` pattern, a concrete example using the `serena_backend` instance, and a `### Limitations` subsection noting no known limitations.

## Summary

- Sections preserved: 3 (project heading, Documentation, Getting Started)
- Sections added: 1 top-level (`# Project Configuration`) containing 3 subsections
- Sections modified: 0
- Sections removed: 0
