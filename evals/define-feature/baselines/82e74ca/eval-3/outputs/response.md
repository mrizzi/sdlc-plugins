This skill requires Project Configuration in your CLAUDE.md. Please run `/setup` first to configure your project, then re-run this skill.

Your CLAUDE.md is missing the `# Project Configuration` section, which must include:

1. **Repository Registry** -- a table with at least one entry
2. **Jira Configuration** -- with Project key, Cloud ID, and Feature issue type ID
3. **Code Intelligence** -- with the tool naming convention

Without this configuration, the skill cannot determine which Jira project to use or how to connect to your Jira instance. Run `/setup` to generate the required configuration, then re-run `/define-feature`.
