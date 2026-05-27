This skill requires Project Configuration in your CLAUDE.md. Please run `/setup` first to configure your project, then re-run this skill.

Your CLAUDE.md is missing the following required sections under `# Project Configuration`:

1. **Repository Registry** — must contain a table with at least one entry
2. **Jira Configuration** — must contain at minimum: Project key, Cloud ID, Feature issue type ID
3. **Code Intelligence** — must exist with the tool naming convention

Without these sections, the define-feature skill cannot determine the Jira project key, Cloud ID, or Feature issue type ID needed to create a Feature issue.
