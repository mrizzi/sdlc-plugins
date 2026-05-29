# Changes Log

## Context

This is a greenfield setup. The existing CLAUDE.md had no Project Configuration section, so all content below is newly added.

## Preserved (unchanged)

The existing CLAUDE.md content was preserved as-is:
- `# my-project` heading and project description
- `## Documentation` section with links to architecture and API docs
- `## Getting Started` section with setup instructions

## Added

### Project Configuration section (new)

The entire `# Project Configuration` section was added, containing:

1. **Repository Registry** — table with 2 entries:
   - trustify-backend (Rust backend service, serena_backend, /home/user/trustify-backend)
   - trustify-ui (TypeScript frontend, serena_ui, /home/user/trustify-ui)

2. **Jira Configuration** — 5 fields:
   - Project key: TC
   - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
   - Feature issue type ID: 10142
   - Git Pull Request custom field: customfield_10875
   - GitHub Issue custom field: customfield_10747

3. **Code Intelligence** — usage instructions with Serena tool prefix convention and example call

4. **Limitations** — noted that no limitations are known for either Serena instance
