# Changes Log

## Sections Added

All sections below are newly added to the CLAUDE.md under `# Project Configuration`:

1. **Repository Registry** — Added table with 2 repositories:
   - `backend` (serena_backend) — Rust backend service at /home/user/backend
   - `frontend-ui` (serena_ui) — TypeScript frontend at /home/user/frontend-ui

2. **Jira Configuration** — Added with 5 fields:
   - Project key: TC
   - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
   - Feature issue type ID: 10142
   - Git Pull Request custom field: customfield_10875
   - GitHub Issue custom field: customfield_10747

3. **Code Intelligence** — Added with tool naming convention documentation (`mcp__<instance>__<tool>`) and example using serena_backend. Includes Limitations subsection (no limitations known).

4. **Bug Configuration** — Added with 3 fields:
   - Bug issue type ID: 10001
   - Bug template: docs/bug-template.md
   - Bug-to-Task link type: Blocks

5. **Security Configuration** — Added with 3 subsections:
   - **Product Lifecycle** — 5 fields configured (Product pages URL, Jira version prefix, Vulnerability issue type ID, Component label pattern, VEX Justification custom field)
   - **Version Streams** — 1 stream configured (2.1.x with Konflux release repo, local path, and security matrix path)
   - **Source Repositories** — 2 repositories configured (backend, frontend-ui)

## Sections Not Added

- **Hierarchy Configuration** — Not included (no user input provided for epic grouping strategy)
- **Jira Field Defaults** — Not included (no user input provided for default priority, fixVersion scope, or prompt settings)

## Files Modified

- `CLAUDE.md` — Project Configuration section appended (simulation: written to outputs/claude-md-result.md)

## Files Not Modified

- Bug template file (docs/bug-template.md) — copy skipped per simulation instructions
- security-matrix.md — scaffolding skipped per user preference
