## Repository
sdlc-plugins

## Description
Improve the plan-feature skill to include transactional integrity guidance when a task involves multiple related database operations that must succeed or fail atomically. The plan-feature skill should detect when Implementation Notes describe cascade or multi-table update operations and add explicit guidance about wrapping those operations in a database transaction.

Additionally, improve the implement-task skill's code analysis to detect when multiple related database writes (updates, inserts, or deletes across multiple tables) are performed sequentially without transactional protection, and proactively wrap them in a transaction.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — add guidance for detecting multi-table write operations in task descriptions and including transactional integrity notes
- `plugins/sdlc-workflow/skills/implement-task/SKILL.md` — add a code analysis check for multi-table write operations that should be wrapped in transactions

## Implementation Notes
- In plan-feature: when generating Implementation Notes that describe cascade updates, multi-table deletes, or related write operations, include a note about transactional integrity (e.g., "Wrap cascade operations in a single database transaction to ensure atomicity")
- In implement-task: during code generation, when multiple `.exec()` or equivalent database write calls target different tables within a single function, verify they are wrapped in a transaction scope
- This is a method-level improvement (language-agnostic analysis technique), not a language-specific fact

## Acceptance Criteria
- [ ] plan-feature generates transactional integrity notes when task describes multi-table write operations
- [ ] implement-task detects sequential multi-table writes and wraps them in transactions
