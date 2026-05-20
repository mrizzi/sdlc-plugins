# Discovery Log

## Source

Discovery was performed by inspecting the available MCP tool listing (simulated).

## Serena Instances Discovered

Two Serena instances were identified from the MCP tool prefixes:

1. **serena_backend** -- discovered from tools prefixed with `mcp__serena_backend__` (e.g., `mcp__serena_backend__find_symbol`, `mcp__serena_backend__get_symbols_overview`, etc.). 10 tools total.
   - User provided: repository name = `trustify-backend`, role = `Rust backend service`, path = `/home/user/trustify-backend`.
   - No known limitations reported.

2. **serena_ui** -- discovered from tools prefixed with `mcp__serena_ui__` (e.g., `mcp__serena_ui__find_symbol`, `mcp__serena_ui__get_symbols_overview`, etc.). 10 tools total.
   - User provided: repository name = `trustify-ui`, role = `TypeScript frontend`, path = `/home/user/trustify-ui`.
   - No known limitations reported.

## Jira / Atlassian MCP Discovered

Atlassian MCP tools were found in the tool listing (e.g., `mcp__atlassian__jira_get_issue`, `mcp__atlassian__jira_search_issues`, etc.). 6 tools total.

- User provided Jira configuration: Project key = TC, Cloud ID = 2b9e35e3-6bd3-4cec-b838-f4249ee02432, Feature issue type ID = 10142, Git Pull Request custom field = customfield_10875, GitHub Issue custom field = customfield_10747.

## Existing CLAUDE.md

The existing CLAUDE.md (`evals/setup/files/claude-md-empty.md`) contained no Project Configuration section. This is a greenfield setup.
