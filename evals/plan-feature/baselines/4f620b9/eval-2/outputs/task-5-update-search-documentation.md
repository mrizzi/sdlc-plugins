## Repository
trustify-backend

## Target Branch
main

## Description
Update the project documentation to reflect the improved search capabilities introduced by TC-9002, including full-text search behavior and the new filter query parameters. This ensures that API consumers and developers understand the updated search endpoint contract.

## Files to Modify
- `README.md` — add or update the search API section to document full-text search behavior and filter parameters

## Implementation Notes
- Document the updated `GET /api/v2/search` endpoint with all supported query parameters:
  - `q` (string) — full-text search query, parsed using PostgreSQL's `websearch_to_tsquery` or `plainto_tsquery`
  - `entity_type` (string, optional) — filter by entity type: `sbom`, `advisory`, `package`
  - `severity` (string, optional) — filter advisories by severity level
  - `created_after` (ISO 8601 date, optional) — return only entities created after this date
  - `created_before` (ISO 8601 date, optional) — return only entities created before this date
- Document that results are ranked by relevance when a search query is provided.
- Document that all filter parameters are optional and combinable.
- Document backward compatibility: existing API consumers who do not send filter parameters will see no behavior change.
- Per docs/constraints.md §2 (Commit Rules): every commit must reference TC-9002, follow Conventional Commits, and include `--trailer="Assisted-by: Claude Code"`.
- Per docs/constraints.md §3 (PR Rules): branch must be named after the Jira issue ID; after opening a PR, post its link as a comment on the Jira task.

## Acceptance Criteria
- [ ] README.md documents the full-text search behavior of `GET /api/v2/search`
- [ ] README.md documents all supported filter query parameters with types and descriptions
- [ ] README.md includes usage examples for common search and filter scenarios
- [ ] Documentation accurately reflects the implemented API contract

## Test Requirements
- [ ] Documentation review: verify all documented parameters match the implemented endpoint
- [ ] Documentation review: verify example requests return expected results when executed against the running service

## Dependencies
- Depends on: Task 3 — Add search filter parameters (documentation must reflect the final implemented API contract)

[sdlc-workflow] Description digest: sha256-md:c4a72e4b44fec2cc238db3591ec00bef98d1909c830d4a34aa3e7e971b7adb93
