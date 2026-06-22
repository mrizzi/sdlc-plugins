# Task 5 — Add integration tests for advisory summary endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Tests should cover the success path with severity count verification, 404 for missing SBOMs, threshold filtering, advisory deduplication, and the response shape contract. Tests follow the established integration testing pattern in `tests/api/`.

## Files to Create
- `tests/api/advisory_summary.rs` — integration tests for the advisory summary endpoint

## Files to Modify
- `tests/Cargo.toml` — add the new test module if test modules are explicitly listed (check existing configuration)

## Implementation Notes
- Follow the integration testing pattern established in `tests/api/sbom.rs` and `tests/api/advisory.rs`. These tests hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` pattern.
- Set up test fixtures by:
  1. Ingesting a test SBOM using the existing ingestion infrastructure
  2. Ingesting test advisories at various severity levels (at least one each of Critical, High, Medium, Low)
  3. Linking advisories to the SBOM via the `sbom_advisory` relationship
- For the deduplication test: link the same advisory to the SBOM via multiple paths and verify it is only counted once.
- For the threshold test: request with `?threshold=high` and verify that only Critical and High counts are returned (Medium and Low are excluded or zero).
- Verify the exact JSON response shape: `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`.
- Performance consideration: while the non-functional requirement specifies p95 < 200ms for SBOMs with up to 500 advisories, integration tests should at minimum verify correctness. Add a test with a moderate number of advisories (10-20) to ensure the aggregation query works at scale beyond trivial counts.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM endpoint integration tests; reference for test setup, fixture ingestion, and assertion patterns
- `tests/api/advisory.rs` — existing advisory endpoint integration tests; reference for advisory fixture creation
- `tests/api/search.rs` — additional reference for test structure and database setup patterns

## Acceptance Criteria
- [ ] All integration tests pass against the test PostgreSQL database
- [ ] Tests verify correct severity count aggregation
- [ ] Tests verify 404 response for non-existent SBOM IDs
- [ ] Tests verify threshold filtering behavior
- [ ] Tests verify advisory deduplication
- [ ] Tests verify the exact JSON response shape

## Test Requirements
- [ ] Test: GET /api/v2/sbom/{id}/advisory-summary with an SBOM having 2 critical, 3 high, 1 medium, 4 low advisories returns `{ "critical": 2, "high": 3, "medium": 1, "low": 4, "total": 10 }`
- [ ] Test: GET /api/v2/sbom/{nonexistent-id}/advisory-summary returns 404
- [ ] Test: GET /api/v2/sbom/{id}/advisory-summary?threshold=high returns counts with critical and high populated, medium and low at 0 or excluded
- [ ] Test: GET /api/v2/sbom/{id}/advisory-summary?threshold=critical returns only critical count
- [ ] Test: SBOM with duplicate advisory links returns each advisory counted exactly once
- [ ] Test: SBOM with zero advisories returns `{ "critical": 0, "high": 0, "medium": 0, "low": 0, "total": 0 }`
- [ ] Test: GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid returns 400

## Verification Commands
- `cargo test --test api -- advisory_summary` — all advisory summary tests pass

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint
