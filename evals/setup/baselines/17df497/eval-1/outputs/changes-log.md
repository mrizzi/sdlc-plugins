# Changes Log

## Existing Content (Preserved)

The following sections from the original CLAUDE.md were preserved without modification:

- `# my-project` — project heading and description
- `## Documentation` — documentation links section
- `## Getting Started` — getting started instructions

## Added Content

The following sections were added as a new `# Project Configuration` block appended to the end of the file:

### Repository Registry (new)

Added 2 repository entries:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend |
| trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui |

### Jira Configuration (new)

Added Jira configuration with all five fields:

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### Code Intelligence (new)

Added Code Intelligence section with:

- Tool naming convention explanation (`mcp__<instance>__<tool>`)
- Example usage with `serena_backend` instance
- Limitations subsection noting no known limitations

## Removed Content

Nothing was removed. The setup skill is incremental and never removes existing entries.
