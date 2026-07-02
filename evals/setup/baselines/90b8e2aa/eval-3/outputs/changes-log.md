# Changes Log

## Summary

Greenfield setup — no existing Project Configuration section was found in CLAUDE.md. All sections below were newly added.

## Added Sections

### 1. Project Configuration (new)

Top-level `# Project Configuration` heading added to anchor all configuration subsections.

### 2. Repository Registry (new)

Empty registry table added with headers (Repository, Role, Serena Instance, Path) and no data rows. No Serena MCP servers were discovered and the user chose to continue without code intelligence, so no repositories were registered.

```markdown
| Repository | Role | Serena Instance | Path |
|---|---|---|---|
```

### 3. Jira Configuration (new)

Added with three fields provided via manual entry:
- Project key: MYPROJ
- Cloud ID: abc123
- Feature issue type ID: 10001

The following optional fields were not provided and were omitted:
- Git Pull Request custom field
- GitHub Issue custom field

### 4. Code Intelligence (new)

Added with placeholder text indicating that no Serena MCP servers are configured and code intelligence is not available.

### 5. Limitations (new)

Added under Code Intelligence with default text indicating no limitations are known since no Serena instances are configured.

### 6. Bug Configuration (new)

Added with three fields:
- Bug issue type ID: 10001 (provided manually by user)
- Bug template: docs/bug-template.md (user accepted default)
- Bug-to-Task link type: Blocks (user accepted default)

Bug template file copy was skipped (simulation mode).

## Sections Not Added

### Security Configuration — declined

The user was offered the Security Configuration opt-in and declined. No Security Configuration section was added.

## Preserved Content

- No existing content was modified (the original CLAUDE.md had no Project Configuration section)
- No MCP tools were called (none available for Serena or Atlassian)
- No Bash commands were executed
