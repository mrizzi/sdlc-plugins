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
| Repository | Short name of the repository (e.g., `backend`) |
| Role | Brief description: language and purpose (e.g., "Rust backend") |
| Serena Instance | The MCP server instance name (e.g., `serena-backend`) |
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
| Project key | The Jira project key used in issue IDs | `PROJ` |
| Cloud ID | The Jira instance URL or cloud UUID | `https://mycompany.atlassian.net` |
| Feature issue type ID | Numeric ID for the Feature issue type | `10001` |

#### Optional fields

| Field | Description | Example |
|---|---|---|
| Git Pull Request custom field | Custom field ID for storing PR URLs (requires ADF format) | `customfield_10001` |
| GitHub Issue custom field | Custom field ID containing a GitHub issue URL (plain string or ADF) | `customfield_10002` |
| Default labels | Labels to apply to AI-generated issues | `ai-generated-jira` |

#### Optional subsection: REST API Credentials (MCP Fallback)

When Atlassian MCP is unavailable due to organizational policies, skills can fall back to JIRA REST API v3. This subsection stores the credentials needed for REST API access.

| Field | Description | Example |
|---|---|---|
| Server URL | JIRA Cloud instance URL | `https://mycompany.atlassian.net` |
| Email | Atlassian account email | `user@example.com` |
| API Token | API token or environment variable reference | `$JIRA_API_TOKEN` (recommended) or actual token |

**Storage modes:**
- **Environment variable (recommended)**: Store `$JIRA_API_TOKEN` reference in CLAUDE.md, actual token in shell environment
- **Plaintext (less secure)**: Store actual token directly in CLAUDE.md

**Important**: Credentials are only collected when MCP fails and user explicitly chooses to use REST API fallback. Skills always prompt before using REST API, even if credentials are already stored.

#### Structure

```markdown
## Jira Configuration

- Project key: PROJ
- Cloud ID: https://mycompany.atlassian.net
- Feature issue type ID: 10001
- Git Pull Request custom field: customfield_10001
- GitHub Issue custom field: customfield_10002

### REST API Credentials (MCP Fallback)
- Server URL: https://mycompany.atlassian.net
- Email: user@example.com
- API Token: $JIRA_API_TOKEN
```

#### How skills use it

- "Use the Jira project key from Project Configuration when creating issues."
- "Use the Cloud ID as the `cloudId` parameter in all Jira MCP tool calls."
- "Use the Feature issue type ID when creating feature-level issues."
- "If a Git Pull Request custom field is configured, update it with the PR URL."
- "If a GitHub Issue custom field is configured, read it from the Jira issue and add a `Closes` reference to the PR description."
- "If Atlassian MCP fails, always prompt user to use REST API fallback. If user chooses REST API, check for `.env` file in repository root first (recommended), then fallback to CLAUDE.md REST API Credentials subsection (legacy). If credentials present, use them; if absent, collect credentials from user and optionally store them in .env file."

---

### 3. Code Intelligence

The Code Intelligence section is under the heading `## Code Intelligence`.
It documents how skills interact with Serena MCP servers and notes any
per-instance limitations.

#### Required content

1. **Tool naming convention**: Explain that Serena tools are prefixed by
   instance name: `mcp__<instance>__<tool>`. For example, if the Serena
   instance is `serena-backend`, the `find_symbol` tool is called as
   `mcp__serena-backend__find_symbol`.

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

## Optional Sections

### 4. Security Configuration

The Security Configuration section is under the heading
`## Security Configuration`. It provides the project-specific settings
that the `triage-security` skill needs to perform CVE triage across
supported product versions. This section is scaffolded by the `setup`
skill's optional Security Configuration step.

#### Required subsections

**`### Product Lifecycle`**

| Field | Required | Description | Example |
|---|---|---|---|
| Product pages URL | Yes | Product lifecycle page for EOL/support status checks | `https://lifecycle.example.com/products/myproduct` |
| Jira version prefix | Yes | Filters Jira versions to this product | `MYPRODUCT` |
| Vulnerability issue type ID | Yes | Jira issue type ID for Vulnerability issues | `10001` |
| Component label pattern | Yes | Label prefix used by PSIRT to identify affected components | `pscomponent:` |
| VEX Justification custom field | No | Custom field ID for VEX justification on not-affected closures | `customfield_00000` |

**`### Version Streams`**

A table mapping each supported version stream to its Konflux release repo
and security matrix file path.

| Column | Description | Example |
|---|---|---|
| Stream | Version stream label | `2.2.x` |
| Konflux Release Repo | Git repository URL (used in Forward Pointers) | `git.downstream.example.com/.../product-release.0.4.z` |
| Local Path | User's local clone path | `/path/to/product-release.0.4.z` |
| Security Matrix Path | Path to security-matrix.md within the repo | `docs/security-matrix.md` |

At least one row is required.

**`### Source Repositories`**

A table listing each source repository whose dependencies are tracked
for CVE analysis.

| Column | Description | Example |
|---|---|---|
| Repository | Short name of the source repo | `backend` |
| URL | Repository URL | `https://github.com/my-org/backend` |

At least one row is required. Each source repository generates a
corresponding commit column in the Supportability Matrix within
`security-matrix.md` — the column names are dynamic, matching the
repository names listed here.

#### Structure

```markdown
## Security Configuration

### Product Lifecycle

- Product pages URL: https://lifecycle.example.com/products/myproduct
- Jira version prefix: MYPRODUCT
- Vulnerability issue type ID: 10001
- Component label pattern: pscomponent:
- VEX Justification custom field: customfield_00000

### Version Streams

| Stream | Konflux Release Repo | Local Path | Security Matrix Path |
|---|---|---|---|
| 2.1.x | git.downstream.example.com/.../product-release.0.3.z | /path/to/product-release.0.3.z | docs/security-matrix.md |
| 2.2.x | git.downstream.example.com/.../product-release.0.4.z | /path/to/product-release.0.4.z | docs/security-matrix.md |

### Source Repositories

| Repository | URL |
|---|---|
| backend | https://github.com/my-org/backend |
| frontend-ui | https://github.com/my-org/frontend-ui |
```

#### How skills use it

- "`triage-security` reads Product Lifecycle fields to filter Jira
  versions and identify PSIRT component labels."
- "`triage-security` follows Version Streams to load security-matrix.md
  from each Konflux release repo and chain across streams via forward
  pointers."
- "`triage-security` uses Source Repositories to identify which repos'
  lock files to inspect for dependency versions."
- "`setup` scaffolds this section interactively using
  `security-config.template.md`."

---

## Extensibility

Projects may add optional sections to `# Project Configuration` beyond
the required and optional ones documented above. Common examples:

- **Figma Configuration** — Figma file IDs, team/project context for design extraction
- **Deployment Configuration** — environment names, deployment targets
- **Content Formatting** — Jira ADF formatting guidance, comment templates

Skills should not fail if they encounter unknown sections — they simply
ignore them. Skills should not fail if optional fields within required
sections are absent — they adapt gracefully.

---

## Template

The canonical template for the `# Project Configuration` section is
maintained in the `/setup` skill at
[plugins/sdlc-workflow/skills/setup/project-config.template.md](../plugins/sdlc-workflow/skills/setup/project-config.template.md).

Replace the `{{placeholder}}` markers with your project's actual values.
Running `/setup` performs this automatically by discovering your MCP
servers and prompting for any missing information.

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
- [ ] (If present) `## Security Configuration` contains `### Product Lifecycle` with all four required fields (VEX Justification is optional)
- [ ] (If present) `## Security Configuration` contains `### Version Streams` with at least one row
- [ ] (If present) `## Security Configuration` contains `### Source Repositories` with at least one row
