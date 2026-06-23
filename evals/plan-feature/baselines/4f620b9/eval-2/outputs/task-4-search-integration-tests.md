## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the improved search functionality, covering full-text search relevance ranking, filter combinations, edge cases, and backward compatibility. This task ensures the search improvements from TC-9002 are thoroughly validated and regression-protected.

## Files to Modify
- `tests/api/search.rs` — add integration tests for full-text search and filtering

## Implementation Notes
- Follow the existing integration test patterns in `tests/api/search.rs`, `tests/api/sbom.rs`, and `tests/api/advisory.rs`.
- Tests should hit a real PostgreSQL test database, consistent with the project's testing convention.
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern established in existing tests.
- Test data setup: insert test SBOMs, advisories, and packages with known names/descriptions to verify search ranking and filtering.
- Verify that full-text search results are ordered by relevance (first result should be the best match).
- Verify filter combinations work correctly (e.g., `entity_type=advisory&severity=critical&q=openssl`).
- Verify edge cases: empty search query, search with no results, filters with no matching entities, invalid date formats.
- Per docs/constraints.md §2 (Commit Rules): every commit must reference TC-9002, follow Conventional Commits, and include `--trailer="Assisted-by: Claude Code"`.
- Per docs/constraints.md §3 (PR Rules): branch must be named after the Jira issue ID; after opening a PR, post its link as a comment on the Jira task.
- Per docs/constraints.md §5 (Code Change Rules): changes must be scoped to listed files; inspect code before modifying; follow patterns in Implementation Notes.
- Per docs/constraints.md §5.11: every test function must have a doc comment.
- Per docs/constraints.md §5.12: non-trivial test functions must include given-when-then inline comments.

## Reuse Candidates
- `tests/api/search.rs` — existing search tests to extend with new test cases
- `tests/api/sbom.rs` — SBOM endpoint integration tests demonstrating test setup, data insertion, and assertion patterns
- `tests/api/advisory.rs` — advisory endpoint integration tests demonstrating the same patterns

## Acceptance Criteria
- [ ] Integration tests cover full-text search with relevance ranking
- [ ] Integration tests cover each filter parameter individually (entity_type, severity, created_after, created_before)
- [ ] Integration tests cover filter combinations
- [ ] Integration tests verify backward compatibility (no filters/no query returns all results)
- [ ] Integration tests cover edge cases (empty query, no results, invalid inputs)
- [ ] All tests pass against a PostgreSQL test database

## Test Requirements
- [ ] Test: full-text search returns results ordered by relevance score
- [ ] Test: entity_type filter returns only matching entity types
- [ ] Test: severity filter returns only advisories with matching severity
- [ ] Test: date range filters return only entities within the specified range
- [ ] Test: combining search query with filters narrows results correctly
- [ ] Test: empty search query with filters returns filtered results
- [ ] Test: search with no matching results returns empty paginated response
- [ ] Test: invalid filter values return appropriate error responses

## Verification Commands
- `cargo test --test search` — all search integration tests pass

## Dependencies
- Depends on: Task 2 — Refactor SearchService for full-text search (tests exercise the refactored search logic)
- Depends on: Task 3 — Add search filter parameters (tests exercise the filter functionality)

[sdlc-workflow] Description digest: sha256-md:21c196f1e89e2eb2c4f6418528f472f9c305c97969f05e1d426cf667bee4795a
