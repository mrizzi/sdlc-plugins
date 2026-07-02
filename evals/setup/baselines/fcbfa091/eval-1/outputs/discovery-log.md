# Discovery Log

## MCP Tool Discovery

Source: MCP tools listing (mcp-tools-with-serena.md)

### Serena Instances Discovered

Two Serena instances were identified from the available MCP tools:

1. **serena_backend** — Discovered from tools prefixed with `mcp__serena_backend__` (find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir)
2. **serena_ui** — Discovered from tools prefixed with `mcp__serena_ui__` (find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir)

### Atlassian MCP Discovered

Jira tools available via `mcp__atlassian__` prefix: jira_get_issue, jira_search_issues, jira_edit_issue, jira_transition_issue, jira_add_comment, jira_user_info.

## Repository Registry

Source: User-provided mapping for each discovered Serena instance.

| Serena Instance | Repository | Role | Path |
|---|---|---|---|
| serena_backend | trustify-backend | Rust backend service | /home/user/trustify-backend |
| serena_ui | trustify-ui | TypeScript frontend | /home/user/trustify-ui |

## Jira Configuration

Source: User-provided values.

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

## Bug Configuration

Source: Jira metadata discovery (simulated) and user confirmation.

- Bug issue type ID: 10001 (discovered from Jira metadata)
- Bug template path: docs/bug-template.md (user accepted default)
- Bug-to-Task link type: Blocks (user accepted default)

## Code Intelligence Limitations

Source: User confirmation for each Serena instance.

- serena_backend: No known limitations
- serena_ui: No known limitations

## Security Configuration

Source: User response to security triage prompt.

- User declined to enable security triage for this project. Security Configuration section was not added.
