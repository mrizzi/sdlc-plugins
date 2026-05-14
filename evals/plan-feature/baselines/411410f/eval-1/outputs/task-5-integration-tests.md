## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. These tests exercise the full request lifecycle against a real PostgreSQL test database, covering success cases, error cases, deduplication, threshold filtering, and cache headers. This task consolidates all end-to-end testing for the feature.

## Files to Create
- `tests/api/sbom_advisory_summary.rs` — Integration test module for the advisory summary endpoint. Contains test functions for each scenario described below.

## Files to Modify
- `tests/Cargo.toml` — Add `sbom_advisory_summary` to the test target configuration if the project requires explicit test file registration (check whether existing test files like `tests/api/sbom.rs` are auto-discovered or manually listed).

## Implementation Notes
- Follow the test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs` for test setup: database connection, test data seeding, HTTP client construction, and assertion style (`assert_eq!(resp.status(), StatusCode::OK)`).
- Use the same test harness and fixtures as existing tests. Seed test data by:
  1. Inserting an SBOM record via the SBOM ingestion service or direct entity insert
  2. Inserting advisory records at various severity levels (at least one of each: critical, high, medium, low)
  3. Linking advisories to the SBOM via `sbom_advisory` join table records
- For the deduplication test, insert the same advisory ID linked to the same SBOM multiple times (or through different relationship paths) and verify it is counted only once.
- For the threshold test, use `?threshold=critical` and verify only the critical count is non-zero in the response, while other levels are excluded or zero.
- For the 404 test, use a random UUID that does not correspond to any SBOM.
- For cache header verification, check that the response includes a `cache-control` header with `max-age=300`.
- Structure tests as individual `#[tokio::test]` async functions, each with descriptive names following the existing convention (e.g., `test_advisory_summary_returns_severity_counts`, `test_advisory_summary_not_found`, etc.).

## Acceptance Criteria
- [ ] Test file `tests/api/sbom_advisory_summary.rs` exists and compiles
- [ ] All tests pass against the PostgreSQL test database
- [ ] Tests cover: successful aggregation, 404 for missing SBOM, deduplication, threshold filtering, and cache headers

## Test Requirements
- [ ] `test_advisory_summary_returns_severity_counts` — Seed an SBOM with 2 critical, 3 high, 1 medium, 4 low advisories; assert response is `{ "critical": 2, "high": 3, "medium": 1, "low": 4, "total": 10 }`
- [ ] `test_advisory_summary_not_found` — Request summary for a non-existent SBOM UUID; assert 404 response
- [ ] `test_advisory_summary_deduplication` — Link the same advisory to an SBOM twice; assert it is counted only once in the response
- [ ] `test_advisory_summary_threshold_critical` — Request with `?threshold=critical`; assert only critical count is returned and total equals critical count
- [ ] `test_advisory_summary_threshold_high` — Request with `?threshold=high`; assert critical and high counts are returned and total equals their sum
- [ ] `test_advisory_summary_empty_sbom` — Request summary for an SBOM with no linked advisories; assert `{ "critical": 0, "high": 0, "medium": 0, "low": 0, "total": 0 }`
- [ ] `test_advisory_summary_cache_headers` — Assert response includes `cache-control` header with `max-age=300`

## Dependencies
- Depends on: Task 3 — Advisory summary endpoint (the endpoint must be implemented and registered before integration tests can run)
