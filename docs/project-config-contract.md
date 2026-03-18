# Project Configuration Contract

This document defines the interface contract between generic SDLC skills
(distributed via the sdlc-plugins marketplace) and project-specific
configuration (in each project repo's CLAUDE.md).

Skills are project-agnostic. They discover project context at runtime by
reading standardized sections from the project's CLAUDE.md. This contract
specifies what those sections must contain.

---

## Contract Overview

Every project that uses sdlc-workflow skills **must** include a
`# Project Configuration` section in its CLAUDE.md with three required
subsections:

1. **Repository Registry** — maps repositories to roles, Serena instances, and paths
2. **Jira Configuration** — project key, cloud ID, issue type IDs, custom fields
3. **Code Intelligence** — Serena tool naming convention and per-instance limitations

Projects **may** add optional sections beyond these three (e.g., Figma
configuration, deployment targets, environment variables). Skills will
ignore sections they do not recognize.

---

## Required Sections

### 1. Repository Registry

The Repository Registry is a markdown table under the heading
`## Repository Registry`. It maps each target repository to its role,
Serena MCP server instance name, and local filesystem path.

#### Required columns

| Column | Description |
|---|---|
| Repository | Short name of the repository (e.g., `trustify`) |
| Role | Brief description: language and purpose (e.g., "Rust backend") |
| Serena Instance | The MCP server instance name (e.g., `serena-trustify`) |
| Path | Absolute local path to the repository clone |

#### Structure

```markdown
## Repository Registry

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| <repo-name> | <language> <purpose> | <serena-instance-name> | <absolute-path> |
```

#### How skills use it

- "For each repository in the Repository Registry, use its Serena Instance
  to perform code analysis."
- "Identify the target repository from the task's Repository field, then
  look up the corresponding Serena Instance in the Repository Registry."
- "Use the Path column to locate repository files when Serena is unavailable."

---

### 2. Jira Configuration

The Jira Configuration is a list of key-value pairs under the heading
`## Jira Configuration`. It provides the project-specific Jira settings
that skills need to create issues, query tasks, and update fields.

#### Required fields

| Field | Description | Example |
|---|---|---|
| Project key | The Jira project key used in issue IDs | `TC` |
| Cloud ID | The Jira instance URL or cloud UUID | `https://issues.redhat.com` |
| Feature issue type ID | Numeric ID for the Feature issue type | `10142` |

#### Optional fields

| Field | Description | Example |
|---|---|---|
| Git Pull Request custom field | Custom field ID for storing PR URLs | `customfield_12310220` |
| Default labels | Labels to apply to AI-generated issues | `ai-generated-jira` |

#### Structure

```markdown
## Jira Configuration

- Project key: TC
- Cloud ID: https://issues.redhat.com
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_12310220
```

#### How skills use it

- "Use the Jira project key from Project Configuration when creating issues."
- "Use the Cloud ID as the `cloudId` parameter in all Jira MCP tool calls."
- "Use the Feature issue type ID when creating feature-level issues."
- "If a Git Pull Request custom field is configured, update it with the PR URL."

---

### 3. Code Intelligence

The Code Intelligence section is under the heading `## Code Intelligence`.
It documents how skills interact with Serena MCP servers and notes any
per-instance limitations.

#### Required content

1. **Tool naming convention**: Explain that Serena tools are prefixed by
   instance name: `mcp__<instance>__<tool>`. For example, if the Serena
   instance is `serena-trustify`, the `find_symbol` tool is called as
   `mcp__serena-trustify__find_symbol`.

2. **Per-instance limitations**: List any known limitations for specific
   Serena instances. This allows skills to adapt their behavior without
   hardcoding workarounds.

#### Structure

```markdown
## Code Intelligence

Tools are prefixed by Serena instance name: `mcp__<instance>__<tool>`.

For example, to search for a symbol in a repository whose Serena instance
is `serena-example`:

    mcp__serena-example__find_symbol(
      name_path_pattern="MyService",
      substring_matching=true,
      include_body=false
    )

### Limitations

- `<instance-name>`: <limitation description>
```

#### How skills use it

- "Check the Code Intelligence section of the project CLAUDE.md for
  per-instance limitations before using Serena tools."
- "Construct Serena tool calls by combining the instance name from the
  Repository Registry with the tool name: `mcp__<instance>__<tool>`."

---

## Extensibility

Projects may add optional sections to `# Project Configuration` beyond
the three required ones. Common examples:

- **Figma Configuration** — Figma file IDs, team/project context for design extraction
- **Deployment Configuration** — environment names, deployment targets
- **Content Formatting** — Jira ADF formatting guidance, comment templates

Skills should not fail if they encounter unknown sections — they simply
ignore them. Skills should not fail if optional fields within required
sections are absent — they adapt gracefully.

---

## Complete Example

Below is a complete `# Project Configuration` section for a Trustify
project. A new project adopter can use this as a starting template,
replacing the values with their own.

```markdown
# Project Configuration

## Repository Registry

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| trustify | Rust backend | serena-trustify | /home/dev/repos/trustify |
| trustify-ui | TypeScript frontend | serena-trustify-ui | /home/dev/repos/trustify-ui |
| trustify-helm-charts | Helm charts / YAML | serena-trustify-helm-charts | /home/dev/repos/trustify-helm-charts |
| scale-testing | Rust scale/perf tests | serena-scale-testing | /home/dev/repos/scale-testing |

## Jira Configuration

- Project key: TC
- Cloud ID: https://issues.redhat.com
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_12310220

## Code Intelligence

Tools are prefixed by Serena instance name: `mcp__<instance>__<tool>`.

For example, to search for a symbol in the trustify backend:

    mcp__serena-trustify__find_symbol(
      name_path_pattern="SbomService",
      substring_matching=true,
      include_body=false
    )

### Limitations

- `serena-trustify-helm-charts`: The YAML language server does not support
  `textDocument/references`, so `find_referencing_symbols` will fail with
  error `-32601`. Use `search_for_pattern` instead for impact analysis on
  Helm chart files.
```

---

## Validation Checklist

Use this checklist to verify a project's CLAUDE.md correctly implements
the contract:

- [ ] `# Project Configuration` heading exists
- [ ] `## Repository Registry` contains a table with columns: Repository, Role, Serena Instance, Path
- [ ] Every listed Serena Instance corresponds to a configured MCP server
- [ ] `## Jira Configuration` contains at minimum: Project key, Cloud ID, Feature issue type ID
- [ ] `## Code Intelligence` documents the `mcp__<instance>__<tool>` naming convention
- [ ] `## Code Intelligence` lists any per-instance limitations under a `### Limitations` subheading
- [ ] All Serena instance names in the Registry match those referenced in Code Intelligence limitations
