# Changes Log

## Preserved Content

The following existing sections from the original CLAUDE.md were preserved unchanged:

- **Header**: `# my-project` and project description
- **Documentation**: Links to architecture.md and api.md
- **Getting Started**: Setup instructions (clone, npm install, npm start)

## Added Sections

The following Project Configuration sections were added to the end of the CLAUDE.md:

### 1. Repository Registry (new)
- Added table with 2 repository entries:
  - `backend` (Rust backend service) mapped to Serena instance `serena_backend` at `/home/user/backend`
  - `frontend-ui` (TypeScript frontend) mapped to Serena instance `serena_ui` at `/home/user/frontend-ui`

### 2. Jira Configuration (new)
- Added project key: TC
- Added cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Added feature issue type ID: 10142
- Added Git Pull Request custom field: customfield_10875
- Added GitHub Issue custom field: customfield_10747

### 3. Code Intelligence (new)
- Added tool usage examples for both Serena instances (`serena_backend`, `serena_ui`)
- Added Limitations subsection noting no known limitations for either instance

### 4. Bug Configuration (new)
- Added bug issue type ID: 10001
- Added bug template path: docs/bug-template.md
- Added Bug-to-Task link type: Blocks

### 5. Security Configuration (new)
- Added Product Lifecycle subsection with product pages URL, Jira version prefix, vulnerability issue type ID, component label pattern, and VEX justification custom field
- Added Version Streams table with 1 entry (2.1.x stream)
- Added Source Repositories table with 2 entries (backend, frontend-ui)

## Summary

- Sections preserved: 3 (header/description, Documentation, Getting Started)
- Sections added: 5 (Repository Registry, Jira Configuration, Code Intelligence, Bug Configuration, Security Configuration)
- Sections modified: 0
- Sections removed: 0
