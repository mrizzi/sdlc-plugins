# Setup Discovery Log

## Step 1 -- Read Existing Configuration

- Read `claude-md-empty.md` as the existing CLAUDE.md.
- No `# Project Configuration` section found -- all sections need to be created.

## Step 2 -- Discover Serena Instances

- Scanned available MCP tools for Serena instances.
- Discovered 2 Serena instances:
  - `serena_backend` -- tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir
  - `serena_ui` -- tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir
- User provided repository details:
  - serena_backend: repository name = "backend", role = "Rust backend service", path = "/home/user/backend"
  - serena_ui: repository name = "frontend-ui", role = "TypeScript frontend", path = "/home/user/frontend-ui"

## Step 3 -- Jira Configuration

- Atlassian MCP tools detected (mcp__atlassian__*).
- User provided Jira configuration fields:
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Feature issue type ID: 10142
  - Git Pull Request custom field: customfield_10875
  - GitHub Issue custom field: customfield_10747

## Step 5 -- Code Intelligence

- Generated Code Intelligence section for 2 Serena instances.
- Used `serena_backend` as the example instance in documentation.
- User reported no known limitations for either instance.

## Step 9 -- Bug Configuration

- Bug Configuration section does not exist -- scaffolding all fields.
- Bug issue type ID discovered from Jira metadata: 10001
- User accepted default bug template path: docs/bug-template.md
- User accepted default Bug-to-Task link type: Blocks
- Bug template file copy skipped (simulation mode).

## Step 10 -- Security Configuration

- Security Configuration section does not exist.
- User accepted when asked whether to enable security triage -- opted in.
- Product Lifecycle fields collected:
  - Product pages URL: https://access.example.com/product-lifecycle
  - Jira version prefix: MYPRODUCT
  - Vulnerability issue type ID: 10200
  - Component label pattern: pscomponent:
  - VEX Justification custom field: customfield_12345
- Version Streams collected (1 stream):
  - 2.1.x: Konflux release repo = git.downstream.example.com/my-org/product-release.2.1.z, local path = /home/user/product-release.2.1.z, security matrix path = security-matrix.md
- Source Repositories collected (2 repos):
  - backend: https://github.com/example/backend
  - frontend-ui: https://github.com/example/frontend-ui
- User declined optional supportability matrix population.
- User skipped security-matrix.md scaffolding.

## Validation

- `# Project Configuration` heading: present
- `## Repository Registry` table: present with 2 rows (backend, frontend-ui)
- `## Jira Configuration`: present with all required fields (Project key, Cloud ID, Feature issue type ID) plus optional fields
- `## Code Intelligence`: present with mcp__<instance>__<tool> naming convention documented
- `### Limitations`: present under Code Intelligence
- `## Bug Configuration`: present with Bug issue type ID, Bug template path, Bug-to-Task link type
- `## Security Configuration`: present with Product Lifecycle, Version Streams, and Source Repositories subsections
- All sections validated successfully.
