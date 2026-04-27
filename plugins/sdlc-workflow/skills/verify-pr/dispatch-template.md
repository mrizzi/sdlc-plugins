# Dispatch Template

Structured input template for dispatching domain sub-agents during verify-pr
execution. The orchestrator constructs one dispatch envelope per sub-agent,
filling in the sections below. All sub-agents receive the same envelope
structure; the Agent-Specific Inputs section varies per agent.

## Template

````markdown
## Sub-Agent Dispatch: <agent name>

### Context
- **Jira Task:** <task key>
- **PR:** <PR URL>
- **Branch:** <branch name>
- **Base Branch:** <base branch name>

### Classified Review Comments

<all classified comments with IDs, classifications, and file/line references>

### Agent-Specific Inputs

<varies per agent -- see Agent-Specific Input Sections below>

### Instructions

<sub-agent skill file content>

### Output Template

<finding-template.md content>
````

## Agent-Specific Input Sections

### Intent Alignment

- `### PR Diff Summary` — file list with per-file line counts (additions/deletions), not full diff content
- `### Task Specification` — Repository, Files to Modify, Files to Create sections from Jira task description
- `### Jira Task ID` — the task key for commit traceability checking
- `### PR Commits` — commit list with hashes and messages

### Security

- `### PR Diff` — full diff content for line-level pattern scanning

### Correctness

- `### PR Diff` — full diff content for code inspection
- `### Task Specification` — Acceptance Criteria, Test Requirements, Verification Commands sections from Jira task description
- `### Repository Info` — repository path and Serena instance info for code inspection
- `### CI Status` — note to fetch CI status via `gh` CLI (not pre-fetched; sub-agent fetches on demand)

### Style/Conventions

- `### PR Diff` — full diff content for code inspection
- `### CONVENTIONS.md` — full content of the repository's CONVENTIONS.md
- `### Test Files` — list of modified/deleted test file paths
- `### Branch Names` — base branch and PR branch names for test change classification sub-agent

## Rules

- Context section and Classified Review Comments are mandatory for all sub-agents
- Agent-Specific Inputs section includes only the sections listed for that sub-agent
- Instructions section contains the full content of the sub-agent's skill file (e.g., `intent-alignment.md`)
- Output Template section contains the full content of `finding-template.md`
