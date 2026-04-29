# Changes Log

## Existing CLAUDE.md Content

The existing CLAUDE.md (`claude-md-empty.md`) contained no Project Configuration section. It had the following sections which were preserved as-is:

- `# my-project` — project title and description
- `## Documentation` — links to architecture and API docs
- `## Getting Started` — setup instructions

## Added Sections

All Project Configuration content is new (greenfield setup):

1. **`# Project Configuration`** — new top-level section added.
2. **`## Repository Registry`** — new table with 2 entries (trustify-backend, trustify-ui) mapped to their Serena instances, roles, and paths.
3. **`## Jira Configuration`** — new section with 5 configuration values (project key, cloud ID, feature issue type ID, Git PR custom field, GitHub Issue custom field).
4. **`## Code Intelligence`** — new section documenting the Serena tool naming convention (`mcp__<instance>__<tool>`) with a concrete example using `serena_backend`.
5. **`### Limitations`** — new subsection noting no known limitations for either Serena instance.

## Preserved Content

All original CLAUDE.md content (project description, documentation links, getting started instructions) was preserved without modification.
