# sdlc-plugins

A Claude Code plugin marketplace for AI-assisted SDLC workflow skills.

This repository hosts reusable skills that help engineers set up projects,
plan features, implement tasks, and verify pull requests with full Jira
traceability. Any project can install these skills via Claude Code's plugin
system.

## Available Plugins

### sdlc-workflow

AI-assisted SDLC workflow skills for setting up projects, planning features,
implementing tasks, and verifying pull requests:

- **setup** — Set up or update the Project Configuration in your CLAUDE.md for
  use with sdlc-workflow skills.

- **define-feature** — Interactively define a Jira Feature by walking through
  all description template sections and creating the issue.

- **plan-feature** — Convert a Jira feature into an implementation plan with
  structured Jira tasks. Analyzes repositories using Serena LSP, builds an
  impact map, and creates linked Jira tasks.

- **implement-task** — Implement a Jira task by reading its structured
  description, modifying code, running tests, committing, opening a PR, and
  updating Jira.

- **verify-pr** — Verify a PR against its Jira task's acceptance criteria and
  deterministic guardrails.

- **performance-setup** — Initialize performance optimization workflow
  configuration for a target repository (workflow discovery, baseline capture
  settings, target directories).

- **performance-baseline** — Capture performance baseline metrics for selected
  workflow scenarios using automated browser testing.

- **performance-analyze-module** — Analyze a workflow module for performance
  anti-patterns (over-fetching, N+1 queries, waterfall loading, render-blocking
  resources, etc.) and generate an analysis report.

- **performance-plan-optimization** — Generate structured optimization plan from
  analysis reports, creating Jira Epic and Tasks for optimization work.

- **performance-implement-optimization** — Execute performance optimization task
  by implementing code changes, running performance tests, and comparing results
  against targets.

- **performance-verify-optimization** — Verify a performance optimization PR by
  reading review feedback, validating acceptance criteria, optionally re-running
  performance baseline, and creating sub-tasks for change requests.

## Installation

### 1. Add the marketplace

```
/plugin marketplace add mrizzi/sdlc-plugins
```

### 2. Install the plugin

```
/plugin install sdlc-workflow
```

This copies the plugin's skills into your project, making them available as
slash commands.

### 3. Configure your project

```
/sdlc-workflow:setup
```

This interactively populates the required Project Configuration in your
project's CLAUDE.md (repository registry, Jira settings, and code intelligence).

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

- [Methodology](docs/methodology.md) — Core principles and SDLC phases
- [Workflow](docs/workflow.md) — Execution workflow (plan, implement, verify) and skill invocation
- [Tools](docs/tools.md) — MCP server catalog (Jira, Figma, Serena)
- [Conventions Spec](docs/conventions-spec.md) — Cross-repo workflow conventions and per-repo template reference
- [Constraints](docs/constraints.md) — Deterministic rules for agent behavior
- [Project Configuration Contract](docs/project-config-contract.md) — Project Configuration contract for CLAUDE.md
- [Metrics](docs/metrics.md) — Workflow metrics and measurement
- [Releasing](docs/releasing.md) — Release process and changelog
- [Architecture Template](docs/templates/architecture.md) — Template for
  documenting your project's architecture
- [Conventions Template](docs/templates/conventions.md) — Template for
  documenting your project's coding conventions

## License

Apache-2.0. See [LICENSE](LICENSE).
