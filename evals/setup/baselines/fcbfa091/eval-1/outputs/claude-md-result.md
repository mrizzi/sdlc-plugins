<!-- SYNTHETIC TEST DATA — CLAUDE.md with no Project Configuration, simulating a greenfield project -->

# my-project

A web application for managing inventory.

## Documentation

- [docs/architecture.md](docs/architecture.md) — System architecture overview
- [docs/api.md](docs/api.md) — REST API reference

## Getting Started

1. Clone the repository
2. Run `npm install`
3. Run `npm start`

# Project Configuration

## Repository Registry

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend |
| trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui |

## Jira Configuration

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

## Code Intelligence

Tools are prefixed by Serena instance name: `mcp__<instance>__<tool>`.

For example, to search for a symbol in the backend repository:

    mcp__serena_backend__find_symbol(
      name_path_pattern="MyService",
      substring_matching=true,
      include_body=false
    )

For example, to search for a symbol in the UI repository:

    mcp__serena_ui__find_symbol(
      name_path_pattern="MyComponent",
      substring_matching=true,
      include_body=false
    )

### Limitations

No limitations known for either Serena instance.

## Bug Configuration

- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

## Hierarchy Configuration

- Default epic grouping strategy: by-sub-feature
