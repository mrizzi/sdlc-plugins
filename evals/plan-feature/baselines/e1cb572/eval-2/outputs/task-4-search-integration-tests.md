# Task 4: Integration Tests for Search Improvements

## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests to `tests/api/search.rs` covering the full-text search ranking, filter query parameters, and performance characteristics introduced by the preceding tasks. These tests validate that the search improvements work end-to-end against a real PostgreSQL test database and serve as the regression baseline for future changes.

**Ambiguity note:** The feature's non-functional requirements state "Should be fast enough" and "Don't break existing functionality" without defining measurable criteria. This task documents that the integration tests in `tests/api/search.rs` serve as the regression baseline per these ambiguous NFRs. No formal latency SLAs or load testing targets are assumed.

**Assumption (pending clarification):** "Don't break existing functionality" is validated by ensuring all pre-existing tests continue to pass and that the search endpoint remains backwards-compatible (no filter parameters = same behavior as before). "Fast enough" is approximated by asserting that search responses complete within a generous timeout (e.g., 5 seconds) in the test environment, but this is not a production SLA.

**Assumption (pending clarification):** The feature does not specify which ranking signals matter most (exact match priority, recency, severity weighting). Tests will assert that exact-match results rank higher than partial matches, as this is the most intuitive relevance behavior, but the precise ranking algorithm is an implementation detail subject to product owner review.

## Files to Modify
- `tests/api/search.rs` — Add new test functions covering full-text search relevance ranking, filter parameter behavior, combined filter scenarios, error handling for invalid filters, and basic performance assertions

## Implementation Notes
- Follow the existing test patterns in `tests/api/search.rs`, `tests/api/sbom.rs`, and `tests/api/advisory.rs`. These tests use a shared test harness that spins up the Axum server against a real PostgreSQL test database.
- Each test function should:
  1. Seed the database with known test data (SBOMs, advisories, and packages with specific names, severities, and creation dates)
  2. Issue HTTP requests to `GET /api/v2/search` with various query and filter parameter combinations
  3. Assert on response status codes, result counts, result ordering, and entity types
- **Relevance ranking tests:**
  - Seed an advisory with title "Critical OpenSSL Vulnerability" and a package named "openssl-utils". Search for `q=openssl`. Assert that results are returned and that exact title matches rank above partial matches.
  - Search for a term that matches no entities. Assert empty results with `200 OK` (not an error).
  - **Assumption (pending clarification):** Ranking order assertions verify relative ordering (result A before result B) rather than absolute rank scores, since the scoring algorithm is not specified.
- **Filter parameter tests:**
  - Seed multiple entity types. Search with `entity_type=advisory` and assert only advisories are returned.
  - Seed advisories with different severities. Search with `severity=critical` and assert only critical advisories are returned.
  - Seed entities with known creation dates. Search with `created_after` and `created_before` and assert only entities within the range are returned.
  - Combine filters: `entity_type=advisory&severity=high&created_after=2024-01-01`. Assert the intersection is returned.
  - Assert that omitting all filters returns results from all entity types (backwards compatibility).
- **Error handling tests:**
  - Send `entity_type=invalid_type` and assert `400 Bad Request`.
  - Send `created_after=not-a-date` and assert `400 Bad Request`.
  - Send `entity_type=sbom&severity=critical` (invalid combination) and assert `400 Bad Request`.
  - Send `created_after=2025-01-01&created_before=2024-01-01` (inverted range) and assert `400 Bad Request`.
- **Performance regression tests:**
  - **Assumption (pending clarification):** No specific latency target is defined. Tests assert that search responses return within 5 seconds in the CI test environment. This is a smoke check, not a production performance guarantee.
  - Use `std::time::Instant` to measure request duration and `assert!(duration < Duration::from_secs(5))`.
  - Seed a moderate dataset (e.g., 100 entities across all types) before running the timing assertion to ensure the test is not trivially fast on an empty database.
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern per project conventions for status code assertions.
- Per CONVENTIONS.md: integration tests live in `tests/api/` and hit a real PostgreSQL test database.
  Applies: task modifies `tests/api/search.rs` matching the convention's integration test scope.

## Reuse Candidates
- `tests/api/search.rs` — Existing search tests for structural patterns and test harness setup
- `tests/api/sbom.rs` — Reference for test data seeding patterns (how to insert SBOMs in the test database)
- `tests/api/advisory.rs` — Reference for advisory test data seeding (including severity values)
- `common/src/model/paginated.rs` — `PaginatedResults<T>` struct for deserializing search responses in test assertions

## Acceptance Criteria
- [ ] At least one test validates that full-text search returns results ranked by relevance (exact matches first)
- [ ] At least one test validates that `entity_type` filter restricts results to the specified type
- [ ] At least one test validates that `severity` filter restricts advisory results to the specified severity
- [ ] At least one test validates that `created_after` / `created_before` filters restrict results to the date range
- [ ] At least one test validates that combined filters produce the correct intersection of results
- [ ] At least one test validates that invalid filter values return `400 Bad Request`
- [ ] At least one test validates backwards compatibility (no filters = all results, same as before)
- [ ] At least one test asserts search response time is under 5 seconds for a moderate dataset (performance smoke check)
- [ ] All pre-existing tests in `tests/api/search.rs` continue to pass
- [ ] `cargo test --test api` passes with no failures

## Test Requirements
- [ ] Tests are self-contained: each test seeds its own data and does not depend on data from other tests
- [ ] Tests clean up after themselves or use isolated transactions that roll back
- [ ] Test names follow the existing naming convention in `tests/api/search.rs` (descriptive snake_case)
- [ ] Tests do not introduce flakiness: avoid timing-sensitive assertions except the explicitly documented 5-second smoke check
- [ ] Tests cover both happy paths and error paths for each filter parameter

## Dependencies
- Depends on: Task 3 — Add filter query parameters to search endpoint (filter parameters must be implemented before they can be tested)

---

`[sdlc-workflow] Description digest: sha256-md:d8f15b3a7c2e904d6a1f83c5b7e29d4f0a6c8e1b3d5f7a92c4e6b0d2f4a8c1e3`
