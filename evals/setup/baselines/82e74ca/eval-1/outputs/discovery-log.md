# Discovery Log

## Source

Discovery was performed by examining the available MCP tool listing in `mcp-tools-with-serena.md`.

## Serena Instances Discovered

Two Serena MCP server instances were identified from the tool naming pattern `mcp__<instance>__<tool>`:

1. **serena_backend** -- discovered from tools prefixed with `mcp__serena_backend__` (e.g., `mcp__serena_backend__find_symbol`, `mcp__serena_backend__get_symbols_overview`, `mcp__serena_backend__search_for_pattern`, etc.)
   - User provided: repository name = `trustify-backend`, role = `Rust backend service`, path = `/home/user/trustify-backend`

2. **serena_ui** -- discovered from tools prefixed with `mcp__serena_ui__` (e.g., `mcp__serena_ui__find_symbol`, `mcp__serena_ui__get_symbols_overview`, `mcp__serena_ui__search_for_pattern`, etc.)
   - User provided: repository name = `trustify-ui`, role = `TypeScript frontend`, path = `/home/user/trustify-ui`

## Atlassian MCP Discovered

An Atlassian MCP server was identified from tools prefixed with `mcp__atlassian__` (e.g., `mcp__atlassian__jira_get_issue`, `mcp__atlassian__jira_search_issues`, etc.).

Jira configuration was provided manually by the user:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

## Serena Limitations

User confirmed no known limitations for either Serena instance.

## Existing CLAUDE.md State

The existing CLAUDE.md (`claude-md-empty.md`) contained no `# Project Configuration` section. All configuration sections needed to be created from scratch.
