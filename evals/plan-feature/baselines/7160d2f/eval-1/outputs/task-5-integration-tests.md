## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint covering the main success path, error cases, deduplication behavior, caching, threshold filtering, and cache invalidation after advisory ingestion. These tests exercise the full request-response cycle against a real PostgreSQL test database, consistent with the existing integration test approach.

## Files to Create
- `tests/api/advisory_summary.rs` — integration tests for the advisory-summary endpoint

## Files to Modify
- `tests/Cargo.toml` — add any new test dependencies if needed (likely none if existing test harness suffices)

## Implementation Notes
- Follow the integration test patterns established in `tests/api/sbom.rs` and `tests/api/advisory.rs` — these tests hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern.
- Test setup should:
  1. Create an SBOM via the ingestion pipeline or directly via the database
  2. Create advisories with known severity levels (e.g., 2 critical, 3 high, 1 medium, 0 low)
  3. Link advisories to the SBOM via the `sbom_advisory` join table
- Test cases to implement:
  - **Success case**: GET advisory-summary for an SBOM with known advisories returns correct counts
  - **Empty SBOM**: GET advisory-summary for an SBOM with no linked advisories returns all-zero counts
  - **Non-existent SBOM**: GET advisory-summary with invalid ID returns 404
  - **Deduplication**: Link the same advisory to an SBOM multiple times, verify it is counted only once
  - **Threshold filtering**: Use `?threshold=high` and verify only critical and high counts are returned
  - **Cache headers**: Verify response includes cache-control header with 5-minute max-age
- Reference the existing test utilities and test database setup patterns from `tests/api/sbom.rs` for creating test fixtures.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM integration tests demonstrating test setup, fixture creation, and assertion patterns
- `tests/api/advisory.rs` — existing advisory integration tests demonstrating advisory creation and endpoint testing
- `tests/Cargo.toml` — existing test dependencies configuration

## Acceptance Criteria
- [ ] Integration test file exists at `tests/api/advisory_summary.rs`
- [ ] All test cases pass against the test PostgreSQL database
- [ ] Tests cover success path, 404 error, deduplication, threshold filtering, and cache headers
- [ ] Tests follow existing integration test conventions (status code assertions, test database usage)

## Test Requirements
- [ ] Test: GET /api/v2/sbom/{id}/advisory-summary returns 200 with correct severity counts for known test data
- [ ] Test: GET /api/v2/sbom/{id}/advisory-summary returns all-zero counts for SBOM with no advisories
- [ ] Test: GET /api/v2/sbom/{nonexistent}/advisory-summary returns 404
- [ ] Test: duplicate advisory links are deduplicated — count reflects unique advisories only
- [ ] Test: `?threshold=high` returns only critical and high counts, medium and low are zero or omitted
- [ ] Test: response includes `cache-control: max-age=300` header

## Verification Commands
- `cargo test --test api advisory_summary` — all integration tests pass

## Dependencies
- Depends on: Task 3 — Add advisory-summary endpoint with caching
- Depends on: Task 4 — Add cache invalidation in advisory ingestion pipeline
