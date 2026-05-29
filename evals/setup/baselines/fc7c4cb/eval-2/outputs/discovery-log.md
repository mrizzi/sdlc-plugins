# Serena Instance Discovery Log

## Discovery Source

Parsed available MCP tools listing to identify Serena instances by the `mcp__<instance>__` prefix pattern.

## Instances Found

### serena_backend — Already Configured

- Present in MCP tools: yes (10 tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir)
- Present in Repository Registry: yes (trustify-backend, Rust backend service)
- Present in Code Intelligence Limitations: yes (rust-analyzer indexing note)
- Action: No changes needed. Existing configuration preserved as-is.

### serena_ui — Newly Discovered

- Present in MCP tools: yes (10 tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir)
- Present in Repository Registry: no
- Present in Code Intelligence Limitations: no
- Action: Added to Repository Registry and Code Intelligence Limitations.
- User-provided details: repository `trustify-ui`, role `TypeScript frontend`, path `/home/user/trustify-ui`, no known limitations.
