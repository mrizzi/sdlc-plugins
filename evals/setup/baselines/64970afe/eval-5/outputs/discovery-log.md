# Setup Discovery Log

## Step 1 -- Read Existing Configuration

- Read fixture CLAUDE.md at `evals/setup/files/claude-md-empty.md`
- No `# Project Configuration` section found -- all sections need to be created
- No Repository Registry, Jira Configuration, Code Intelligence, Bug Configuration, Security Configuration, or Hierarchy Configuration present

## Step 2 -- Discover Serena Instances

Examined available MCP tools from `evals/setup/files/mcp-tools-with-serena.md`.

Discovered 2 Serena instances:
1. **serena_backend** -- tools: `mcp__serena_backend__find_symbol`, `mcp__serena_backend__get_symbols_overview`, `mcp__serena_backend__search_for_pattern`, `mcp__serena_backend__find_referencing_symbols`, `mcp__serena_backend__replace_symbol_body`, `mcp__serena_backend__insert_after_symbol`, `mcp__serena_backend__insert_before_symbol`, `mcp__serena_backend__rename_symbol`, `mcp__serena_backend__get_diagnostics`, `mcp__serena_backend__list_dir`
2. **serena_ui** -- tools: `mcp__serena_ui__find_symbol`, `mcp__serena_ui__get_symbols_overview`, `mcp__serena_ui__search_for_pattern`, `mcp__serena_ui__find_referencing_symbols`, `mcp__serena_ui__replace_symbol_body`, `mcp__serena_ui__insert_after_symbol`, `mcp__serena_ui__insert_before_symbol`, `mcp__serena_ui__rename_symbol`, `mcp__serena_ui__get_diagnostics`, `mcp__serena_ui__list_dir`

Also discovered: Atlassian MCP tools (prefixed `mcp__atlassian__`)

User-provided repository details:
- serena_backend: repository name = `backend`, role = `Rust backend service`, path = `/home/user/backend`
- serena_ui: repository name = `frontend-ui`, role = `TypeScript frontend`, path = `/home/user/frontend-ui`

## Step 3 -- Jira Configuration

No existing Jira Configuration found. All fields need to be collected.

User-provided Jira configuration:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

## Step 4 -- Jira Field Defaults

Skipped -- MCP discovery not available in simulation mode. No user-provided defaults.

## Step 5 -- Code Intelligence

No existing Code Intelligence section found. Generated section with:
- Tool naming convention explanation: `mcp__<instance>__<tool>`
- Concrete example using first Serena instance: `serena_backend`
- Limitations: No limitations reported for either instance

## Step 7 -- Copy Constraints Template

Skipped -- simulation mode, no file operations performed.

## Step 8 -- Scaffold CONVENTIONS.md

Skipped -- simulation mode, no file operations performed.

## Step 9 -- Bug Configuration

No existing Bug Configuration found. All fields need to be collected.

- Bug issue type ID: 10001 (discovered from Jira metadata)
- Bug template path: docs/bug-template.md (user accepted default)
- Bug-to-Task link type: Blocks (user accepted default)
- Bug template file copy: skipped (simulation mode)

## Step 10 -- Security Configuration

No existing Security Configuration found. User accepted opt-in to enable security triage.

### Step 10.1 -- Product Lifecycle fields

User-provided values:
- Product pages URL: https://access.example.com/product-lifecycle
- Jira version prefix: MYPRODUCT
- Vulnerability issue type ID: 10200
- Component label pattern: pscomponent:
- VEX Justification custom field: customfield_12345
- Upstream Affected Component custom field: (not provided, skipped)
- PS Component custom field: (not provided, skipped)
- Stream custom field: (not provided, skipped)
- ProdSec contact email: (not provided, skipped)
- ProdSec Jira account ID: (not provided, skipped)
- Embargo policy URL: (not provided, skipped)

### Step 10.2 -- Version Streams

Collected 1 version stream:
| Stream | Konflux Release Repo | Local Path | Security Matrix Path |
|---|---|---|---|
| 2.1.x | git.downstream.example.com/my-org/product-release.2.1.z | /home/user/product-release.2.1.z | security-matrix.md |

### Step 10.3 -- Source Repositories

Collected 2 source repositories:
| Repository | URL | Deployment Context |
|---|---|---|
| backend | https://github.com/example/backend | upstream |
| frontend-ui | https://github.com/example/frontend-ui | upstream |

### Step 10.5 -- Scaffold security-matrix.md

Skipped -- user declined security-matrix.md scaffolding.

### Step 10.6 -- Populate supportability matrix

Skipped -- user declined supportability matrix population.

## Step 11 -- Validation

Verified the generated Project Configuration contains:
- [x] `# Project Configuration` heading exists
- [x] `## Repository Registry` contains table with columns: Repository, Role, Serena Instance, Path
- [x] Repository Registry has 2 entries: backend, frontend-ui
- [x] `## Jira Configuration` contains: Project key (TC), Cloud ID, Feature issue type ID (10142)
- [x] `## Jira Configuration` contains optional fields: Git Pull Request custom field, GitHub Issue custom field
- [x] `## Code Intelligence` documents `mcp__<instance>__<tool>` naming convention
- [x] `## Code Intelligence` has `### Limitations` subheading
- [x] `## Bug Configuration` contains: Bug issue type ID (10001), Bug template (docs/bug-template.md), Bug-to-Task link type (Blocks)
- [x] `## Security Configuration` contains `### Product Lifecycle` with all four required fields
- [x] `## Security Configuration` contains `### Product Lifecycle` with optional VEX Justification field
- [x] `## Security Configuration` contains `### Version Streams` with 1 row
- [x] `## Security Configuration` contains `### Source Repositories` with 2 rows
