## Repository
trustify-backend

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. These tests validate the full request-response cycle against a real PostgreSQL test database, covering the success path, 404 handling, severity deduplication, threshold filtering, and response shape. This task consolidates end-to-end test coverage that exercises the model, service, and endpoint layers together.

## Files to Create
- `tests/api/advisory_summary.rs` — integration tests for the advisory-summary endpoint

## Files to Modify
- `tests/Cargo.toml` — add the new test file to the test harness if needed (depending on test discovery configuration)

## Implementation Notes
- Follow the integration test pattern established in `tests/api/sbom.rs` and `tests/api/advisory.rs`: tests hit a real PostgreSQL test database, use the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern, and set up test data using the ingestion pipeline or direct entity insertion.
- Test setup should:
  1. Create a test SBOM via the ingestion pipeline or direct database insertion
  2. Create test advisories with known severity levels (e.g., 2 critical, 3 high, 1 medium, 1 low)
  3. Link advisories to the SBOM via the `sbom_advisory` join table
- Include a deduplication test case: link the same advisory to the SBOM multiple times and verify the count reflects unique advisories, not duplicates.
- Include a threshold filtering test: call with `?threshold=high` and verify that only critical and high counts are non-zero.
- Include a 404 test: call with a non-existent SBOM ID and verify the response status is 404.
- Verify the response JSON shape matches `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`.

## Reuse Candidates
- `tests/api/sbom.rs` — demonstrates integration test setup for SBOM-related endpoints: test database initialization, SBOM creation, HTTP request construction, response assertions
- `tests/api/advisory.rs` — demonstrates advisory entity setup in tests; reuse the test data creation patterns for advisories with specific severity levels

## Acceptance Criteria
- [ ] Integration tests exist in `tests/api/advisory_summary.rs`
- [ ] Tests cover: successful response with correct counts, 404 for missing SBOM, deduplication of advisory IDs, threshold filtering, correct JSON response shape
- [ ] All tests pass against the PostgreSQL test database
- [ ] Test assertions use the established `assert_eq!(resp.status(), StatusCode::...)` pattern

## Test Requirements
- [ ] Test: GET /api/v2/sbom/{id}/advisory-summary returns 200 with correct severity counts for an SBOM with known advisories
- [ ] Test: GET /api/v2/sbom/{id}/advisory-summary returns 404 for a non-existent SBOM ID
- [ ] Test: advisory deduplication — linking the same advisory multiple times does not inflate counts
- [ ] Test: threshold=critical returns only critical count as non-zero
- [ ] Test: threshold=high returns critical and high counts, medium and low are zero
- [ ] Test: response JSON shape includes all expected fields (critical, high, medium, low, total)

## Verification Commands
- `cargo test --test api advisory_summary` — all advisory summary integration tests should pass

## Dependencies
- Depends on: Task 3 — Advisory summary REST endpoint
- Depends on: Task 5 — Cache invalidation on advisory ingestion
