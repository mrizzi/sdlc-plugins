This skill requires Project Configuration in your CLAUDE.md. Please run `/setup` first to configure your project, then re-run this skill.

Your CLAUDE.md is missing the required `# Project Configuration` section, which must include:

- **Repository Registry** — a table with at least one entry
- **Jira Configuration** — containing Project key, Cloud ID, and Feature issue type ID
- **Code Intelligence** — with the tool naming convention

Without this configuration, the define-feature skill cannot proceed. Run `/setup` to generate the necessary configuration, then invoke `/sdlc-workflow:define-feature` again.
