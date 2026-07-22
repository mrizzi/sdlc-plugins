# Changes Log

## Existing Content Preserved

- `# my-project` heading and description retained.
- `## Documentation` section retained (links to architecture.md and api.md).
- `## Getting Started` section retained (clone, npm install, npm start instructions).

## Newly Added Sections

### `# Project Configuration` (new)

Appended to end of CLAUDE.md since no Project Configuration section existed.

### `## Repository Registry` (new)

Added table with 2 repositories discovered from Serena instances:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| backend | Rust backend service | serena_backend | /home/user/backend |
| frontend-ui | TypeScript frontend | serena_ui | /home/user/frontend-ui |

### `## Jira Configuration` (new)

Added with 5 fields provided by user:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### `## Code Intelligence` (new)

Added with:
- Tool naming convention (`mcp__<instance>__<tool>`)
- Example using `serena_backend` instance
- `### Limitations` subsection noting no known limitations

### `## Bug Configuration` (new)

Added with 3 fields:
- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

### `## Security Configuration` (new)

Added with the following subsections:

#### `### Product Lifecycle`
- Product pages URL: https://access.example.com/product-lifecycle
- Jira version prefix: MYPRODUCT
- Vulnerability issue type ID: 10200
- Component label pattern: pscomponent:
- VEX Justification custom field: customfield_12345
- Optional fields left blank: Upstream Affected Component, PS Component, Stream, ProdSec contact email, ProdSec Jira account ID, Embargo policy URL

#### `### Version Streams`
- 1 stream: 2.1.x with Konflux release repo, local path, and security matrix path

#### `### Source Repositories`
- 2 repositories: backend and frontend-ui (both upstream deployment context)

## Not Modified

- No existing content was removed or overwritten.
- Bug template file copy was skipped (simulation mode).
- Supportability matrix population was declined by user.
- security-matrix.md scaffolding was skipped by user.
- Jira Field Defaults and Hierarchy Configuration were not configured (no discovery data available in simulation).
