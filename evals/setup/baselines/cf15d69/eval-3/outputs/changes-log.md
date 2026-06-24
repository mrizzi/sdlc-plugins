# Changes Log

## Summary

Created new `# Project Configuration` section for CLAUDE.md. The existing CLAUDE.md had no Project Configuration — all sections were created from scratch.

## Sections Added

### 1. Repository Registry
- **Action**: Created with table headers only (no rows)
- **Reason**: No Serena MCP servers were discovered; user chose to continue without code intelligence

### 2. Jira Configuration
- **Action**: Created with three required fields populated via manual entry
- **Fields set**:
  - Project key: MYPROJ
  - Cloud ID: abc123
  - Feature issue type ID: 10001
- **Fields omitted** (user had none):
  - Git Pull Request custom field
  - GitHub Issue custom field
- **Note**: Jira Field Defaults subsection not created — no MCP or REST API available to discover priorities and fixVersions

### 3. Code Intelligence
- **Action**: Created with notice that no Serena servers are configured
- **Limitations subsection**: Created with note that no limitations are known

### 4. Bug Configuration
- **Action**: Created with all three required fields
- **Fields set**:
  - Bug issue type ID: 10001
  - Bug template: docs/bug-template.md
  - Bug-to-Task link type: Blocks
- **Note**: Bug template file copy skipped (simulation mode)

### 5. Hierarchy Configuration
- **Action**: Created with default epic grouping strategy
- **Fields set**:
  - Default epic grouping strategy: by-sub-feature

## Sections Skipped

### Security Configuration
- **Reason**: User declined to enable security triage

### Jira Field Defaults
- **Reason**: No Atlassian MCP or REST API available to discover priority and fixVersion values

## Files Not Modified (Simulation Mode)

- `docs/constraints.md` — would have been created from constraints template
- `docs/bug-template.md` — would have been created from bug template
- `CONVENTIONS.md` — not applicable (no repositories in Registry)
