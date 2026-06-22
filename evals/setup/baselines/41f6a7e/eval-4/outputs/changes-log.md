# Changes Log

## Summary

Updated Project Configuration in CLAUDE.md with the following changes:

## Changes Made

### 1. Repository Registry -- added new entry

Added a new row for the `serena_ui` Serena instance:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui |

Existing entry for trustify-backend (serena_backend) was preserved without modification.

### 2. Code Intelligence -- added limitation for new instance

Added limitation entry under `### Limitations`:

- `serena_ui`: No limitations known.

All existing Code Intelligence content was preserved without modification.

### 3. Bug Configuration -- new section

Created new `## Bug Configuration` section with the following fields:

- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

Bug template file copy was skipped (simulation mode).

## No Changes

The following sections were already up to date and were preserved as-is:

- **Jira Configuration** -- all required and optional fields already populated
- **Code Intelligence** (existing content) -- tool naming convention and existing limitations preserved

## Sections Not Created

- **Security Configuration** -- user declined when offered the security triage opt-in
- **Hierarchy Configuration** -- hierarchy discovery not exercised in this simulation
