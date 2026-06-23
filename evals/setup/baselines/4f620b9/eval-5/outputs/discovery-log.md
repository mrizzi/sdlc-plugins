# Setup Discovery Log

## Step 1 -- Read Existing Configuration

- Read CLAUDE.md from `evals/setup/files/claude-md-empty.md`
- No `# Project Configuration` section found -- full setup required
- No Repository Registry, Jira Configuration, Code Intelligence, Bug Configuration, Security Configuration, or Hierarchy Configuration sections exist

## Step 2 -- Discover Serena Instances

- Examined available MCP tools from `evals/setup/files/mcp-tools-with-serena.md`
- Discovered 2 Serena instances:
  - `serena_backend` -- tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir
  - `serena_ui` -- tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir
- User provided repository details:
  - serena_backend: repository name = `backend`, role = `Rust backend service`, path = `/home/user/backend`
  - serena_ui: repository name = `frontend-ui`, role = `TypeScript frontend`, path = `/home/user/frontend-ui`

## Step 3 -- Jira Configuration

- Atlassian MCP detected: tools prefixed with `mcp__atlassian__` found
- User provided configuration values:
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Feature issue type ID: 10142
  - Git Pull Request custom field: customfield_10875
  - GitHub Issue custom field: customfield_10747

## Step 3.5 -- Hierarchy Configuration

- User selected default epic grouping strategy: `by-sub-feature`

## Step 4 -- Code Intelligence

- Generated Code Intelligence section for 2 Serena instances
- Example uses `serena_backend` as the primary instance
- User reported no known limitations for either instance

## Step 6 -- Constraints Template

- Simulation mode: skipped file copy of `docs/constraints.md`

## Step 7 -- CONVENTIONS.md Scaffolding

- Simulation mode: skipped CONVENTIONS.md scaffolding for both repositories

## Step 8 -- Bug Configuration

- Bug issue type ID discovered from Jira metadata: 10001
- User accepted default bug template path: `docs/bug-template.md`
- User accepted default Bug-to-Task link type: `Blocks`
- Simulation mode: skipped bug template file copy

## Step 9 -- Security Configuration

- User accepted security triage enablement
- Product Lifecycle fields collected:
  - Product pages URL: https://access.example.com/product-lifecycle
  - Jira version prefix: MYPRODUCT
  - Vulnerability issue type ID: 10200
  - Component label pattern: pscomponent:
  - VEX Justification custom field: customfield_12345
  - Upstream Affected Component custom field: (skipped)
  - PS Component custom field: (skipped)
  - Stream custom field: (skipped)
- Version Streams collected (1 stream):
  - 2.1.x: Konflux release repo = git.downstream.example.com/my-org/product-release.2.1.z, local path = /home/user/product-release.2.1.z, security matrix path = security-matrix.md
- Source Repositories collected (2 repos):
  - backend: https://github.com/example/backend
  - frontend-ui: https://github.com/example/frontend-ui
- User declined supportability matrix population
- User skipped security-matrix.md scaffolding

## Step 10 -- Validation

- `# Project Configuration` heading: present
- `## Repository Registry` table with correct columns: present (2 rows)
- `## Jira Configuration` with required fields: present (Project key, Cloud ID, Feature issue type ID)
- `## Code Intelligence` with mcp naming convention: present
- `## Code Intelligence` with `### Limitations` subheading: present
- `## Bug Configuration` with required fields: present (Bug issue type ID, Bug template, Bug-to-Task link type)
- `## Security Configuration` with `### Product Lifecycle`: present (all required fields populated)
- `## Security Configuration` with `### Version Streams`: present (1 row)
- `## Security Configuration` with `### Source Repositories`: present (2 rows)
- `## Hierarchy Configuration` with default epic grouping strategy: present
- Constraints document: skipped (simulation mode)
- Bug template file: skipped (simulation mode)

All validation checks passed.
