## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Tests cover the full request-response cycle against a real PostgreSQL test database, validating correct severity aggregation, deduplication, 404 handling, threshold filtering, and cache headers.

## Files to Modify
- `tests/api/sbom.rs` — Add integration tests for the advisory-summary endpoint

## Implementation Notes
Follow the existing integration test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs`. These tests hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` pattern from Key Conventions.

Test setup should:
1. Ingest a test SBOM (using patterns from existing SBOM tests in `tests/api/sbom.rs`)
2. Ingest multiple test advisories with varying severities (following patterns from `tests/api/advisory.rs`)
3. Link advisories to the SBOM via the `sbom_advisory` join table (`entity/src/sbom_advisory.rs`)

Test cases:
- **Happy path**: SBOM with 2 critical, 3 high, 1 medium, 0 low advisories returns `{ critical: 2, high: 3, medium: 1, low: 0, total: 6 }`
- **Deduplication**: Same advisory linked twice returns count of 1, not 2
- **Empty SBOM**: SBOM with no linked advisories returns `{ critical: 0, high: 0, medium: 0, low: 0, total: 0 }`
- **Non-existent SBOM**: Returns 404 status
- **Threshold filter**: `?threshold=high` returns only critical and high counts, zeros for medium and low
- **Cache headers**: Response includes `Cache-Control` header with `max-age=300`

Per Key Conventions (Testing): Integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task modifies `tests/api/sbom.rs` matching the convention's test files scope.

## Acceptance Criteria
- [ ] At least 5 integration test cases covering happy path, deduplication, empty SBOM, 404, and threshold filtering
- [ ] All tests use the real PostgreSQL test database pattern from existing tests
- [ ] Tests validate response body JSON shape matches `AdvisorySeveritySummary`
- [ ] Tests validate HTTP status codes (200 for success, 404 for missing SBOM)
- [ ] Tests validate cache-control headers

## Test Requirements
- [ ] `test_advisory_summary_happy_path` — correct severity counts for known test data
- [ ] `test_advisory_summary_deduplication` — duplicate advisory links are counted once
- [ ] `test_advisory_summary_empty_sbom` — SBOM with no advisories returns all zeros
- [ ] `test_advisory_summary_not_found` — non-existent SBOM ID returns 404
- [ ] `test_advisory_summary_threshold_filter` — threshold parameter correctly filters counts
- [ ] `test_advisory_summary_cache_headers` — response includes correct cache-control header

## Verification Commands
- `cargo test --test api sbom::test_advisory_summary` — all advisory-summary integration tests pass

## Dependencies
- Depends on: Task 3 — advisory summary endpoint (endpoint must exist to test it)
- Depends on: Task 4 — cache invalidation (to test cache behavior end-to-end)

[sdlc-workflow] Description digest: sha256-md:24fe66d2c77e2da6f6ed54fa22336999d3813178f1b5cf9dbcd4e536cc57e9c5
