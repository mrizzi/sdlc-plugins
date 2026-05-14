# Discovery Log

## Source

MCP tool listing from `mcp-tools-with-serena.md`.

## Serena Instances Discovered

Two Serena MCP server instances were discovered by scanning tool name prefixes matching the pattern `mcp__<instance>__<tool>`:

1. **serena_backend** -- identified from tools prefixed with `mcp__serena_backend__` (10 tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir)
2. **serena_ui** -- identified from tools prefixed with `mcp__serena_ui__` (10 tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir)

## Jira/Atlassian MCP Discovered

Atlassian MCP tools were discovered with prefix `mcp__atlassian__`:
- jira_get_issue, jira_search_issues, jira_edit_issue, jira_transition_issue, jira_add_comment, jira_user_info

## User-Provided Configuration

- **serena_backend**: repository = trustify-backend, role = Rust backend service, path = /home/user/trustify-backend
- **serena_ui**: repository = trustify-ui, role = TypeScript frontend, path = /home/user/trustify-ui
- **Jira**: Project key = TC, Cloud ID = 2b9e35e3-6bd3-4cec-b838-f4249ee02432, Feature issue type ID = 10142, Git Pull Request custom field = customfield_10875, GitHub Issue custom field = customfield_10747
- **Limitations**: No known limitations for either Serena instance.

## Existing Project Configuration

No existing `# Project Configuration` section was found in the CLAUDE.md. This is a greenfield setup.
