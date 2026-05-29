# Discovery Log

## Source

MCP tool listing from `mcp-tools-with-serena.md`.

## Serena Instances Discovered

Two Serena instances were discovered from the MCP tool listing by identifying tool name prefixes matching the pattern `mcp__<instance>__<tool>`:

1. **serena_backend** — identified from tools prefixed with `mcp__serena_backend__` (10 tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir)
2. **serena_ui** — identified from tools prefixed with `mcp__serena_ui__` (10 tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir)

## Serena Instance Mapping (User-Provided)

- **serena_backend** mapped to repository `trustify-backend`, role: Rust backend service, path: `/home/user/trustify-backend`
- **serena_ui** mapped to repository `trustify-ui`, role: TypeScript frontend, path: `/home/user/trustify-ui`

## Jira / Atlassian MCP Discovered

Atlassian MCP tools were discovered from the tool listing, confirming Jira integration is available. Tools found:

- mcp__atlassian__jira_get_issue
- mcp__atlassian__jira_search_issues
- mcp__atlassian__jira_edit_issue
- mcp__atlassian__jira_transition_issue
- mcp__atlassian__jira_add_comment
- mcp__atlassian__jira_user_info

## Jira Configuration (User-Provided)

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

## Limitations

No limitations were reported for either Serena instance.
