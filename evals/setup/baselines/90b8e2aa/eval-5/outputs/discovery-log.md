# Discovery Log

## Step 1 -- Read Existing Configuration

Read `CLAUDE.md` (simulated from `evals/setup/files/claude-md-empty.md`). The file exists but contains no `# Project Configuration` section. All sections need to be created from scratch.

## Step 2 -- Discover Serena Instances

Examined available MCP tools listing. Discovered 2 Serena instances by identifying tools matching the `mcp__<instance>__<tool>` naming pattern:

- **serena_backend** -- tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir
- **serena_ui** -- tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir

Also discovered Atlassian MCP server (tools prefixed with `mcp__atlassian__`).

User provided repository details for each Serena instance:
- serena_backend: repository 'backend', role 'Rust backend service', path '/home/user/backend'
- serena_ui: repository 'frontend-ui', role 'TypeScript frontend', path '/home/user/frontend-ui'

## Step 3 -- Jira Configuration

No existing Jira Configuration found. User provided all fields manually:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

## Step 5 -- Code Intelligence

No existing Code Intelligence section found. Generated section with:
- Tool naming convention documentation (`mcp__<instance>__<tool>`)
- Concrete example using serena_backend instance
- Limitations subheading -- user confirmed no known limitations for either instance

## Step 9 -- Bug Configuration

No existing Bug Configuration found. Discovered and configured:
- Bug issue type ID: 10001 (discovered from Jira metadata)
- Bug template path: docs/bug-template.md (user accepted default)
- Bug-to-Task link type: Blocks (user accepted default)
- Bug template file copy skipped (simulation mode)

## Step 10 -- Security Configuration

No existing Security Configuration found. User was asked whether to enable security triage -- **user accepted the opt-in**.

### Step 10.1 -- Product Lifecycle

User provided all Product Lifecycle fields:
- Product pages URL: https://access.example.com/product-lifecycle
- Jira version prefix: MYPRODUCT
- Vulnerability issue type ID: 10200
- Component label pattern: pscomponent:
- VEX Justification custom field: customfield_12345

### Step 10.2 -- Version Streams

User provided 1 version stream:
- Stream: 2.1.x
- Konflux Release Repo: git.downstream.example.com/my-org/product-release.2.1.z
- Local Path: /home/user/product-release.2.1.z
- Security Matrix Path: security-matrix.md

### Step 10.3 -- Source Repositories

User provided 2 source repositories:
- backend: https://github.com/example/backend (deployment context: upstream)
- frontend-ui: https://github.com/example/frontend-ui (deployment context: upstream)

### Step 10.5 -- Security Matrix Scaffolding

User skipped security-matrix.md scaffolding.

### Step 10.6 -- Supportability Matrix Population

User declined optional supportability matrix population.
