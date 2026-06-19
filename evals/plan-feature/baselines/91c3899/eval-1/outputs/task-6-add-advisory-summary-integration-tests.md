## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the advisory-summary endpoint covering the core scenarios: successful aggregation, 404 for missing SBOMs, deduplication correctness, threshold filtering, and caching behavior. These tests ensure the endpoint meets the functional and non-functional requirements specified in TC-9001.

## Files to Create
- `tests/api/advisory_summary.rs` — Integration tests for GET /api/v2/sbom/{id}/advisory-summary

## Files to Modify
- `tests/Cargo.toml` — Add any necessary test dependencies if not already present

## Implementation Notes
- Follow the existing integration test patterns established in `tests/api/sbom.rs` (SBOM endpoint integration tests) and `tests/api/advisory.rs` (Advisory endpoint integration tests). These tests hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern.
- Set up test data by ingesting SBOMs and advisories via the existing test helpers or service methods, then linking them via the `sbom_advisory` join table (`entity/src/sbom_advisory.rs`).
- Per Testing convention: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task creates `tests/api/advisory_summary.rs` matching the convention's test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — Follow the test setup, HTTP client configuration, and assertion patterns used in existing SBOM tests
- `tests/api/advisory.rs` — Follow the test data setup patterns for creating advisories with different severity levels
- `modules/ingestor/src/graph/sbom/mod.rs` — Reuse SBOM ingestion utilities for test data setup
- `modules/ingestor/src/graph/advisory/mod.rs` — Reuse advisory ingestion utilities for test data setup

## Acceptance Criteria
- [ ] Test for successful aggregation: SBOM with advisories of mixed severities returns correct counts
- [ ] Test for empty result: SBOM with no linked advisories returns all-zero counts
- [ ] Test for 404: non-existent SBOM ID returns 404 status
- [ ] Test for deduplication: SBOM with duplicate advisory links returns correct deduplicated counts
- [ ] Test for threshold filtering: `?threshold=high` returns only critical and high counts, with medium and low zeroed out
- [ ] Test for total field correctness: total equals sum of all severity counts
- [ ] All tests pass against the PostgreSQL test database

## Test Requirements
- [ ] At least 6 integration test cases covering the scenarios listed in Acceptance Criteria
- [ ] Tests use real database interactions, not mocks
- [ ] Test data setup creates SBOMs and advisories with known severity distributions for deterministic assertions

## Verification Commands
- `cargo test -p trustify-tests -- advisory_summary` — expected: all advisory-summary tests pass

## Dependencies
- Depends on: Task 3 — Add advisory summary endpoint
- Depends on: Task 5 — Add cache invalidation on advisory ingestion
