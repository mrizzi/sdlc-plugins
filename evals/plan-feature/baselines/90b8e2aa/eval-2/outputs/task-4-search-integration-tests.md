## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive end-to-end integration tests for all search improvements introduced by TC-9002 (performance, relevance ranking, and filtering). While individual tasks include their own test requirements, this task ensures cross-cutting test coverage: scenarios that exercise multiple new capabilities simultaneously (e.g., filtered search with relevance ordering), regression tests for backward compatibility, and performance baseline validation.

## Files to Modify
- `tests/api/search.rs` — add integration test functions covering combined search scenarios, regression cases, and performance validation

## Implementation Notes
- Follow the existing test pattern in `tests/api/search.rs` which uses a real PostgreSQL test database and the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern. Applies: task modifies `tests/api/search.rs` matching the convention's Rust test file scope.
- Test data setup: insert known SBOMs, advisories, and packages with controlled text content so that relevance ordering and filter behavior can be deterministically verified.
- Combined scenario tests should exercise filters and ranking together — e.g., search with `entity_type=advisory` and a query string, verifying that results are filtered to advisories AND ordered by relevance.
- Regression tests should verify that existing search behavior (no filters, no query string) produces the same results as before the changes.
- Performance validation tests should assert that search queries complete within a reasonable time bound — note that integration tests against a test database may not reflect production-scale performance, so these serve as smoke tests rather than definitive benchmarks.
- Reference existing test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs` for test setup, fixture insertion, and assertion patterns.

## Reuse Candidates
- `tests/api/search.rs` — existing search integration tests showing the established test pattern, request construction, and assertion style
- `tests/api/sbom.rs` — SBOM integration tests demonstrating test data setup and response validation patterns
- `tests/api/advisory.rs` — advisory integration tests demonstrating entity-specific test patterns

## Acceptance Criteria
- [ ] Integration tests cover combined filter + relevance ranking scenarios
- [ ] Integration tests verify backward compatibility (existing search behavior unchanged when no new parameters are used)
- [ ] Integration tests cover edge cases: empty search results with filters, filters with no query string, query string with no filters
- [ ] All new tests pass against a PostgreSQL test database
- [ ] No existing tests are broken by the new test additions

## Test Requirements
- [ ] Test: search with query string and entity_type filter returns filtered results ordered by relevance
- [ ] Test: search with query string, date range, and severity filters returns correctly filtered and ranked results
- [ ] Test: search with only filters (no query string) returns filtered results in default order
- [ ] Test: search with no parameters returns all results (backward compatibility regression test)
- [ ] Test: search with contradictory filters (e.g., entity_type=sbom and severity filter) returns appropriate result (empty set or error depending on implementation)

## Verification Commands
- `cargo test -p tests --test search` — all search integration tests pass

## Dependencies
- Depends on: Task 1 — Add database indexes for search query performance
- Depends on: Task 2 — Implement search result relevance ranking
- Depends on: Task 3 — Add filter parameters to search endpoint
