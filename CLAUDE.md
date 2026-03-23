# sdlc-plugins

## Documentation

- [docs/methodology.md](docs/methodology.md) — Core principles and SDLC phases
- [docs/workflow.md](docs/workflow.md) — Execution workflow (plan, implement, verify) and skill invocation
- [docs/tools.md](docs/tools.md) — MCP server catalog (Jira, Figma, Serena)
- [docs/conventions-spec.md](docs/conventions-spec.md) — Cross-repo workflow conventions and per-repo template reference
- [docs/constraints.md](docs/constraints.md) — Deterministic rules for agent behavior
- [docs/project-config-contract.md](docs/project-config-contract.md) — Project Configuration contract for CLAUDE.md
- [docs/metrics.md](docs/metrics.md) — Workflow metrics and measurement
- [docs/releasing.md](docs/releasing.md) — Release process and changelog

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
- GitHub Issue custom field: customfield_10747

## Code Intelligence

No Serena MCP servers are configured. Code intelligence is not available.

### Limitations

No limitations known — no Serena instances configured.
