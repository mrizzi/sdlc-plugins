# Changes Log

## What Was Added

The following sections were created from scratch since the existing CLAUDE.md had no Project Configuration:

### 1. Project Configuration (top-level heading)
- **Added**: `# Project Configuration` heading — did not previously exist

### 2. Repository Registry
- **Added**: `## Repository Registry` section with table
- **Added**: Row for `trustify-backend` (Rust backend service, serena_backend, /home/user/trustify-backend)
- **Added**: Row for `trustify-ui` (TypeScript frontend, serena_ui, /home/user/trustify-ui)

### 3. Jira Configuration
- **Added**: `## Jira Configuration` section with all fields:
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Feature issue type ID: 10142
  - Git Pull Request custom field: customfield_10875
  - GitHub Issue custom field: customfield_10747

### 4. Code Intelligence
- **Added**: `## Code Intelligence` section documenting the MCP tool naming convention
- **Added**: Example using `serena_backend` instance
- **Added**: `### Limitations` subsection noting no known limitations

### 5. Bug Configuration
- **Added**: `## Bug Configuration` section with all fields:
  - Bug issue type ID: 10001
  - Bug template: docs/bug-template.md
  - Bug-to-Task link type: Blocks

### 6. Hierarchy Configuration
- **Added**: `## Hierarchy Configuration` section with:
  - Default epic grouping strategy: by-sub-feature

## What Was Preserved

- All existing content from the original CLAUDE.md was preserved:
  - `# my-project` heading and description
  - `## Documentation` section with links to architecture.md and api.md
  - `## Getting Started` section with setup instructions

## What Was Not Created

- **Security Configuration**: User declined to enable security triage — section not created
- **Bug template file**: File copy skipped per simulation instructions
- **Constraints document**: Not copied per simulation instructions (no Bash commands)
- **CONVENTIONS.md**: Not scaffolded per simulation instructions (no Bash commands)
