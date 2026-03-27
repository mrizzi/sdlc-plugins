# Task Description Template

All Jira tasks created by SDLC workflow skills must follow this template.
Skills that create tasks (plan-feature, verify-pr) produce this format;
skills that consume tasks (implement-task) parse it.

## Template

```
## Repository
<repository-name>

## Description
<What this task achieves and why>

## Files to Modify
- `path/to/file.ext` — <brief reason>

## Files to Create
- `path/to/new_file.ext` — <purpose>

## API Changes
- `GET /v2/endpoint` — NEW: <description>
- `PUT /v2/endpoint/{id}` — MODIFY: <what changes in request/response>

## Implementation Notes
<Specific guidance: patterns to follow, existing code to reuse,
key functions/structs/components to interact with.
Reference actual file paths and symbol names found during repository analysis.>

## Reuse Candidates
- `path/to/file.ext::symbol_name` — <what it does and how it relates to this task>

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Test Requirements
- [ ] Test description 1
- [ ] Test description 2

## Verification Commands
- `<command>` — <expected outcome>

## Documentation Updates
- `path/to/doc.md` — <what content to add or revise>

## Dependencies
- Depends on: Task N — <task title> (if any)
```

## Rules

- Omit sections that don't apply (e.g. no API Changes for a pure UI task, no Files
  to Create if only modifying, no Documentation Updates if no docs are impacted)
- Repository must be a single repository per task
- File paths must be real paths discovered during repository or code analysis
- Implementation Notes must reference existing patterns, not abstract guidance —
  when reusable utilities, helpers, or shared modules exist, list them with file
  paths and symbol names so the implementer can reuse them instead of writing new code
- Reuse Candidates is optional — include it when existing code (domain logic,
  components, utilities, or patterns) overlaps with the planned changes, so the
  implementer has an explicit checklist of code to consider reusing
- Each task must be small enough for a single engineer to implement
- Verification Commands are optional — include them when acceptance criteria can be
  verified by running a command against the built or running service
- Documentation Updates is optional — include it when the task changes public APIs,
  configuration, setup steps, or architectural patterns, listing which docs need
  updating and what content to add or revise (not the actual doc content)

## Extension sections

Individual skills may add context-specific sections beyond the base template.
These extensions are documented in the skill that produces them:

- **Target PR** — used by verify-pr (Step 4e) for review feedback fixes, so
  implement-task adds commits to an existing PR branch
- **Review Context** — used by verify-pr (Step 4e) to capture the original review
  comment text and PR file/line reference
