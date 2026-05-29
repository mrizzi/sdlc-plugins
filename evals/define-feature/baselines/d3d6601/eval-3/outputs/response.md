This skill requires Project Configuration in your CLAUDE.md. Please run `/setup` first to configure your project, then re-run this skill.

The following required sections are missing from your CLAUDE.md:

1. **Repository Registry** -- no `## Repository Registry` section found under `# Project Configuration`
2. **Jira Configuration** -- no `## Jira Configuration` section found (Project key, Cloud ID, and Feature issue type ID are required)
3. **Code Intelligence** -- no `## Code Intelligence` section found

Without these configuration sections, the define-feature skill cannot determine which Jira project to create the Feature in, what issue type to use, or which cloud instance to target. Please run `/setup` to initialize your project configuration, then re-run `/sdlc-workflow:define-feature`.
