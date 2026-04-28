# Task 5 — Add integration tests for advisory summary endpoint

## Repository
trustify-backend

## Description
Add comprehensive integration tests for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Tests should cover the full request/response lifecycle against a real PostgreSQL test database, consistent with the existing test patterns in `tests/api/`.

## Files to Create
- `tests/api/advisory_summary.rs` — integration tests for the advisory summary endpoint

## Files to Modify
- `tests/Cargo.toml` — add test module if required by the test harness configuration

## Implementation Notes
- Follow the integration test patterns established in `tests/api/sbom.rs` and `tests/api/advisory.rs`: set up test data, make HTTP requests to the endpoint, and assert on response status codes and body content.
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern from existing tests.
- Test setup should:
  1. Create a test SBOM via the ingestion pipeline or direct database insertion
  2. Create advisories with known severity levels (e.g., 2 critical, 3 high, 1 medium, 0 low)
  3. Link advisories to the SBOM via the `sbom_advisory` join table
- Ensure deduplication is tested: link the same advisory to the SBOM through multiple paths and verify it is counted only once.
- For the threshold filter test, verify that `?threshold=high` returns counts for critical and high only (or returns zeros for medium and low, depending on implementation).
- Per constraints doc section 5.11: every test function must have a doc comment.
- Per constraints doc section 5.12: non-trivial test functions must have given-when-then inline comments.

## Reuse Candidates
- `tests/api/sbom.rs` — SBOM endpoint integration test patterns, test setup helpers, database fixtures
- `tests/api/advisory.rs` — advisory endpoint integration test patterns, advisory test data setup
- `tests/api/search.rs` — additional integration test reference for pattern consistency

## Acceptance Criteria
- [ ] Integration tests cover: successful aggregation with correct counts, 404 for non-existent SBOM, deduplication, threshold filtering
- [ ] Tests follow existing patterns in `tests/api/`
- [ ] All tests pass against the PostgreSQL test database
- [ ] Every test function has a doc comment
- [ ] Non-trivial tests have given-when-then inline comments

## Test Requirements
- [ ] Test: `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with correct severity counts for an SBOM with known advisories
- [ ] Test: `GET /api/v2/sbom/{id}/advisory-summary` returns 404 for a non-existent SBOM ID
- [ ] Test: advisory linked through multiple paths is counted only once (deduplication)
- [ ] Test: `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns only critical count (or filtered counts)
- [ ] Test: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns critical and high counts
- [ ] Test: response includes expected cache control headers

## Verification Commands
- `cargo test --test api advisory_summary` — all integration tests should pass

## Dependencies
- Depends on: Task 3 — Add advisory summary endpoint
- Depends on: Task 4 — Add cache invalidation for advisory summaries
