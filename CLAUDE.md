# sdlc-plugins

## Version Management

The plugin version must be kept in sync in two files:

- `plugins/sdlc-workflow/.claude-plugin/plugin.json` — the plugin manifest (required by CI validation)
- `.claude-plugin/marketplace.json` — the marketplace registry (required for relative-path plugins per Claude Code docs)

When bumping the version, update both files together.

# Project Configuration

## Repository Registry

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| sdlc-plugins | Claude Code plugin | — | ./ |

## Jira Configuration

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875

## Code Intelligence

No Serena MCP servers are configured. Code intelligence is not available.

### Limitations

No limitations known — no Serena instances configured.
