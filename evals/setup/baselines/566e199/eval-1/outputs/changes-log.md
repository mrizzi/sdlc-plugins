# Changes Log

## Preserved (Existing Content)

The following sections from the original CLAUDE.md were preserved unchanged:

- **`# my-project`** — project title and description
- **`## Documentation`** — documentation links (architecture.md, api.md)
- **`## Getting Started`** — setup instructions (clone, npm install, npm start)

## Added (New Content)

The following sections were added as a new `# Project Configuration` block appended to the end of the existing CLAUDE.md:

### Repository Registry

New section with a table mapping two repositories to their Serena instances:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend |
| trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui |

### Jira Configuration

New section with five configuration fields:

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### Code Intelligence

New section documenting the Serena tool naming convention (`mcp__<instance>__<tool>`) with a usage example using `serena_backend`.

### Limitations

New subsection noting no known limitations for either Serena instance.

## Summary

- Sections preserved: 3 (title/description, Documentation, Getting Started)
- Sections added: 4 (Repository Registry, Jira Configuration, Code Intelligence, Limitations)
- Sections modified: 0
- Sections removed: 0
