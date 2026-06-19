# Discovery Log

## Serena Instances

- **serena_backend**: Already configured in the Repository Registry (trustify-backend, Rust backend service, /home/user/trustify-backend). No changes needed.
- **serena_ui**: Newly discovered from the MCP tool listing. Tools found: `mcp__serena_ui__find_symbol`, `mcp__serena_ui__get_symbols_overview`, `mcp__serena_ui__search_for_pattern`, and others. User provided: repository 'trustify-ui', role 'TypeScript frontend', path '/home/user/trustify-ui', no known limitations. Added to Repository Registry and Code Intelligence Limitations.

## Jira Configuration

Jira Configuration is already fully populated — no changes needed. All fields present: Project key (TC), Cloud ID, Feature issue type ID (10142), Git Pull Request custom field (customfield_10875), GitHub Issue custom field (customfield_10747).

## Code Intelligence

Code Intelligence section exists with naming convention documentation and serena_backend example. serena_backend limitations preserved ("rust-analyzer may take 30-60 seconds to index on first use"). serena_ui limitation entry added ("No known limitations").

## Bug Configuration

Bug Configuration is up to date. All three fields present and unchanged: Bug issue type ID (10001), Bug template (docs/bug-template.md), Bug-to-Task link type (Blocks).

## Security Configuration

Security Configuration opt-in was offered (the existing CLAUDE.md has no Security Configuration section). User declined — Security Configuration section was not added.
