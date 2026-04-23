## Repository
trustify-backend

## Description
Write comprehensive integration tests in `tests/api/search.rs` that validate the full improved search behavior: ranked full-text results (Task 2) and filter query parameters (Task 3). These tests run against a real PostgreSQL test database and confirm that the MVP requirements — faster relevance-ranked results and working filters — are verifiably correct before the feature is shipped.

This task also adds a basic performance assertion to give a quantitative signal that the GIN index (Task 1) is providing the expected speedup, fulfilling the "search should be faster" requirement in a measurable way.

**Assumptions pending clarification**:
- The existing test harness in `tests/api/search.rs` already sets up a test PostgreSQL database and HTTP test client. This task extends the existing test file rather than creating a new harness.
- Performance assertions will use wall-clock timing (`std::time::Instant`) with a loose upper bound (e.g. 200 ms for a single search against a seeded dataset of 500 rows) rather than `EXPLAIN ANALYZE`. A more rigorous benchmark is out of scope until performance targets are clarified (see Ambiguity 1 in the impact map).

## Files to Modify
- `tests/api/search.rs` — add test cases for ranked results, filter parameters, edge cases, and a timing assertion

## Implementation Notes
Follow the existing pattern in `tests/api/sbom.rs` and `tests/api/advisory.rs`: use `assert_eq!(resp.status(), StatusCode::OK)` for status checks and deserialize response bodies into the appropriate result struct.

Structure the new tests as follows:

**Ranked results test**: Insert two SBOMs — one where the query term appears in `name`, one where it appears only in `description`. Assert that the name-match ranks first in the response array. Use a deterministic dataset (fixed names/descriptions) so the ranking expectation is stable.

**Filter tests**:
- Insert an advisory with `severity = "critical"` and one with `severity = "low"`. Issue `GET /api/v2/search?q=<shared-term>&severity=critical` and assert only the critical advisory is returned.
- Insert a package with `license = "MIT"` and one with `license = "Apache-2.0"`. Issue `GET /api/v2/search?q=<shared-term>&license=MIT` and assert only the MIT package is returned.

**Edge case tests**:
- Empty query string: assert the response is HTTP 400 or an empty result (whichever the implementation chooses — confirm in Task 2 implementation).
- Query with no matching documents: assert HTTP 200 with `total: 0`.
- Filter value with no matching documents: assert HTTP 200 with `total: 0`.

**Timing assertion**: Seed the database with 500 advisory rows sharing a common term. Measure wall-clock time for `GET /api/v2/search?q=<common-term>` and assert it completes in under 500 ms. Use `std::time::Instant::now()` and `elapsed()`.

The `PaginatedResults<T>` deserialization type is already used in existing tests; reuse the same deserializer.

## Reuse Candidates
- `tests/api/sbom.rs` — reference for test database setup, HTTP client construction, and `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern
- `tests/api/advisory.rs` — reference for inserting advisory test fixtures and asserting on deserialized `AdvisorySummary` fields, including `severity`
- `common/src/model/paginated.rs::PaginatedResults` — response type to deserialize search results into for assertions

## Acceptance Criteria
- [ ] All new tests pass with `cargo test -p tests search`
- [ ] The ranked results test reliably places the name-match before the description-match (not flaky)
- [ ] Each filter test asserts both that matching results are present and that non-matching results are absent
- [ ] The timing assertion passes on the CI database (i.e. 500 ms budget is achievable with GIN index in place)
- [ ] No existing tests in `tests/api/search.rs` are broken or removed

## Test Requirements
- [ ] Test: ranked full-text results — name-match ranks above description-match
- [ ] Test: `?severity=<value>` filter — returns only matching advisories
- [ ] Test: `?license=<value>` filter — returns only matching packages
- [ ] Test: combined `?severity=&license=` filters — applies both predicates
- [ ] Test: empty result set — query matching no documents returns HTTP 200 with `total: 0`
- [ ] Test: unknown filter value — returns HTTP 200 with `total: 0`, not 400 or 500
- [ ] Test: timing assertion — 500-row dataset search completes within 500 ms

## Verification Commands
- `cargo test -p tests search -- --nocapture` — all search tests pass and timing output is visible
- `cargo test -p tests` — full test suite passes (no regressions in sbom or advisory tests)

## Dependencies
- Depends on: Task 2 — Refactor SearchService to use ranked full-text search
- Depends on: Task 3 — Add filter query parameters to the search endpoint
