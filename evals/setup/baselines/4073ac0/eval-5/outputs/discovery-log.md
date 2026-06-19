# Setup Discovery Log

## MCP Tool Discovery

### Serena Instances

Discovered 2 Serena instances from the MCP tool listing:

1. **serena_backend** — identified by `mcp__serena_backend__*` tool prefix (10 tools: find_symbol, get_symbols_overview, search_for_pattern, find_referencing_symbols, replace_symbol_body, insert_after_symbol, insert_before_symbol, rename_symbol, get_diagnostics, list_dir)
2. **serena_ui** — identified by `mcp__serena_ui__*` tool prefix (10 tools: same set as serena_backend)

### Atlassian MCP

Discovered Atlassian MCP tools from the tool listing:

- mcp__atlassian__jira_get_issue
- mcp__atlassian__jira_search_issues
- mcp__atlassian__jira_edit_issue
- mcp__atlassian__jira_transition_issue
- mcp__atlassian__jira_add_comment
- mcp__atlassian__jira_user_info

Atlassian MCP presence confirms Jira integration is available.

## User-Provided Configuration

### Repository Mapping

User provided repository details for each discovered Serena instance:

- **serena_backend** -> repository 'backend', role 'Rust backend service', path '/home/user/backend'
- **serena_ui** -> repository 'frontend-ui', role 'TypeScript frontend', path '/home/user/frontend-ui'

No known limitations reported for either Serena instance.

### Jira Configuration

User provided the following Jira configuration fields:

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### Bug Configuration

- Bug issue type ID: 10001 (discovered from Jira metadata)
- Bug template path: docs/bug-template.md (user accepted default)
- Bug-to-Task link type: Blocks (user accepted default)

### Security Configuration

- User was asked whether to enable security triage and **accepted**
- All Product Lifecycle fields were collected from user input:
  - Product pages URL: https://access.example.com/product-lifecycle
  - Jira version prefix: MYPRODUCT
  - Vulnerability issue type ID: 10200
  - Component label pattern: pscomponent:
  - VEX Justification custom field: customfield_12345

### Version Streams

Collected 1 version stream from user:

| Stream | Konflux Release Repo | Local Path | Security Matrix Path |
|---|---|---|---|
| 2.1.x | git.downstream.example.com/my-org/product-release.2.1.z | /home/user/product-release.2.1.z | security-matrix.md |

### Source Repositories

Collected 2 source repositories from user:

| Repository | URL |
|---|---|
| backend | https://github.com/example/backend |
| frontend-ui | https://github.com/example/frontend-ui |

### Optional Steps

- User **declined** supportability matrix population
- Security-matrix.md scaffolding was skipped
