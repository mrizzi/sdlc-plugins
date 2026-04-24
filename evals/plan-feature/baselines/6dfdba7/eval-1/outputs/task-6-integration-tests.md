## Repository
trustify-backend

## Description
Write comprehensive integration tests for the advisory severity summary endpoint covering all acceptance criteria from TC-9001: successful aggregation with correct counts, 404 for unknown SBOMs, threshold filtering, advisory deduplication, and response header validation. These tests run against a real PostgreSQL test database following the existing test patterns in the project.

## Files to Modify
- `tests/api/sbom.rs` — Add integration test functions for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint

## Implementation Notes
- Follow the test patterns established in `tests/api/sbom.rs` (existing SBOM endpoint tests) and `tests/api/advisory.rs` (advisory endpoint tests). These tests likely:
  1. Set up a test database with fixtures (SBOM records, advisory records, sbom_advisory join records)
  2. Start a test server instance
  3. Make HTTP requests using a test client (e.g., `reqwest` or axum's test utilities)
  4. Assert on response status codes and JSON body content using `assert_eq!(resp.status(), StatusCode::OK)` pattern
- Test cases to implement:
  1. **Happy path**: Create an SBOM with linked advisories at varying severities, call the endpoint, assert counts match expected values
  2. **Empty advisories**: Create an SBOM with no linked advisories, assert all counts are 0 and total is 0
  3. **SBOM not found**: Call endpoint with a random UUID, assert 404 response
  4. **Deduplication**: Link the same advisory to an SBOM multiple times (if the schema allows), assert it is counted once
  5. **Threshold filter**: Create an SBOM with advisories at all severity levels, call with `?threshold=high`, assert only critical and high counts are non-zero, medium and low are 0
  6. **Cache header**: Assert response includes `Cache-Control` header with `max-age=300`
- For test data setup, reference how `tests/api/sbom.rs` creates SBOM fixtures and how `tests/api/advisory.rs` creates advisory fixtures. The `sbom_advisory` join records can be inserted directly or through the ingestion service.
- Use the entity definitions from `entity/src/sbom.rs`, `entity/src/advisory.rs`, and `entity/src/sbom_advisory.rs` for constructing test data.

## Reuse Candidates
- `tests/api/sbom.rs` — Existing test setup and helper functions for SBOM test fixtures
- `tests/api/advisory.rs` — Test patterns for advisory-related assertions
- `entity/src/sbom_advisory.rs` — Entity for creating test join table records

## Acceptance Criteria
- [ ] At least 5 integration test cases covering the scenarios described above
- [ ] All tests pass against the test database
- [ ] Tests verify both response status codes and JSON body content
- [ ] Tests verify the Cache-Control response header
- [ ] Tests cover the optional threshold query parameter

## Test Requirements
- [ ] Test: valid SBOM returns 200 with correct severity counts in JSON
- [ ] Test: non-existent SBOM returns 404
- [ ] Test: SBOM with no advisories returns all-zero counts
- [ ] Test: duplicate advisory links are counted once (deduplication)
- [ ] Test: threshold parameter filters severity counts correctly
- [ ] Test: response includes Cache-Control header with max-age=300

## Verification Commands
- `cargo test -p trustify-tests --test sbom` — should pass all tests including the new ones

## Dependencies
- Depends on: Task 3 — Advisory summary endpoint (endpoint must exist to test it)
- Depends on: Task 4 — Response caching (cache headers must be set to verify them)
