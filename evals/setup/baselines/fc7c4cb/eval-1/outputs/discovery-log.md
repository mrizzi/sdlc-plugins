# Discovery Log

## Existing CLAUDE.md Analysis

- Source: `evals/setup/files/claude-md-empty.md`
- Project Configuration section: **not found** (greenfield setup)
- Existing content: project heading, documentation links, and getting started instructions

## Serena Instance Discovery

- Source: MCP tools listing (`evals/setup/files/mcp-tools-with-serena.md`)
- Discovered **2 Serena instances**:
  1. `serena_backend` — identified from tools prefixed with `mcp__serena_backend__` (10 tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir)
  2. `serena_ui` — identified from tools prefixed with `mcp__serena_ui__` (10 tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir)

## Other MCP Tools Discovered

- Atlassian MCP tools available (jira_get_issue, jira_search_issues, jira_edit_issue, jira_transition_issue, jira_add_comment, jira_user_info) — confirms Jira integration is available for the configured project
