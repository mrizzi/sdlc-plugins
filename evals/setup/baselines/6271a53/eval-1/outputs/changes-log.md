# Changes Log

## What was preserved

- The existing CLAUDE.md content (project heading, Documentation section, Getting Started section) was not modified. The Project Configuration section is generated as a new addition.

## What was added

The following sections were added as the new Project Configuration block:

1. **Repository Registry** -- new table with 2 rows:
   - `trustify-backend` (Rust backend service, Serena instance `serena_backend`, path `/home/user/trustify-backend`)
   - `trustify-ui` (TypeScript frontend, Serena instance `serena_ui`, path `/home/user/trustify-ui`)

2. **Jira Configuration** -- new section with 5 fields:
   - Project key: TC
   - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
   - Feature issue type ID: 10142
   - Git Pull Request custom field: customfield_10875
   - GitHub Issue custom field: customfield_10747

3. **Code Intelligence** -- new section documenting the `mcp__<instance>__<tool>` naming convention with usage examples for both `serena_backend` and `serena_ui`.

4. **Limitations** (subsection of Code Intelligence) -- added with a note that no limitations are known for either Serena instance.
