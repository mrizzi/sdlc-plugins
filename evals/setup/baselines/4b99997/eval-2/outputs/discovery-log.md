# Discovery Log

## Source

MCP tool listing from: `files/mcp-tools-with-serena.md`

## Discovered Serena Instances

1. **serena_backend** — already configured in existing Repository Registry. No changes needed.
2. **serena_ui** — newly discovered from MCP tools prefixed with `mcp__serena_ui__` (10 tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir). Not yet in the Registry — needs to be added.

## Discovered Atlassian/Jira Tools

- `mcp__atlassian__jira_get_issue`
- `mcp__atlassian__jira_search_issues`
- `mcp__atlassian__jira_edit_issue`
- `mcp__atlassian__jira_transition_issue`
- `mcp__atlassian__jira_add_comment`
- `mcp__atlassian__jira_user_info`

## User-Provided Configuration

### New Repository Mapping

- serena_ui: repository 'trustify-ui', role 'TypeScript frontend', path '/home/user/trustify-ui'

### Jira Configuration

All Jira fields already configured — no changes needed.

### Limitations

- No known limitations reported for the new serena_ui instance.
