## Repository
sdlc-plugins

## Description
Root-cause: strengthen implement-task skill to verify that multi-table write operations are wrapped in database transactions. The implement-task skill should include a check that when a service method performs multiple related database writes (INSERT, UPDATE, DELETE across different tables), those writes are enclosed in a transaction block. This is a universal analysis method -- "check whether related writes are wrapped in a transaction" -- that applies to any database-backed codebase regardless of framework or language.

## Files to Modify
- `plugins/sdlc-workflow/skills/implement-task/SKILL.md` — add a verification step in the implementation phase that checks for transactional consistency when generating service methods with multiple related database write operations

## Implementation Notes
- The gap was exposed during verification of TC-9103, where the `soft_delete` method performed three sequential UPDATE statements (on `sbom`, `sbom_package`, and `sbom_advisory` tables) without wrapping them in a transaction
- The implement-task skill should recognize the pattern of "multiple related writes" and ensure they are grouped in a transaction
- This is a method-level check (language-agnostic): "when generating code that performs multiple related database writes, wrap them in a transaction"
- The check should apply during the code generation phase, not as a post-hoc verification

## Acceptance Criteria
- [ ] implement-task skill documentation includes guidance to wrap multiple related database writes in a transaction
- [ ] The guidance is expressed as a universal method, not tied to a specific ORM or language

## Dependencies
- Depends on: TC-9103 — Add SBOM deletion endpoint (root-cause source)
