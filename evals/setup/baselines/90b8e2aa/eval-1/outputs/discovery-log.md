# Discovery Log

## Serena Instances

Discovered 2 Serena instances from the MCP tool listing:

1. **serena_backend** — identified from tools prefixed with `mcp__serena_backend__` (10 tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir). User confirmed: repository `trustify-backend`, role "Rust backend service", path `/home/user/trustify-backend`. No known limitations.

2. **serena_ui** — identified from tools prefixed with `mcp__serena_ui__` (10 tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir). User confirmed: repository `trustify-ui`, role "TypeScript frontend", path `/home/user/trustify-ui`. No known limitations.

## Jira / Atlassian

Discovered Atlassian MCP tools from the tool listing (6 tools prefixed with `mcp__atlassian__`). User provided Jira configuration values:

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

## Bug Configuration

- Bug issue type ID: 10001 (discovered from Jira metadata)
- Bug template path: docs/bug-template.md (user accepted default)
- Bug-to-Task link type: Blocks (user accepted default)

## Security Configuration

- User declined to enable security triage for this project. Section not added.
