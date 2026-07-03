# Changes Log

## Sections Added to Project Configuration

1. **Repository Registry** -- Newly added. Table created with standard headers (Repository, Role, Serena Instance, Path) but no data rows, since no Serena instances were discovered.

2. **Jira Configuration** -- Newly added. Configured with manually provided values:
   - Project key: MYPROJ
   - Cloud ID: abc123
   - Feature issue type ID: 10001

3. **Code Intelligence** -- Newly added. Documents that no Serena MCP servers are configured and code intelligence is not available. Limitations subsection notes no Serena instances.

4. **Bug Configuration** -- Newly added. Configured with:
   - Bug issue type ID: 10001 (manually provided)
   - Bug template: docs/bug-template.md (default accepted)
   - Bug-to-Task link type: Blocks (default accepted)

## Sections Declined

- **Security Configuration** -- User declined when prompted whether to enable security triage. Section was not added.
