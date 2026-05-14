This skill requires Project Configuration in your CLAUDE.md. Please run `/setup` first to configure your project, then re-run this skill.

Your CLAUDE.md is missing the required `# Project Configuration` section, which must include:

1. **Repository Registry** — a table with at least one entry
2. **Jira Configuration** — containing Project key, Cloud ID, and Feature issue type ID
3. **Code Intelligence** — with the tool naming convention

Without this configuration, the skill cannot determine the Jira project key, cloud ID, or issue type needed to create a Feature issue. Run `/setup` to generate this configuration, then re-run `/sdlc-workflow:define-feature`.
