<!-- SYNTHETIC TEST DATA — mock CLAUDE.md with Security Configuration including Embargo policy URL for triage-security eval testing -->

# rhtpa

## Documentation

- [docs/architecture.md](docs/architecture.md) — System architecture overview

# Project Configuration

## Repository Registry

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| rhtpa-backend | Rust backend service | serena_backend | /home/dev/repos/rhtpa-backend |

## Jira Configuration

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

## Code Intelligence

Serena MCP servers provide code intelligence for repository analysis.

### Tool naming convention

Tools are called as `mcp__<serena-instance>__<tool>`.

### Configured instances

| Serena Instance | Repository | Language Server |
|---|---|---|
| serena_backend | rhtpa-backend | rust-analyzer |

### Limitations

- rust-analyzer may take 30-60 seconds to index on first use

## Security Configuration

### Product Lifecycle

- Product pages URL: https://access.example.com/product-life-cycle/rhtpa
- Jira version prefix: RHTPA
- Vulnerability issue type ID: 10024
- Component label pattern: pscomponent:
- VEX Justification custom field: customfield_12345
- Embargo policy URL: https://example.com/security/embargo-policy

### Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

### Source Repositories

| Repository | URL | Local Path |
|------------|-----|------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend |
