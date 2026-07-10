# Setup Discovery Log

## Step 1 — Read Existing Configuration

- Read CLAUDE.md: file exists, no `# Project Configuration` section found.
- All sections need to be created from scratch.

## Step 2 — Discover Serena Instances

- Scanned available MCP tools for Serena instances.
- Discovered 2 Serena instances:
  - `serena_backend` — tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir
  - `serena_ui` — tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir
- User provided repository details:
  - serena_backend: repository 'backend', role 'Rust backend service', path '/home/user/backend'
  - serena_ui: repository 'frontend-ui', role 'TypeScript frontend', path '/home/user/frontend-ui'

## Step 3 — Jira Configuration

- Atlassian MCP tools detected (mcp__atlassian__* prefix).
- User provided Jira configuration manually:
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Feature issue type ID: 10142
  - Git Pull Request custom field: customfield_10875
  - GitHub Issue custom field: customfield_10747

## Step 5 — Code Intelligence

- Generated Code Intelligence section with naming convention and example using serena_backend.
- User reported no known limitations for either Serena instance.

## Step 9 — Bug Configuration

- Bug issue type ID discovered from Jira metadata: 10001
- User accepted default bug template path: docs/bug-template.md
- User accepted default Bug-to-Task link type: Blocks
- Bug template file copy skipped (simulation mode).

## Step 10 — Security Configuration

- User was asked whether to enable security triage: accepted.
- Security Configuration was opted in and fields were collected.

### Product Lifecycle fields collected:
  - Product pages URL: https://access.example.com/product-lifecycle
  - Jira version prefix: MYPRODUCT
  - Vulnerability issue type ID: 10200
  - Component label pattern: pscomponent:
  - VEX Justification custom field: customfield_12345
  - Optional fields (Upstream Affected Component, PS Component, Stream, ProdSec contact email, ProdSec Jira account ID, Embargo policy URL): skipped by user.

### Version Streams collected:
  - Stream 2.1.x: Konflux release repo git.downstream.example.com/my-org/product-release.2.1.z, local path /home/user/product-release.2.1.z, security matrix path security-matrix.md

### Source Repositories collected:
  - backend: https://github.com/example/backend (deployment context: upstream)
  - frontend-ui: https://github.com/example/frontend-ui (deployment context: upstream)

### Supportability Matrix:
  - User declined optional supportability matrix population.

### Security Matrix Scaffolding:
  - User skipped security-matrix.md scaffolding.
