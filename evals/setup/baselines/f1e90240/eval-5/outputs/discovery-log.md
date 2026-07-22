# Discovery Log

## Step 1 -- Read Existing Configuration

- Read `CLAUDE.md` (claude-md-empty.md): file exists but contains no `# Project Configuration` section.
- All sections need to be created from scratch.

## Step 2 -- Discover Serena Instances

- Scanned available MCP tools for Serena naming pattern `mcp__<instance>__<tool>`.
- Discovered 2 Serena instances:
  - `serena_backend` -- tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir
  - `serena_ui` -- tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir
- User provided repository details:
  - `serena_backend` -> repository: backend, role: Rust backend service, path: /home/user/backend
  - `serena_ui` -> repository: frontend-ui, role: TypeScript frontend, path: /home/user/frontend-ui

## Step 3 -- Jira Configuration

- Atlassian MCP tools detected (prefixed with `mcp__atlassian__`).
- User provided Jira configuration fields:
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Feature issue type ID: 10142
  - Git Pull Request custom field: customfield_10875
  - GitHub Issue custom field: customfield_10747

## Step 5 -- Code Intelligence

- Generated Code Intelligence section documenting the `mcp__<instance>__<tool>` naming convention.
- Used `serena_backend` as the example instance.
- User confirmed no known limitations for either Serena instance.

## Step 9 -- Bug Configuration

- Bug issue type ID discovered from Jira metadata: 10001
- User accepted default bug template path: docs/bug-template.md
- User accepted default Bug-to-Task link type: Blocks
- Bug template file copy skipped (simulation mode).

## Step 10 -- Security Configuration

- User accepted opt-in to enable security triage for this project.
- Product Lifecycle fields collected from user:
  - Product pages URL: https://access.example.com/product-lifecycle
  - Jira version prefix: MYPRODUCT
  - Vulnerability issue type ID: 10200
  - Component label pattern: pscomponent:
  - VEX Justification custom field: customfield_12345
  - Optional fields (Upstream Affected Component, PS Component, Stream, ProdSec contact email, ProdSec Jira account ID, Embargo policy URL): skipped by user
- Version Streams collected:
  - 2.1.x: Konflux release repo at git.downstream.example.com/my-org/product-release.2.1.z, local path /home/user/product-release.2.1.z, security matrix at security-matrix.md
- Source Repositories collected:
  - backend: https://github.com/example/backend (deployment context: upstream)
  - frontend-ui: https://github.com/example/frontend-ui (deployment context: upstream)
- User declined supportability matrix population.
- security-matrix.md scaffolding skipped by user.
