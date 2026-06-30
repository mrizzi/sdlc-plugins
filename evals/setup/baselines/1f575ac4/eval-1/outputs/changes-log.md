# Changes Log

## Preserved (pre-existing content)

The following sections already existed in CLAUDE.md and were not modified:

- `# my-project` — project heading and description
- `## Documentation` — links to architecture.md and api.md
- `## Getting Started` — setup instructions (clone, npm install, npm start)

## Added (new sections)

The CLAUDE.md had no Project Configuration section. All of the following were added as new content:

1. **# Project Configuration** — top-level configuration heading
2. **## Repository Registry** — table with 2 entries (trustify-backend, trustify-ui), including Repository, Role, Serena Instance, and Path columns
3. **## Jira Configuration** — 5 fields: Project key, Cloud ID, Feature issue type ID, Git Pull Request custom field, GitHub Issue custom field
4. **## Code Intelligence** — documents the `mcp__<instance>__<tool>` naming convention with a concrete example using `serena_backend`, plus a Limitations subsection
5. **## Bug Configuration** — 3 fields: Bug issue type ID (10001), Bug template (docs/bug-template.md), Bug-to-Task link type (Blocks)

## Omitted

- **Security Configuration** — user declined to enable security triage, so this section was not added
- **Jira Field Defaults** — not configured in this session
- **Hierarchy Configuration** — not configured in this session
