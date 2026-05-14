# Discovery Log

## Source

MCP tools listing from `mcp-tools-with-serena.md`.

## Discovered Serena Instances

Two Serena MCP server instances were discovered by scanning for tools matching the `mcp__<instance>__<tool>` naming pattern:

1. **serena_backend** -- identified from tools prefixed with `mcp__serena_backend__` (10 tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir)
2. **serena_ui** -- identified from tools prefixed with `mcp__serena_ui__` (10 tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir)

## Discovered Atlassian MCP

Atlassian MCP tools were also discovered (prefixed with `mcp__atlassian__`): jira_get_issue, jira_search_issues, jira_edit_issue, jira_transition_issue, jira_add_comment, jira_user_info.

## User-Provided Repository Mappings

- **serena_backend** mapped to repository `trustify-backend`, role "Rust backend service", path `/home/user/trustify-backend`
- **serena_ui** mapped to repository `trustify-ui`, role "TypeScript frontend", path `/home/user/trustify-ui`

## User-Provided Jira Configuration

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

## Limitations

No limitations were reported for either Serena instance.
