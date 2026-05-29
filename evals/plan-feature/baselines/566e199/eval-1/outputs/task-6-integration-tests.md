# Task 6 — Add comprehensive integration tests for advisory-summary endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add a dedicated integration test module for the advisory-summary endpoint covering all acceptance scenarios: correct severity counts, deduplication, 404 for missing SBOMs, cache headers, and performance characteristics. This ensures the endpoint meets the p95 < 200ms requirement for SBOMs with up to 500 advisories and validates the complete data flow from ingestion through API response.

## Files to Modify
- `tests/Cargo.toml` — add any necessary test dependencies if not already present

## Files to Create
- `tests/api/advisory_summary.rs` — integration test module for `GET /api/v2/sbom/{id}/advisory-summary`

## Implementation Notes
- Follow the existing integration test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs` for test setup, database fixtures, HTTP client configuration, and assertion patterns.
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern established in the project.
- Test data setup: create test SBOMs and advisories with known severities using the existing ingestion service or direct database inserts consistent with how `tests/api/sbom.rs` sets up fixtures.
- For the deduplication test, link the same advisory to an SBOM multiple times and verify it is counted only once.
- For the performance test, create an SBOM with 500 advisories and verify the response time is under 200ms (use a timing assertion or at minimum verify the endpoint handles the volume without timeout).
- Register the new test module in the test harness if required by the project's test organization.

## Reuse Candidates
- `tests/api/sbom.rs` — SBOM endpoint integration test patterns (setup, assertions, fixtures)
- `tests/api/advisory.rs` — advisory endpoint integration test patterns
- `tests/Cargo.toml` — test dependency configuration

## Acceptance Criteria
- [ ] Integration test file `tests/api/advisory_summary.rs` exists with tests covering all key scenarios
- [ ] All tests pass against a PostgreSQL test database
- [ ] Test coverage includes: success case, 404 case, deduplication case, and large-volume case (500 advisories)

## Test Requirements
- [ ] Test: SBOM with advisories at all four severity levels returns correct counts
- [ ] Test: SBOM with no advisories returns all zeros
- [ ] Test: non-existent SBOM ID returns 404
- [ ] Test: duplicate advisory links are deduplicated (advisory counted once)
- [ ] Test: SBOM with 500 advisories responds successfully (validates performance requirement)
- [ ] Test: response JSON shape matches `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`

## Verification Commands
- `cargo test --test api advisory_summary` — all advisory-summary integration tests pass

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint
