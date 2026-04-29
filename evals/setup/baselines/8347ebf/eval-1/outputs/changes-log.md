# Changes Log

## Summary

This is a greenfield setup. No existing Project Configuration section was found in CLAUDE.md. All content below is newly added.

## Preserved Content

- Existing CLAUDE.md content (project title, documentation links, getting started section) is preserved as-is. The new `# Project Configuration` section is appended after the existing content.

## Added Content

### Section: `# Project Configuration`

New top-level section created.

### Subsection: `## Repository Registry`

Added repository registry table with 2 entries:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend |
| trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui |

### Subsection: `## Jira Configuration`

Added Jira configuration with 5 fields:

- Project key: TC (added)
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432 (added)
- Feature issue type ID: 10142 (added)
- Git Pull Request custom field: customfield_10875 (added)
- GitHub Issue custom field: customfield_10747 (added)

### Subsection: `## Code Intelligence`

Added Code Intelligence section with:

- Tool naming convention documentation (`mcp__<instance>__<tool>`)
- Example using `serena_backend` instance
- Limitations subsection noting no known limitations for either instance
