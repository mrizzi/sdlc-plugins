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
- **Adversarial fixture annotation**: Eval or test fixture files that contain intentionally adversarial, malicious-looking, or unusual content (e.g., injection vectors, malformed input, security-sensitive patterns) must include a leading comment block explaining that the content is deliberate test material. Use the file's native comment syntax (e.g., `<!-- ... -->` for Markdown/HTML, `// ...` for JSON with comments, `# ...` for YAML). The comment should state the purpose (e.g., "This fixture contains intentional injection patterns for eval testing") so reviewers and automated scanners do not flag the content as a real security concern.
- **Synthetic data labeling**: Fixture files that represent synthetic or mock entities (e.g., fake repository structures, mock Jira issues, fabricated API responses) must include a header comment noting they are representative test data, not real resources. This prevents confusion about whether the data refers to actual systems, repositories, or issues. Use a brief note such as "Synthetic test data — names, URLs, and identifiers are fictional."

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
