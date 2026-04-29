# Discovery Log

## Source

MCP tools listing from: `evals/setup/files/mcp-tools-with-serena.md`

## Serena Instances Discovered

Two Serena instances were identified by scanning for `mcp__<instance>__<tool>` patterns in the MCP tools listing.

### 1. serena_backend

- **Source section**: "Serena -- serena_backend"
- **Tools discovered** (10 tools):
  - mcp__serena_backend__find_symbol
  - mcp__serena_backend__get_symbols_overview
  - mcp__serena_backend__search_for_pattern
  - mcp__serena_backend__find_referencing_symbols
  - mcp__serena_backend__replace_symbol_body
  - mcp__serena_backend__insert_after_symbol
  - mcp__serena_backend__insert_before_symbol
  - mcp__serena_backend__rename_symbol
  - mcp__serena_backend__get_diagnostics
  - mcp__serena_backend__list_dir
- **User-provided mapping**: repository 'trustify-backend', role 'Rust backend service', path '/home/user/trustify-backend'

### 2. serena_ui

- **Source section**: "Serena -- serena_ui"
- **Tools discovered** (10 tools):
  - mcp__serena_ui__find_symbol
  - mcp__serena_ui__get_symbols_overview
  - mcp__serena_ui__search_for_pattern
  - mcp__serena_ui__find_referencing_symbols
  - mcp__serena_ui__replace_symbol_body
  - mcp__serena_ui__insert_after_symbol
  - mcp__serena_ui__insert_before_symbol
  - mcp__serena_ui__rename_symbol
  - mcp__serena_ui__get_diagnostics
  - mcp__serena_ui__list_dir
- **User-provided mapping**: repository 'trustify-ui', role 'TypeScript frontend', path '/home/user/trustify-ui'

## Jira Configuration Discovered

- **Source**: Atlassian MCP tools section in the MCP tools listing (tools prefixed with `mcp__atlassian__jira_*`)
- **User-provided values**: Project key=TC, Cloud ID=2b9e35e3-6bd3-4cec-b838-f4249ee02432, Feature issue type ID=10142, Git Pull Request custom field=customfield_10875, GitHub Issue custom field=customfield_10747

## Existing CLAUDE.md

- **Source**: `evals/setup/files/claude-md-empty.md`
- **Observation**: No Project Configuration section found. The file contains only project description, documentation links, and getting started instructions.
