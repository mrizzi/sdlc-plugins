# sdlc-plugins

A Claude Code plugin marketplace for AI-assisted SDLC workflow skills.

This repository hosts reusable skills that help engineers plan features and
implement tasks with full Jira traceability. Any project can install these
skills via Claude Code's plugin system.

## Available Plugins

### sdlc-workflow (v0.1.0)

AI-assisted SDLC workflow skills:

- **plan-feature** — Convert a Jira feature into an implementation plan with
  structured Jira tasks. Analyzes repositories using Serena LSP, builds an
  impact map, and creates linked Jira tasks.

- **implement-task** — Implement a Jira task by reading its structured
  description, modifying code, running tests, committing, opening a PR, and
  updating Jira.

## Installation

### 1. Add the marketplace

```
/plugin marketplace add /path/to/sdlc-plugins
```

### 2. Install the plugin

```
/plugin install sdlc-workflow
```

This copies the plugin's skills into your project, making them available as
slash commands.

## Project Configuration

For the skills to work with your project, your project's CLAUDE.md must
implement the [Project Configuration Contract](docs/project-config-contract.md).

The contract requires three sections in your CLAUDE.md:

1. **Repository Registry** — maps repos to Serena instances and local paths
2. **Jira Configuration** — project key, cloud ID, issue type IDs
3. **Code Intelligence** — Serena tool naming and per-instance limitations

See [docs/project-config-contract.md](docs/project-config-contract.md) for
the full specification and a complete example.

## Documentation

- [Project Configuration Contract](docs/project-config-contract.md) — interface
  contract between skills and project configuration
- [SDLC Methodology](docs/methodology.md) — core principles and phased roadmap
- [Architecture Template](docs/templates/architecture.md) — template for
  documenting your project's architecture
- [Conventions Template](docs/templates/conventions.md) — template for
  documenting your project's coding conventions

## License

Apache-2.0. See [LICENSE](LICENSE).
