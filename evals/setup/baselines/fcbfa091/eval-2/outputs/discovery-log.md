# Discovery Log

## Serena Instance Discovery

Scanned available MCP tools for Serena instances by identifying tool prefixes matching `mcp__serena_*__*`.

### Discovered Instances

| Instance | Status | Tools Found |
|---|---|---|
| serena_backend | Already configured | 10 (find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir) |
| serena_ui | New — not yet in Registry | 10 (find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir) |

### Other MCP Servers

| Server | Status |
|---|---|
| Atlassian MCP | Present (provides Jira tools) |

## Jira Configuration

Jira configuration already present in existing CLAUDE.md. No changes needed.

## Bug Configuration

Bug configuration already present in existing CLAUDE.md. No changes needed.

## Security Configuration

User declined security triage configuration. Security Configuration section not added.

## New Instance Details (User-Provided)

- **serena_ui**:
  - Repository: trustify-ui
  - Role: TypeScript frontend
  - Path: /home/user/trustify-ui
  - Known limitations: None
