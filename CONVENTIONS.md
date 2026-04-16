# Coding Conventions

<!-- This file documents project-specific coding standards for sdlc-plugins.
     It helps the AI assistant follow your project's patterns when generating
     or modifying code. Fill in each section with your project's conventions. -->

## Language and Framework

- **Primary format**: Markdown documentation
- **Configuration**: YAML (`.serena/project.yml`) and JSON (plugin manifests)
- **Plugin system**: Claude Code plugin format
- **No source code**: This is a documentation-heavy repository — skills are defined in Markdown (`SKILL.md` files) rather than traditional programming languages

## Code Style

- **Markdown**: Use GitHub-flavored Markdown for all documentation
- **Line length**: No strict limit, but keep content readable
- **YAML**: Use 2-space indentation for configuration files (`.serena/project.yml`)
- **JSON**: Use 2-space indentation for manifests (`.claude-plugin/*.json`)
- **Formatting**: No automated formatters — manual review for consistency

## Naming Conventions

- **Skills**: kebab-case (e.g., `plan-feature`, `implement-task`, `verify-pr`)
- **Documentation files**: kebab-case (e.g., `project-config-contract.md`, `conventions-spec.md`)
- **Skill definitions**: uppercase `SKILL.md` in each skill directory
- **Templates**: use `.template.md` suffix (e.g., `conventions.template.md`, `constraints.template.md`)
- **Directories**: kebab-case (e.g., `define-feature`, `implement-task`)

## File Organization

- **`docs/`** — core documentation (methodology, workflow, tools, conventions, constraints, metrics, releasing)
- **`docs/templates/`** — reusable templates (architecture, conventions)
- **`plugins/sdlc-workflow/`** — main plugin directory
  - **`skills/<skill-name>/`** — individual skill directories, each containing a `SKILL.md` file
  - **`shared/`** — shared resources like `task-description-template.md`
  - **`scripts/`** — utility scripts (if any)
  - **`.claude-plugin/`** — plugin manifest (`plugin.json`)
- **`.claude-plugin/`** — marketplace manifest at root level (`marketplace.json`)
- **`.serena/`** — Serena configuration files
- **`.github/workflows/`** — CI validation workflows

**New skill placement**: Add new skills as subdirectories under `plugins/sdlc-workflow/skills/` with a `SKILL.md` file inside.

**New documentation**: Add core documentation to `docs/`, templates to `docs/templates/`.

## Error Handling

Not applicable — this is a documentation repository with no runtime code.

## Testing Conventions

- **Manual smoke testing**: Described in `.github/workflows/validate-plugins.yml` header
  1. Run `claude --plugin-dir ./plugins/sdlc-workflow`
  2. Test each skill (e.g., `/sdlc-workflow:plan-feature`) to verify it loads and responds
  3. Run `/agents` to verify no plugin agents are missing
  4. Edit a `SKILL.md`, then `/reload-plugins` to verify changes are picked up
- **CI validation**: Uses `claude plugin validate` on all plugin directories under `plugins/`
- **No automated tests**: Skills are validated through CI and manual testing; no unit test framework

## Commit Messages

- **Format**: Conventional Commits — `type(scope): description`
- **Types**:
  - `feat` — new features or enhancements
  - `fix` — bug fixes
  - `refactor` — code restructuring
  - `test` — test-related changes
  - `docs` — documentation updates
  - `chore` — maintenance tasks (e.g., version bumps, releases)
- **Scope**: Use the skill name (e.g., `verify-pr`, `implement-task`) or component (e.g., `release`, `workflow`)
- **Examples from this repo**:
  - `feat(verify-pr): add test doc comment check to Step 12`
  - `chore(release): bump version to 0.5.11`
  - `fix(plan-feature): correct inconsistent example mapping in display text comparison`

## Shared Modules and Reuse

- **`plugins/sdlc-workflow/shared/task-description-template.md`** — canonical task template structure used by `plan-feature`, `verify-pr` (producers) and `implement-task` (consumer)
- **`plugins/sdlc-workflow/skills/setup/*.template.md`** — templates for scaffolding:
  - `conventions.template.md` — CONVENTIONS.md scaffold
  - `constraints.template.md` — constraints document scaffold
  - `project-config.template.md` — Project Configuration section scaffold
- **Skill patterns**: When creating new skills, follow the structure of existing skills (e.g., `implement-task/SKILL.md`, `plan-feature/SKILL.md`) — each has clear step-by-step instructions, guardrails, and important rules sections

## Documentation

- **`README.md`** (root) — project overview, installation instructions, plugin catalog; update when:
  - New skills are added
  - Installation steps change
  - Project description changes
- **`docs/`** directory — comprehensive documentation:
  - `methodology.md` — core principles and SDLC phases
  - `workflow.md` — execution workflow
  - `tools.md` — MCP server catalog
  - `conventions-spec.md` — workflow conventions
  - `constraints.md` — deterministic rules (update when skill behavior rules change)
  - `project-config-contract.md` — CLAUDE.md configuration contract
  - `metrics.md` — workflow metrics
  - `releasing.md` — release process
- **`CHANGELOG.md`** — release history; update with every version bump
- **`SKILL.md`** files — skill-specific instructions; update when skill behavior changes
- **Format**: All documentation uses Markdown (GitHub-flavored)
- **Triggers for doc updates**:
  - New skills added → update `README.md`, add skill to documentation index
  - Skill behavior changes → update corresponding `SKILL.md` and `docs/constraints.md`
  - Configuration contract changes → update `docs/project-config-contract.md`
  - Release process changes → update `docs/releasing.md`

## Dependencies

- **No external dependencies** — this repository contains only documentation and configuration files
- **Runtime dependency**: Claude Code CLI (users must have Claude Code installed to use the plugins)
- **Plugin system**: Uses Claude Code's plugin marketplace and validation system (`claude plugin validate`)
- **Version synchronization**: The plugin version must be kept in sync between:
  - `.claude-plugin/marketplace.json` (required for update detection)
  - `plugins/sdlc-workflow/.claude-plugin/plugin.json` (required by CI validation)

## Performance Optimization

- **Documentation style**: Quick reference format — tables, bullet points, minimal prose
  - Core principles: Scannable, concise, actionable
  - Avoid: Long paragraphs, verbose examples, extensive troubleshooting prose
  - Prefer: Tables for structured data, bullet lists for procedures, diagrams for workflows
- **Commit message type**: Use `perf(scope): description` for performance optimization features
  - Example: `feat(performance): add baseline capture skill with test data verification`
- **Skill distinctions**: Make explicit which skills inspect source code vs read reports
  - Skills that inspect code: `performance-analyze-module` (analyzes source code for anti-patterns)
  - Skills that read reports: `performance-plan-optimization` (reads analysis reports), `performance-verify-optimization` (reads implementation results)
  - Document this distinction in skill descriptions and documentation
- **Metrics conventions**:
  - Default aggregation: p95 (95th percentile) across 5 iterations
  - Core Web Vitals: LCP (2500ms), FCP (1800ms), TTI (3500ms), Total Load Time (4000ms)
  - Regression threshold: 5% degradation in non-target scenarios
- **Baseline capture**:
  - Tool: Playwright for browser automation
  - Security: Validate user input, use timeouts, graceful degradation
  - Configuration: Store in `.claude/performance-config.md` in target repository
- **Anti-pattern detection**: 9 standard patterns (over-fetching, N+1 queries, waterfall loading, render-blocking, unused code, expensive re-renders, long tasks, layout thrashing, missing lazy loading)
