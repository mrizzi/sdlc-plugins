This skill requires Project Configuration in your CLAUDE.md. Please run `/setup` first to configure your project, then re-run this skill.

The project's CLAUDE.md is missing the required `# Project Configuration` section. Specifically, the following required subsections were not found:

1. **Repository Registry** — not present
2. **Jira Configuration** — not present (must contain Project key, Cloud ID, and Feature issue type ID)
3. **Code Intelligence** — not present

Without these configuration sections, the define-feature skill cannot determine the Jira project key, Cloud ID, or Feature issue type ID needed to create a Feature issue.

Please run `/setup` to configure your project, which will add the necessary Project Configuration section to your CLAUDE.md, then re-run `/sdlc-workflow:define-feature`.
