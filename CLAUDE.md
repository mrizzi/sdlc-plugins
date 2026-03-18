# sdlc-plugins

## Version Management

The plugin version must be kept in sync in two files:

- `plugins/sdlc-workflow/.claude-plugin/plugin.json` — the plugin manifest (required by CI validation)
- `.claude-plugin/marketplace.json` — the marketplace registry (required for relative-path plugins per Claude Code docs)

When bumping the version, update both files together.
