# Discovery Log

## MCP Tool Scan

Scanned available MCP tools for Serena instances by identifying tool prefixes matching the pattern `mcp__serena_*__<tool>`.

### Discovered Serena Instances

| Instance | Tools Found | Status |
|---|---|---|
| serena_backend | 10 | Already configured in Repository Registry |
| serena_ui | 10 | NEW -- not yet in Repository Registry |

### serena_backend (existing)

Tools detected:
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

Action: No changes needed. Entry already present in Repository Registry.

### serena_ui (new)

Tools detected:
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

Action: Added to Repository Registry with user-provided metadata.
- Repository: trustify-ui
- Role: TypeScript frontend
- Path: /home/user/trustify-ui
- Limitations: No known limitations

## Other MCP Tools

- Built-in tools: Bash, Read, Write, Edit, Glob, Grep
- Atlassian MCP: jira_get_issue, jira_search_issues, jira_edit_issue, jira_transition_issue, jira_add_comment, jira_user_info (Jira configuration already present)
