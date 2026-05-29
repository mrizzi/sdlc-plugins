## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the improved search functionality, covering full-text search ranking, filter combinations, performance characteristics, and backward compatibility. This task ensures the search improvements from TC-9002 are verified end-to-end against a real PostgreSQL test database, following the project's established integration testing pattern.

## Files to Modify
- `tests/api/search.rs` — Extend existing search integration tests with new test cases for full-text ranking, filtering, filter combinations, edge cases, and backward compatibility

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/sbom.rs` and `tests/api/advisory.rs` — tests hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` pattern.
- Test data setup: create test SBOMs, advisories, and packages with known text content and severity values so that ranking and filtering can be deterministically verified.
- For ranking tests: insert records with varying degrees of text match (exact title match, partial title match, description-only match) and verify the response order reflects the expected ranking.
- For filter tests: verify each filter individually and in combination, including edge cases (empty results, all filters active, contradictory filters).
- For backward compatibility: verify that requests without the new filter parameters return the same results as before the changes.
- For performance: while we cannot set strict latency assertions in integration tests, verify that searches with indexes complete without timeout and return correct results.
- Per docs/constraints.md §5.11: Add a doc comment to every test function.
- Per docs/constraints.md §5.12: Add given-when-then inline comments to non-trivial test functions.
- Per docs/constraints.md §5.9: Prefer parameterized tests when multiple test cases exercise the same behavior with different inputs (e.g., testing each entity type filter).
- Per docs/constraints.md §2.1-2.3: Commits must reference TC-9002, follow Conventional Commits, and include the AI assistance trailer.

## Reuse Candidates
- `tests/api/search.rs` — Existing search tests showing the established test setup and assertion patterns
- `tests/api/sbom.rs` — SBOM integration tests demonstrating test data creation and response validation patterns
- `tests/api/advisory.rs` — Advisory integration tests demonstrating the project's test conventions

## Acceptance Criteria
- [ ] Integration tests exist for full-text search ranking (exact match > partial match > description match)
- [ ] Integration tests exist for each filter type (entity_type, severity, date_from, date_to)
- [ ] Integration tests exist for filter combinations
- [ ] Integration tests verify backward compatibility (no filters = same behavior as before)
- [ ] Integration tests verify error responses for invalid filter values
- [ ] All test functions have doc comments
- [ ] Non-trivial test functions have given-when-then inline comments
- [ ] All integration tests pass against the PostgreSQL test database

## Test Requirements
- [ ] Ranking test: insert 3+ records with varying match quality, search, and verify order matches expected ranking
- [ ] Entity type filter test: search with entity_type=sbom and verify only SBOMs are returned
- [ ] Severity filter test: search with severity=high and verify only matching advisories are returned
- [ ] Date range filter test: search with date bounds and verify only records within range are returned
- [ ] Combined filter test: search with entity_type + severity and verify correct intersection
- [ ] Invalid filter test: search with entity_type=invalid and verify 400 response
- [ ] No-filter test: search without any new parameters and verify results match pre-change behavior
- [ ] Empty results test: search with filters that match no records and verify empty paginated response

## Verification Commands
- `cargo test --test api search` — all search integration tests pass

## Dependencies
- Depends on: Task 3 — Search filters (requires the filter endpoint changes to be in place)
