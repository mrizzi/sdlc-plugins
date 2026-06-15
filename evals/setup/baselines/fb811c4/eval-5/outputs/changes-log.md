# Changes Log

## Sections Added

All sections were newly added (no existing Project Configuration was present in the CLAUDE.md).

### 1. `# Project Configuration` (new)

Top-level heading added to contain all project-specific configuration.

### 2. `## Repository Registry` (new)

Added table with 2 rows:
- **backend** -- Rust backend service, Serena instance `serena_backend`, path `/home/user/backend`
- **frontend-ui** -- TypeScript frontend, Serena instance `serena_ui`, path `/home/user/frontend-ui`

### 3. `## Jira Configuration` (new)

Added 5 configuration fields:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### 4. `## Code Intelligence` (new)

Added tool naming convention documentation with example using `serena_backend`. Added `### Limitations` subsection noting no known limitations for either instance.

### 5. `## Security Configuration` (new)

Added complete Security Configuration section with three subsections:

- **### Product Lifecycle** -- 5 fields: Product pages URL, Jira version prefix, Vulnerability issue type ID, Component label pattern, VEX Justification custom field
- **### Version Streams** -- 1 row: stream 2.1.x with Konflux release repo, local path, and security matrix path
- **### Source Repositories** -- 2 rows: backend and frontend-ui with their GitHub URLs

## Sections Preserved

The existing CLAUDE.md content (project heading and description) was not modified. The `# Project Configuration` section was appended as a new top-level section.
