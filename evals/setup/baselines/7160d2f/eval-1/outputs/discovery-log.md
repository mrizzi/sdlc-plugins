# Discovery Log

## Existing CLAUDE.md

- Source: `evals/setup/files/claude-md-empty.md`
- No existing Project Configuration section found. This is a greenfield setup.

## Serena Instance Discovery

- Source: `evals/setup/files/mcp-tools-with-serena.md` (MCP tool listing)
- Discovered **2 Serena instances** by matching the `mcp__<instance>__<tool>` naming pattern:
  - `serena_backend` — 10 tools (find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir)
  - `serena_ui` — 10 tools (find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir)

## Jira Discovery

- Source: MCP tool listing shows Atlassian MCP tools available (jira_get_issue, jira_search_issues, jira_edit_issue, jira_transition_issue, jira_add_comment, jira_user_info)
- Jira configuration values provided by user:
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Feature issue type ID: 10142
  - Git Pull Request custom field: customfield_10875
  - GitHub Issue custom field: customfield_10747

## Security Configuration

- User declined to enable security triage. No Security Configuration section added.
