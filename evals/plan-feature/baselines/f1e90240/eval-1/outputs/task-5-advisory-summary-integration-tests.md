# Task 5: Add integration tests for advisory-summary endpoint

**Jira Parent**: TC-9001
**Priority**: Major
**Fix Versions**: RHTPA 1.5.0

## Repository

trustify-backend

## Target Branch

main

## Description

Add integration tests that exercise the full `GET /api/v2/sbom/{id}/advisory-summary` endpoint against a real PostgreSQL test database. Tests must cover successful aggregation, missing SBOM (404), deduplication of advisories, threshold filtering, and cache header verification. Follow the existing integration test patterns in `tests/api/`.

## Acceptance Criteria

- [ ] Integration test: valid SBOM with multiple advisories at different severities returns correct counts
- [ ] Integration test: nonexistent SBOM ID returns 404 status
- [ ] Integration test: SBOM with no linked advisories returns all-zero counts
- [ ] Integration test: duplicate advisory links produce deduplicated counts
- [ ] Integration test: `?threshold=high` returns only critical and high counts (medium and low are zero)
- [ ] Integration test: response includes `Cache-Control` header with `max-age=300`
- [ ] All tests follow existing patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs`

## Test Requirements

- [ ] All tests use the PostgreSQL test database infrastructure from the existing test harness
- [ ] Tests create test fixtures (SBOMs, advisories, sbom_advisory links) as setup
- [ ] Tests assert on HTTP status codes using `assert_eq!(resp.status(), StatusCode::OK)` pattern
- [ ] Tests assert on JSON response body structure and values

## Dependencies

- Task 3 (advisory-summary endpoint) -- the endpoint must be implemented before integration tests can run
- Task 4 (cache invalidation) -- cache invalidation must be in place for cache-related tests

## Files to Create

- `tests/api/sbom_advisory_summary.rs` -- integration test module for the advisory-summary endpoint

## Files to Modify

- `tests/Cargo.toml` -- add any additional test dependencies if needed (should not be needed if existing test infrastructure suffices)

## Implementation Notes

- Follow the test structure in `tests/api/sbom.rs` which tests SBOM endpoints against a real PostgreSQL test database using `assert_eq!(resp.status(), StatusCode::OK)`.
  - Applies: task creates `tests/api/sbom_advisory_summary.rs` matching the convention's testing scope.
- Set up test data by inserting SBOM records, advisory records with different severity levels, and `sbom_advisory` join records via the entities in `entity/src/sbom.rs`, `entity/src/advisory.rs`, and `entity/src/sbom_advisory.rs`.
- For threshold filtering tests, verify that the response JSON contains zero values for severities below the threshold.
