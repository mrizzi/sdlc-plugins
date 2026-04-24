# Task 5 — Add integration tests for advisory summary endpoint

## Repository
trustify-backend

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Tests should cover the primary success path, error cases, deduplication behavior, threshold filtering, and response shape validation. These tests follow the existing integration test patterns in the `tests/api/` directory, hitting a real PostgreSQL test database.

## Files to Modify
- `tests/api/sbom.rs` — add advisory summary endpoint tests to the existing SBOM test file (or create a new dedicated test file if the existing file is already large)

## Files to Create
- `tests/api/advisory_summary.rs` — (optional, if a dedicated test file is preferred for organization) dedicated integration tests for the advisory summary endpoint

## Implementation Notes
- Follow the integration test patterns established in `tests/api/sbom.rs` and `tests/api/advisory.rs`:
  - Use `assert_eq!(resp.status(), StatusCode::OK)` pattern for status assertions.
  - Hit a real PostgreSQL test database — tests should set up SBOM and advisory fixture data, link them via the `sbom_advisory` join table, then call the endpoint and assert the response.
- Test data setup should:
  - Create an SBOM via the ingestion service or direct entity insertion
  - Create advisories at various severity levels (critical, high, medium, low)
  - Link advisories to the SBOM via the `sbom_advisory` join entity
- Verify the JSON response shape matches `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` exactly.
- For deduplication testing: link the same advisory to the SBOM twice and verify it is counted only once.
- For threshold testing: call with `?threshold=high` and verify only critical and high counts are non-zero (or that medium and low are excluded).
- For 404 testing: call with a random UUID that does not correspond to any SBOM and verify `StatusCode::NOT_FOUND`.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM integration tests; follow their test setup, HTTP client usage, and assertion patterns
- `tests/api/advisory.rs` — advisory integration tests; reference for advisory fixture data creation patterns

## Acceptance Criteria
- [ ] Integration test for successful advisory summary retrieval with correct counts
- [ ] Integration test for 404 response on non-existent SBOM ID
- [ ] Integration test for deduplication (same advisory linked twice yields count of 1)
- [ ] Integration test for threshold filtering (`?threshold=critical`, `?threshold=high`)
- [ ] Integration test for SBOM with no advisories (all counts are 0, total is 0)
- [ ] Integration test for response JSON shape validation
- [ ] All tests pass against the test database

## Test Requirements
- [ ] Test: GET /api/v2/sbom/{id}/advisory-summary returns 200 with correct severity breakdown for an SBOM with mixed-severity advisories
- [ ] Test: GET /api/v2/sbom/{id}/advisory-summary returns 404 for non-existent SBOM
- [ ] Test: duplicate advisory links do not inflate counts
- [ ] Test: threshold=critical returns only critical count > 0, others are 0
- [ ] Test: threshold=high returns critical and high counts, medium and low are 0
- [ ] Test: SBOM with zero advisories returns { critical: 0, high: 0, medium: 0, low: 0, total: 0 }

## Verification Commands
- `cargo test --test api advisory_summary` — all integration tests should pass
- `cargo test --test api sbom::advisory_summary` — if tests are added to the existing sbom test file

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint
