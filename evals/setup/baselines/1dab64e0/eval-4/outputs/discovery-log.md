# Discovery Log

## Serena Instance Discovery

Scanned available MCP tools for Serena instances by identifying tool prefixes matching the pattern `mcp__<instance>__<tool>`.

### Discovered Instances

1. **serena_backend** — 10 tools available (find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir)
   - Status: Already present in Repository Registry
   - Action: Preserved existing entry verbatim

2. **serena_ui** — 10 tools available (find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir)
   - Status: New instance, not in existing Registry
   - User provided: repository 'trustify-ui', role 'TypeScript frontend', path '/home/user/trustify-ui'
   - Action: Added to Repository Registry

## Jira Discovery

Jira MCP tools detected (mcp__atlassian__jira_*). Existing Jira Configuration found in CLAUDE.md and preserved.

- Project key: already configured
- Cloud ID: already configured
- Feature issue type ID: already configured
- Custom fields: already configured

## Bug Configuration Discovery

- Bug issue type ID: 10001 (discovered from Jira metadata)
- Bug template path: docs/bug-template.md (user accepted default)
- Bug-to-Task link type: Blocks (user accepted default)
- Action: Added Bug Configuration section

## Security Configuration

- User was asked whether to enable security triage
- User declined
- Action: Security Configuration section not added

## Hierarchy Configuration

- Default epic grouping strategy set to: by-sub-feature
