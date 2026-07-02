This skill requires Project Configuration in your CLAUDE.md. Please run `/setup` first to configure your project, then re-run this skill.

Specifically, the following required sections under `# Project Configuration` are missing from your CLAUDE.md:

- **Repository Registry** -- must contain a table with at least one entry
- **Jira Configuration** -- must contain at minimum: Project key, Cloud ID, Feature issue type ID
- **Code Intelligence** -- must exist with the tool naming convention

Run `/setup` to generate the Project Configuration section, then re-run `/define-feature`.
