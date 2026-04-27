This skill requires Project Configuration in your CLAUDE.md. Please run `/setup` first to configure your project, then re-run this skill.

Your CLAUDE.md is missing the required `# Project Configuration` section. Specifically, the following subsections were not found:

- `## Repository Registry` -- must contain a table with at least one entry
- `## Jira Configuration` -- must contain at minimum: Project key, Cloud ID, Feature issue type ID
- `## Code Intelligence` -- must exist with the tool naming convention

Run `/setup` to generate these sections, then invoke `/sdlc-workflow:define-feature` again.
