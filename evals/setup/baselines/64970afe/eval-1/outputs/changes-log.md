# Changes Log

## Summary

All sections were newly created. The existing CLAUDE.md had no `# Project Configuration` section, so the entire configuration block was generated from scratch.

## Preserved Content

- Project title (`# my-project`) — preserved, not modified
- `## Documentation` section — preserved, not modified
- `## Getting Started` section — preserved, not modified

## Added Sections

### 1. `# Project Configuration` (new)

Top-level heading added to contain all configuration subsections.

### 2. `## Repository Registry` (new)

Added table with 2 repositories:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend |
| trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui |

### 3. `## Jira Configuration` (new)

Added with all 5 fields:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

Note: `### Jira Field Defaults` subsection was NOT added — MCP was unavailable for priority/fixVersion discovery and no user input was provided.

### 4. `## Code Intelligence` (new)

Added with:
- Tool naming convention explanation (`mcp__<instance>__<tool>`)
- Concrete example using `serena_backend` instance
- `### Limitations` subheading — no limitations known for either instance

### 5. `## Bug Configuration` (new)

Added with all 3 fields:
- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

### 6. `## Hierarchy Configuration` (new)

Added with:
- Default epic grouping strategy: by-sub-feature

## Skipped Sections

### `## Security Configuration`

Not created — user declined to enable security triage for this project.

### `### Jira Field Defaults`

Not created — MCP unavailable for auto-discovery; no manual input provided.

## File Operations Skipped (Simulation)

- `docs/constraints.md` — would be created from constraints.template.md
- `docs/bug-template.md` — would be created from bug-template.md template
- `CONVENTIONS.md` in trustify-backend — would be offered for scaffolding
- `CONVENTIONS.md` in trustify-ui — would be offered for scaffolding
