**Configuration missing — cannot proceed.**

I checked your project's CLAUDE.md and found that the `## Bug Configuration` section is missing under `# Project Configuration`. This section is required for the report-bug skill to function, as it provides the Bug issue type ID and the path to the bug description template.

Your CLAUDE.md has `## Jira Configuration` and `## Repository Registry`, but without `## Bug Configuration` I cannot determine the issue type or template to use.

> This skill requires Bug Configuration in your CLAUDE.md. Please run `/setup` first to configure your project, then re-run this skill.
