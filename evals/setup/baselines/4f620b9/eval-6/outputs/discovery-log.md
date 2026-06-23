# Discovery Log

## Step 1 – Read Existing Configuration

Read existing CLAUDE.md from `evals/setup/files/claude-md-configured-with-security.md`.

Parsed existing configuration:

- **`# Project Configuration`** heading: present
- **`## Repository Registry`** table: present
  - `backend` — Rust backend service — Serena instance: `serena_backend` — Path: `/home/user/backend`
  - `frontend-ui` — TypeScript frontend — Serena instance: `serena_ui` — Path: `/home/user/frontend-ui`
- **`## Jira Configuration`**: present, all fields populated
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Feature issue type ID: 10142
  - Git Pull Request custom field: customfield_10875
  - GitHub Issue custom field: customfield_10747
- **`## Code Intelligence`**: present, documents `mcp__<instance>__<tool>` convention
  - Covers `serena_backend` and `serena_ui`
  - `### Limitations` subheading present with entries for both instances
- **`## Bug Configuration`**: present, all three required fields populated
  - Bug issue type ID: 10001
  - Bug template: docs/bug-template.md
  - Bug-to-Task link type: Blocks
- **`## Security Configuration`**: present, fully populated (no `{{placeholder}}` markers)
  - `### Product Lifecycle`: all required fields populated, VEX Justification custom field populated
  - `### Version Streams`: 1 row (2.1.x stream)
  - `### Source Repositories`: 2 rows (backend, frontend-ui)
- **`## Hierarchy Configuration`**: NOT present

## Step 2 – Discover Serena Instances

Examined available MCP tools from `evals/setup/files/mcp-tools-with-serena.md`.

Discovered Serena instances (by `mcp__<instance>__<tool>` naming pattern):

1. **`serena_backend`** — tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir
2. **`serena_ui`** — tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir

Both `serena_backend` and `serena_ui` are already in the Repository Registry.

Result: **Repository Registry is up to date.**

## Step 3 – Jira Configuration

All required fields (Project key, Cloud ID, Feature issue type ID) are already populated. Optional fields (Git Pull Request custom field, GitHub Issue custom field) are also populated.

Result: **Jira Configuration is up to date.**

## Step 3.5 – Hierarchy Preferences

`## Hierarchy Configuration` does NOT exist in the current CLAUDE.md.

Discovery of issue type hierarchy requires Atlassian MCP or REST API access. The available MCP tools include `mcp__atlassian__` prefixed tools, but actual MCP calls are not permitted in this eval run. Hierarchy Configuration cannot be auto-discovered without calling MCP tools.

Result: **Hierarchy Configuration skipped** — cannot discover issue type hierarchy without calling MCP tools. This section can be added by re-running `/setup` with MCP access enabled.

## Step 4 – Code Intelligence

The `## Code Intelligence` section exists and covers both Serena instances (`serena_backend`, `serena_ui`) from the Repository Registry. The `### Limitations` subheading is present with entries for both instances.

Result: **Code Intelligence is up to date.**

## Step 5 – Write Configuration

All existing sections are up to date. The only missing section is `## Hierarchy Configuration`, which cannot be populated without MCP tool access.

Result: **No changes written** — existing configuration preserved.

## Step 6 – Copy Constraints Template

Cannot check target project filesystem in this eval. Skipped.

## Step 7 – Scaffold CONVENTIONS.md

Cannot check target project filesystem in this eval. Skipped.

## Step 8 – Bug Configuration

All three required fields are populated (Bug issue type ID: 10001, Bug template: docs/bug-template.md, Bug-to-Task link type: Blocks). No `{{placeholder}}` markers found.

Result: **Bug Configuration is up to date.**

## Step 9 – Security Configuration

`## Security Configuration` exists and is fully populated with no `{{placeholder}}` markers:

- **Product Lifecycle**: All required fields populated (Product pages URL, Jira version prefix, Vulnerability issue type ID, Component label pattern). Optional VEX Justification custom field is also populated.
- **Version Streams**: 1 row present (2.1.x stream with Konflux release repo, local path, and security matrix path).
- **Source Repositories**: 2 rows present (backend, frontend-ui with URLs).

Result: **Security Configuration is up to date.**

## Step 10 – Validate

| Check | Status |
|---|---|
| `# Project Configuration` heading exists | PASS |
| `## Repository Registry` has correct table columns | PASS |
| `## Jira Configuration` has required fields | PASS |
| `## Code Intelligence` documents naming convention | PASS |
| `## Code Intelligence` has `### Limitations` | PASS |
| `## Bug Configuration` has required fields | PASS |
| `## Security Configuration` / `### Product Lifecycle` | PASS |
| `## Security Configuration` / `### Version Streams` | PASS |
| `## Security Configuration` / `### Source Repositories` | PASS |
| `## Hierarchy Configuration` | SKIPPED — requires MCP access |

**Overall: Project Configuration is up to date — no changes needed** (except Hierarchy Configuration which requires MCP tool access to discover).
