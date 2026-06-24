# Discovery Log

## Step 1 -- Read Existing Configuration

Read CLAUDE.md from `evals/setup/files/claude-md-configured-with-security.md`.

Existing configuration found:

- `# Project Configuration` heading: **present**
- `## Repository Registry` table:
  - `backend` -- Rust backend service, Serena instance `serena_backend`, path `/home/user/backend`
  - `frontend-ui` -- TypeScript frontend, Serena instance `serena_ui`, path `/home/user/frontend-ui`
- `## Jira Configuration`:
  - Project key: TC -- **present**
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432 -- **present**
  - Feature issue type ID: 10142 -- **present**
  - Git Pull Request custom field: customfield_10875 -- **present**
  - GitHub Issue custom field: customfield_10747 -- **present**
- `### Jira Field Defaults`: **not present**
- `## Code Intelligence`: **present**, documents `mcp__<instance>__<tool>` convention with example using `serena_backend`
  - `### Limitations`:
    - `serena_backend`: rust-analyzer may take 30-60 seconds to index on first use
    - `serena_ui`: No known limitations
- `## Bug Configuration`: **present**
  - Bug issue type ID: 10001
  - Bug template: docs/bug-template.md
  - Bug-to-Task link type: Blocks
- `## Security Configuration`: **present**
  - `### Product Lifecycle`: **fully populated**
    - Product pages URL: https://access.example.com/product-lifecycle
    - Jira version prefix: MYPRODUCT
    - Vulnerability issue type ID: 10200
    - Component label pattern: pscomponent:
    - VEX Justification custom field: customfield_12345
  - `### Version Streams`: **present** with 1 row (2.1.x)
  - `### Source Repositories`: **present** with 2 rows (backend, frontend-ui)
- `## Hierarchy Configuration`: **not present**

## Step 2 -- Discover Serena Instances

Examined available MCP tools from `evals/setup/files/mcp-tools-with-serena.md`.

Discovered Serena instances:
- `serena_backend` -- tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir
- `serena_ui` -- tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir

Both `serena_backend` and `serena_ui` are already in the Repository Registry.

Result: **Repository Registry is up to date**.

## Step 3 -- Jira Configuration

All three required fields are already populated:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142

Result: **Jira Configuration is up to date**.

## Step 3.5 -- Hierarchy Preferences

`## Hierarchy Configuration` does not exist in the current CLAUDE.md. However, discovery of Jira issue type hierarchy requires calling MCP tools or the REST API, which is not permitted in this eval run. This section would need to be configured in a live session.

Result: **Hierarchy Configuration not present -- requires interactive discovery (skipped in eval mode)**.

## Step 4 -- Jira Field Defaults

`### Jira Field Defaults` does not exist under `## Jira Configuration`. Discovery of available priorities and fixVersions requires calling MCP tools or the REST API, which is not permitted in this eval run. This subsection would need to be configured in a live session.

Result: **Jira Field Defaults not present -- requires interactive discovery (skipped in eval mode)**.

## Step 5 -- Code Intelligence

`## Code Intelligence` already exists and covers both Serena instances from the Repository Registry (`serena_backend` and `serena_ui`).

Result: **Code Intelligence is up to date**.

## Step 7 -- Constraints Template

Not checked -- eval mode does not permit filesystem operations outside outputs/.

## Step 8 -- CONVENTIONS.md Scaffold

Not checked -- eval mode does not permit filesystem operations outside outputs/.

## Step 9 -- Bug Configuration

`## Bug Configuration` already exists with all three required fields populated:
- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

No `{{placeholder}}` markers found.

Result: **Bug Configuration is up to date**.

## Step 10 -- Security Configuration

`## Security Configuration` already exists with all required fields fully populated:

### Product Lifecycle
- Product pages URL: https://access.example.com/product-lifecycle -- **present**
- Jira version prefix: MYPRODUCT -- **present**
- Vulnerability issue type ID: 10200 -- **present**
- Component label pattern: pscomponent: -- **present**
- VEX Justification custom field: customfield_12345 -- **present** (optional)

### Version Streams
- 1 row present (2.1.x) -- **populated**

### Source Repositories
- 2 rows present (backend, frontend-ui) -- **populated**

No `{{placeholder}}` markers found in any Security Configuration subsection.

Result: **Security Configuration is up to date**.

## Summary

| Section | Status |
|---|---|
| Repository Registry | Up to date |
| Jira Configuration | Up to date |
| Jira Field Defaults | Not present (requires interactive discovery) |
| Hierarchy Configuration | Not present (requires interactive discovery) |
| Code Intelligence | Up to date |
| Bug Configuration | Up to date |
| Security Configuration | Up to date |
