**Project Configuration is missing from CLAUDE.md.**

The `define-feature` skill requires a `# Project Configuration` section in your project's CLAUDE.md file, including the following sub-sections:

- **Repository Registry** — lists the repositories involved and their roles
- **Jira Configuration** — provides the Jira project key, cloud ID, and custom field mappings
- **Code Intelligence** — describes any Serena MCP server instances for code navigation

Without this configuration, the skill cannot proceed.

Please run `/setup` first to generate the required Project Configuration section in your CLAUDE.md, then re-run `/define-feature`.
