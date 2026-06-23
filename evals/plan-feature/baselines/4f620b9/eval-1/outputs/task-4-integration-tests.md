## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint in the existing test suite. These tests validate the full request-response cycle including correct severity counting, advisory deduplication, 404 handling, threshold filtering, and cache behavior, ensuring the endpoint meets all acceptance criteria from the feature requirements.

## Files to Modify
- `tests/api/sbom.rs` — add integration test functions for the advisory summary endpoint

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/sbom.rs` (SBOM endpoint integration tests) and `tests/api/advisory.rs` (advisory endpoint integration tests). These tests hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` pattern.
- Test setup should create test SBOMs and advisories at each severity level (critical, high, medium, low) using the existing test helper patterns. Link advisories to SBOMs via the `sbom_advisory` join table.
- Test cases to implement:
  1. **Success response**: create an SBOM with known advisories at each severity, call the endpoint, verify the response JSON matches expected counts
  2. **SBOM not found**: call with a non-existent SBOM ID, verify 404 response
  3. **Deduplication**: link the same advisory to an SBOM through multiple paths, verify it is counted only once
  4. **Empty advisories**: create an SBOM with no linked advisories, verify response returns all zeros with total 0
  5. **Threshold filtering**: call with `?threshold=critical`, verify only critical count is returned; call with `?threshold=high`, verify critical and high counts are returned
  6. **P95 performance baseline**: for an SBOM with 500 advisories, verify response time is under 200ms (soft assertion / logging)
- Per CONVENTIONS.md §Testing: place tests in `tests/api/` and use the real PostgreSQL test database pattern.
  Applies: task modifies `tests/api/sbom.rs` matching the convention's test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM integration tests; follow the same setup/teardown patterns for test database management
- `tests/api/advisory.rs` — existing advisory integration tests; reference for how advisories are created and linked in test fixtures
- `common/src/model/paginated.rs::PaginatedResults` — reference for how other test assertions validate response types

## Acceptance Criteria
- [ ] All integration tests pass against a PostgreSQL test database
- [ ] Test coverage includes: success case, 404, deduplication, empty advisories, threshold filtering
- [ ] Tests follow existing patterns in `tests/api/sbom.rs`

## Test Requirements
- [ ] Integration test: `GET /api/v2/sbom/{id}/advisory-summary` returns correct counts for an SBOM with advisories at all severity levels
- [ ] Integration test: `GET /api/v2/sbom/{id}/advisory-summary` returns 404 for non-existent SBOM
- [ ] Integration test: duplicate advisories linked to the same SBOM are counted only once
- [ ] Integration test: SBOM with no advisories returns zero counts
- [ ] Integration test: `?threshold=critical` returns only critical count
- [ ] Integration test: `?threshold=high` returns critical and high counts

## Verification Commands
- `cargo test --test api -- sbom::advisory_summary` — expected: all advisory summary tests pass
- `cargo test --test api` — expected: all existing SBOM and advisory tests continue to pass (no regressions)

## Dependencies
- Depends on: Task 2 — Add advisory summary endpoint with caching

[sdlc-workflow] Description digest: sha256-md:f78dd48475abcb0e31f9d09d0375d60e34a9546008cc304b18bf6291927062f0
