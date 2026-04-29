# Task 4 — Expand Search Integration Tests for Performance, Relevance, and Filters

## Repository
trustify-backend

## Description
Expand the existing search integration test suite to comprehensively cover the new search capabilities: full-text search with GIN indexes (performance), relevance-based ranking, and filter parameters. This ensures that the search improvements are verified end-to-end against a real PostgreSQL test database, following the established integration test patterns in the repository.

## Files to Modify
- `tests/api/search.rs` — add integration tests covering relevance ordering, filter parameter combinations, edge cases (empty results, invalid filters), and performance characteristics of indexed search

## Implementation Notes
- The existing integration test file at `tests/api/search.rs` contains search endpoint tests. Add new test functions to this file rather than creating new files, following the existing test organization pattern.
- Follow the established test pattern: tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` for status assertions (as documented in the repository conventions).
- Test data setup: create test SBOMs, advisories, and packages with known text content so that relevance ordering can be verified deterministically. Use entities with varying degrees of search term presence to verify ranking.
- Test filter validation: verify that invalid `entity_type`, `severity`, and date format values return 400 status codes with appropriate error messages.
- Test filter combinations: verify AND logic when multiple filters are applied simultaneously.
- Test edge cases: empty search query with filters only, filters that match no results, date ranges with no matching entities.
- Per `docs/constraints.md` section 5.11: every test function must have a doc comment.
- Per `docs/constraints.md` section 5.12: non-trivial tests must include given-when-then inline comments.
- Per `docs/constraints.md` section 5.9: prefer parameterized tests when multiple test cases exercise the same behavior with different inputs.
- Per `docs/constraints.md` section 2 (Commit Rules): commit must reference TC-9002 and follow Conventional Commits.

## Reuse Candidates
- `tests/api/search.rs` — existing search integration tests; follow their setup patterns and assertion style
- `tests/api/sbom.rs` — SBOM integration tests for reference on test data creation patterns
- `tests/api/advisory.rs` — advisory integration tests for reference on entity creation and assertion patterns

## Acceptance Criteria
- [ ] Integration tests verify relevance-ordered results (most relevant result appears first)
- [ ] Integration tests verify each filter type independently (entity_type, severity, date_from, date_to)
- [ ] Integration tests verify filter combinations (multiple filters applied simultaneously)
- [ ] Integration tests verify invalid filter parameter handling (400 responses)
- [ ] Integration tests verify edge cases (no results, empty query with filters)
- [ ] All new tests pass against the PostgreSQL test database
- [ ] All pre-existing search tests continue to pass (no regressions)

## Test Requirements
- [ ] Test: relevance ordering — create entities with different levels of search term density, verify ordering matches expected relevance
- [ ] Test: entity type filter — verify each entity type filter returns only the correct entity type
- [ ] Test: severity filter — verify severity filter returns only matching advisories
- [ ] Test: date range filter — verify date range boundaries are inclusive and correct
- [ ] Test: combined filters — verify AND logic across entity_type + severity, entity_type + date_range
- [ ] Test: invalid filter values — verify 400 response for unknown entity_type, invalid severity, malformed dates
- [ ] Test: empty results — verify correct empty response structure when filters match nothing

## Verification Commands
- `cargo test --test api search` — all search integration tests pass

## Dependencies
- Depends on: Task 3 — Add Filter Parameters to Search Endpoint
