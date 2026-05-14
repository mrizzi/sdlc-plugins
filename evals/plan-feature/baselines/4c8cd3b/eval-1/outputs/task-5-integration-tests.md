## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary`
endpoint. These tests exercise the full request-response cycle against a real PostgreSQL
test database, verifying correct severity aggregation, 404 handling, cache headers,
threshold filtering, and deduplication behavior.

## Files to Create
- `tests/api/advisory_summary.rs` — integration test module for the advisory-summary endpoint

## Files to Modify
- `tests/Cargo.toml` — add any necessary test dependencies if not already present (e.g., test fixtures, HTTP client utilities)

## Implementation Notes
- Follow the existing integration test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs`. These tests demonstrate:
  - How to set up the test HTTP client and database
  - How to create test fixtures (SBOMs, advisories) in the test database
  - The `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern
  - How to deserialize JSON response bodies for field-level assertions
- **Test fixture setup:** Each test should:
  1. Create an SBOM in the test database
  2. Create advisories with known severity levels (e.g., 2 critical, 3 high, 1 medium, 0 low)
  3. Link advisories to the SBOM via `sbom_advisory` records
  4. Call the endpoint and assert the response matches expected counts
- **Deduplication test:** Create a scenario where the same advisory is linked to the same SBOM multiple times (duplicate `sbom_advisory` records) and verify the count reflects unique advisories only.
- **404 test:** Call the endpoint with a UUID that does not correspond to any SBOM and assert a 404 status.
- **Cache header test:** Verify the response contains `Cache-Control: max-age=300`.
- **Threshold filter tests:**
  - `?threshold=critical` — only `critical` count is non-zero, others are zero, `total` equals `critical`
  - `?threshold=high` — `critical` and `high` are non-zero, `medium` and `low` are zero
  - `?threshold=medium` — `critical`, `high`, and `medium` are non-zero, `low` is zero
  - No threshold — all severity counts are returned as-is
- **Empty SBOM test:** Call the endpoint for an SBOM with no linked advisories and verify all counts are zero.
- Per `docs/constraints.md` section 5.11: every test function must have a doc comment explaining what it tests.
- Per `docs/constraints.md` section 5.12: non-trivial tests must include given-when-then inline comments.

## Reuse Candidates
- `tests/api/sbom.rs` — integration test patterns for SBOM endpoint testing, including fixture setup and response assertion patterns
- `tests/api/advisory.rs` — integration test patterns for advisory-related testing, including how to create advisory test fixtures with severity levels
- `common/src/model/paginated.rs::PaginatedResults` — reference for response deserialization patterns used in existing tests

## Dependencies
- Depends on: Task 3 — Add advisory-summary endpoint
- Depends on: Task 4 — Add cache invalidation in advisory ingestion pipeline

## Acceptance Criteria
- [ ] Integration test file exists at `tests/api/advisory_summary.rs`
- [ ] Tests cover: successful severity count response, 404 for missing SBOM, cache headers, threshold filtering (all levels), deduplication, empty SBOM
- [ ] All tests pass against the PostgreSQL test database (`cargo test`)
- [ ] Each test function has a doc comment
- [ ] Non-trivial tests include given-when-then inline comments

## Test Requirements
- [ ] Test: valid SBOM with mixed severity advisories returns correct counts for each severity level and correct total
- [ ] Test: non-existent SBOM ID returns 404 status
- [ ] Test: response includes `Cache-Control: max-age=300` header
- [ ] Test: `?threshold=critical` filters correctly (only critical non-zero)
- [ ] Test: `?threshold=high` filters correctly (critical and high non-zero)
- [ ] Test: duplicate advisory links do not inflate counts (deduplication)
- [ ] Test: SBOM with no linked advisories returns all-zero counts
- [ ] Test: `?threshold=medium` returns critical, high, and medium counts with low zeroed

## Verification Commands
- `cargo test --test api advisory_summary` — all advisory-summary integration tests pass
