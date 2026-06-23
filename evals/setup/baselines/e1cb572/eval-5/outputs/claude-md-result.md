# Project Configuration

## Repository Registry

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| backend | Rust backend service | serena_backend | /home/user/backend |
| frontend-ui | TypeScript frontend | serena_ui | /home/user/frontend-ui |

## Jira Configuration

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

## Code Intelligence

Tools are prefixed by Serena instance name: `mcp__<instance>__<tool>`.

For example, to search for a symbol in the backend repository whose Serena instance
is `serena_backend`:

    mcp__serena_backend__find_symbol(
      name_path_pattern="MyService",
      substring_matching=true,
      include_body=false
    )

### Limitations

No limitations known -- no Serena instances reported issues.

## Bug Configuration

- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

## Security Configuration

### Product Lifecycle

- Product pages URL: https://access.example.com/product-lifecycle
- Jira version prefix: MYPRODUCT
- Vulnerability issue type ID: 10200
- Component label pattern: pscomponent:
- VEX Justification custom field: customfield_12345

### Version Streams

| Stream | Konflux Release Repo | Local Path | Security Matrix Path |
|---|---|---|---|
| 2.1.x | git.downstream.example.com/my-org/product-release.2.1.z | /home/user/product-release.2.1.z | security-matrix.md |

### Source Repositories

| Repository | URL |
|---|---|
| backend | https://github.com/example/backend |
| frontend-ui | https://github.com/example/frontend-ui |
