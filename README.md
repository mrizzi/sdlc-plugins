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

- **report-bug** — Interactively define a Jira Bug by walking through
  project-configured template sections, or accept structured input
  programmatically from other skills.

- **triage-bug** — Triage a Jira Bug issue by investigating root cause through
  codebase analysis, posting a root cause comment, and producing a linked fix
  Task with a reproducer test front-loaded for `/implement-task` consumption.

- **triage-security** — Triage PSIRT-created Vulnerability issues (CVEs) with
  version-aware impact analysis across supported product versions. Includes a
  discovery mode for listing untriaged vulnerabilities.

- **run-evals** — Run structured eval suites against skills to measure output
  quality and catch regressions.

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

## Evaluations

Several skills have structured eval suites for measuring output quality and
catching regressions. See the eval directories for each skill:

- [evals/plan-feature/](evals/plan-feature/) — Plan-feature eval cases
- [evals/define-feature/](evals/define-feature/) — Define-feature eval cases
- [evals/implement-task/](evals/implement-task/) — Implement-task eval cases
- [evals/verify-pr/](evals/verify-pr/) — Verify-pr eval cases
- [evals/report-bug/](evals/report-bug/) — Report-bug eval cases
- [evals/triage-bug/](evals/triage-bug/) — Triage-bug eval cases
- [evals/triage-security/](evals/triage-security/) — Triage-security eval cases
- [evals/setup/](evals/setup/) — Setup eval cases

See [evals/README.md](evals/README.md) for usage instructions and the iteration
workflow.

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
