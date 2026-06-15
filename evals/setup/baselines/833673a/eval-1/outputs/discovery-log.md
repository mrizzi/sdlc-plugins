# Discovery Log

## Source

MCP tools listing from: evals/setup/files/mcp-tools-with-serena.md

## Serena Instances Discovered

Two Serena instances were discovered by scanning for `mcp__<instance>__<tool>` patterns in the MCP tools listing:

### serena_backend

- Identified by tool prefix: `mcp__serena_backend__`
- Tools found (10): find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir
- User-provided mapping: repository 'trustify-backend', role 'Rust backend service', path '/home/user/trustify-backend'

### serena_ui

- Identified by tool prefix: `mcp__serena_ui__`
- Tools found (10): find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir
- User-provided mapping: repository 'trustify-ui', role 'TypeScript frontend', path '/home/user/trustify-ui'

## Atlassian MCP

- Jira tools discovered: jira_get_issue, jira_search_issues, jira_edit_issue, jira_transition_issue, jira_add_comment, jira_user_info
- Jira configuration values provided by user

## Existing CLAUDE.md

- Source: evals/setup/files/claude-md-empty.md
- No existing Project Configuration section found — greenfield setup

## Security Configuration

- User declined security triage — section omitted
