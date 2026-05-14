# Task 4 — Add integration tests for advisory-summary endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. These tests verify the full request-response cycle against a real PostgreSQL test database, covering success cases, error cases, deduplication logic, and threshold filtering. This follows the established integration test pattern in `tests/api/`.

## Files to Modify
- `tests/api/sbom.rs` — Add integration test functions for the advisory-summary endpoint, following the existing test structure and patterns in this file (SBOM endpoint integration tests)

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/sbom.rs` and `tests/api/advisory.rs`. These tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` for status verification.
- Test setup should:
  1. Create a test SBOM via the ingestion pipeline or direct database seeding
  2. Create test advisories with known severity levels (e.g., 2 critical, 3 high, 1 medium, 1 low)
  3. Link advisories to the SBOM via `sbom_advisory` records
  4. Include a duplicate advisory link to verify deduplication
- Test cases to implement:
  - **Happy path**: SBOM with multiple advisories at various severities returns correct counts
  - **Empty SBOM**: SBOM with no linked advisories returns all zeros `{ critical: 0, high: 0, medium: 0, low: 0, total: 0 }`
  - **404**: Non-existent SBOM ID returns HTTP 404
  - **Deduplication**: Same advisory linked twice to an SBOM is counted only once
  - **Threshold filter (critical)**: `?threshold=critical` returns only critical count, others zeroed
  - **Threshold filter (high)**: `?threshold=high` returns critical and high counts, others zeroed
  - **Invalid threshold**: `?threshold=invalid` returns HTTP 400 or is ignored (match endpoint behavior)
- Per `docs/constraints.md` section 5.11: add a doc comment to every test function. Per section 5.12: add given-when-then inline comments to non-trivial test functions.

## Reuse Candidates
- `tests/api/sbom.rs` — Existing SBOM integration tests; follow the same test setup, HTTP client usage, and assertion patterns
- `tests/api/advisory.rs` — Advisory integration tests; reference for advisory creation and linking setup patterns
- `common/src/model/paginated.rs::PaginatedResults` — Though not used by this endpoint, reference for response parsing patterns in tests

## Acceptance Criteria
- [ ] Integration tests cover: happy path, empty SBOM, 404, deduplication, threshold filtering
- [ ] All tests pass against the PostgreSQL test database
- [ ] Tests follow existing patterns in `tests/api/sbom.rs` (setup, assertion style, status code checks)
- [ ] Each test function has a doc comment explaining what it verifies
- [ ] Non-trivial tests include given-when-then inline comments

## Test Requirements
- [ ] Test: SBOM with multiple advisories returns correct severity counts
- [ ] Test: SBOM with no advisories returns all zero counts
- [ ] Test: Non-existent SBOM ID returns 404
- [ ] Test: Duplicate advisory links are deduplicated (same advisory counted once)
- [ ] Test: `?threshold=critical` filters to only critical severity
- [ ] Test: `?threshold=high` filters to critical and high severities

## Verification Commands
- `cargo test --test api` — all integration tests pass
- `cargo test advisory_summary` — advisory-summary specific tests pass

## Dependencies
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
