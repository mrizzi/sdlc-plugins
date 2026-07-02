## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint covering all acceptance criteria: happy path with correct severity counts, 404 for non-existent SBOM, advisory deduplication, threshold query parameter filtering, and cache behavior. These tests ensure the endpoint works correctly end-to-end against a real PostgreSQL test database, following the established integration testing patterns in the project.

## Files to Create
- `tests/api/advisory_summary.rs` — integration test module with test functions covering all scenarios for the advisory-summary endpoint

## Implementation Notes
- Follow the existing integration test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs`. These tests hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` pattern for status code assertions.
- Test setup should:
  1. Create an SBOM via the ingestion pipeline or direct database insertion
  2. Create advisories at various severity levels (Critical, High, Medium, Low)
  3. Link advisories to the SBOM via the sbom_advisory join table
- Test scenarios to implement:
  - **Happy path**: SBOM with advisories at all severity levels; verify counts match expected values
  - **Empty SBOM**: SBOM with no linked advisories; verify all counts are zero and total is zero
  - **404**: Request with a non-existent SBOM UUID; verify 404 status code
  - **Deduplication**: Link the same advisory to an SBOM through multiple paths; verify it is counted only once
  - **Threshold filtering**: Use `?threshold=high` and verify only high and critical counts are non-zero
  - **Invalid threshold**: Use `?threshold=invalid` and verify 400 status code
  - **Cache headers**: Verify response includes `Cache-Control: max-age=300` header
- Per CONVENTIONS.md §Testing: use real PostgreSQL test database for integration tests and follow the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern. Applies: task creates `tests/api/advisory_summary.rs` matching the convention's tests/api/ directory scope.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM endpoint integration tests; follow the same test setup, fixture creation, and assertion patterns
- `tests/api/advisory.rs` — existing advisory endpoint integration tests; reference for advisory fixture creation
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion logic for creating test fixtures
- `modules/ingestor/src/graph/advisory/mod.rs` — advisory ingestion logic for creating test fixtures

## Acceptance Criteria
- [ ] Integration tests pass against a real PostgreSQL test database
- [ ] All endpoint behaviors are covered: happy path, 404, deduplication, threshold filtering, cache headers
- [ ] Tests follow the established patterns in the existing test suite
- [ ] Test fixtures create realistic data (multiple severity levels, deduplicated advisories)

## Test Requirements
- [ ] Test: GET /api/v2/sbom/{id}/advisory-summary returns 200 with correct severity counts for an SBOM with advisories at all severity levels
- [ ] Test: GET /api/v2/sbom/{id}/advisory-summary returns 200 with all-zero counts for an SBOM with no advisories
- [ ] Test: GET /api/v2/sbom/{nonexistent}/advisory-summary returns 404
- [ ] Test: advisories linked multiple times are counted only once (deduplication)
- [ ] Test: ?threshold=high returns only high and critical counts, with medium and low zeroed
- [ ] Test: ?threshold=invalid returns 400
- [ ] Test: response includes Cache-Control header with max-age=300

## Verification Commands
- `cargo test --test api advisory_summary` — all advisory-summary integration tests pass
- `cargo test --test api` — full integration test suite passes (no regressions)

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and aggregation service
- Depends on: Task 2 — Add advisory-summary endpoint

---
[sdlc-workflow] Description digest: sha256-md:9c429bd7927fa60be2213eae0fa81fc48cff042a01987c2d1b8d01a869c58ebb
