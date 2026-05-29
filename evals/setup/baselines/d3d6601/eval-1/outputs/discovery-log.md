# Discovery Log

## Source

MCP tool listing from: `evals/setup/files/mcp-tools-with-serena.md`

## Serena Instances Discovered

Two Serena instances were identified from the MCP tool listing by scanning for tool name prefixes matching the pattern `mcp__<instance>__<tool>`:

### serena_backend

- Source: MCP tool listing section "Serena -- serena_backend"
- Tools found (10): find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir
- User-provided mapping: repository 'trustify-backend', role 'Rust backend service', path '/home/user/trustify-backend'
- Limitations: none reported

### serena_ui

- Source: MCP tool listing section "Serena -- serena_ui"
- Tools found (10): find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir
- User-provided mapping: repository 'trustify-ui', role 'TypeScript frontend', path '/home/user/trustify-ui'
- Limitations: none reported

## Other MCP Tools Discovered

- **Atlassian MCP**: jira_get_issue, jira_search_issues, jira_edit_issue, jira_transition_issue, jira_add_comment, jira_user_info
- **Built-in tools**: Bash, Read, Write, Edit, Glob, Grep

## Jira Configuration

Provided by user:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747
