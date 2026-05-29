# Changes Log

All sections are newly added (greenfield setup — no prior Project Configuration existed).

## Added

### Project Configuration (new top-level section)

- **Repository Registry**: Added table structure with headers (Repository, Role, Serena Instance, Path). No data rows — no Serena instances were discovered.

- **Jira Configuration**: Added with three fields provided via manual entry:
  - Project key: MYPROJ
  - Cloud ID: abc123
  - Feature issue type ID: 10001
  - No optional custom fields were provided (Git Pull Request, GitHub Issue fields omitted).

- **Code Intelligence**: Added with no-Serena notice. Documents that no Serena MCP servers are configured and code intelligence is not available.
  - **Limitations** subsection notes no limitations known since no Serena instances are configured.
