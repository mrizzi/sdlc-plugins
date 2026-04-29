## Repository
trustify-backend

## Description
Add comprehensive integration tests for the advisory summary endpoint covering the happy path, error cases, threshold filtering, caching behavior, and cache invalidation. These tests validate the end-to-end behavior of all prior tasks and ensure the feature works correctly against a real PostgreSQL test database.

## Files to Create
- `tests/api/advisory_summary.rs` — Integration test module for `GET /api/v2/sbom/{id}/advisory-summary`

## Files to Modify
- `tests/Cargo.toml` — Add the new test file to the test harness if required by the project's test configuration

## Implementation Notes
- Follow the integration test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs`: set up test data by inserting SBOM and advisory records into the test database, then issue HTTP requests and assert on response status, headers, and body.
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern established in existing tests.
- Test data setup should:
  1. Insert an SBOM record
  2. Insert advisories at various severity levels (e.g., 2 critical, 3 high, 1 medium, 0 low)
  3. Link advisories to the SBOM via the `sbom_advisory` join table
  4. Optionally link the same advisory twice to verify deduplication
- Test cases to include:
  - **Happy path**: Valid SBOM with mixed-severity advisories returns correct counts and total
  - **Empty SBOM**: Valid SBOM with no linked advisories returns all zeros
  - **Not found**: Non-existent SBOM ID returns 404
  - **Deduplication**: Same advisory linked twice to an SBOM counts as 1
  - **Threshold filter**: `?threshold=critical` zeroes non-critical counts; `?threshold=high` returns critical + high only
  - **Invalid threshold**: `?threshold=invalid` returns 400
  - **Cache header**: Response includes `Cache-Control: max-age=300`
- Reference entity structs from `entity/src/sbom.rs`, `entity/src/advisory.rs`, and `entity/src/sbom_advisory.rs` for test data insertion.

## Reuse Candidates
- `tests/api/sbom.rs` — Pattern for SBOM integration tests (test setup, HTTP client usage, assertion style)
- `tests/api/advisory.rs` — Pattern for advisory-related test data setup
- `entity/src/sbom.rs` — SBOM entity for inserting test records
- `entity/src/advisory.rs` — Advisory entity for inserting test records with severity values
- `entity/src/sbom_advisory.rs` — Join entity for linking test advisories to test SBOMs

## Acceptance Criteria
- [ ] All integration tests pass against the PostgreSQL test database
- [ ] Happy path test validates correct severity counts for a known dataset
- [ ] Not-found test validates 404 response
- [ ] Deduplication test validates that duplicate links do not inflate counts
- [ ] Threshold filter tests validate correct zeroing behavior for each threshold level
- [ ] Cache header test validates `Cache-Control: max-age=300` is present

## Test Requirements
- [ ] Test: SBOM with 2 critical, 3 high, 1 medium, 0 low advisories returns `{ critical: 2, high: 3, medium: 1, low: 0, total: 6 }`
- [ ] Test: SBOM with no advisories returns `{ critical: 0, high: 0, medium: 0, low: 0, total: 0 }`
- [ ] Test: non-existent SBOM UUID returns HTTP 404
- [ ] Test: advisory linked to SBOM twice yields count of 1 for that severity
- [ ] Test: `?threshold=critical` with above dataset returns `{ critical: 2, high: 0, medium: 0, low: 0, total: 2 }`
- [ ] Test: `?threshold=high` returns `{ critical: 2, high: 3, medium: 0, low: 0, total: 5 }`
- [ ] Test: `?threshold=invalid` returns HTTP 400
- [ ] Test: response includes `Cache-Control: max-age=300` header

## Verification Commands
- `cargo test -p tests --test advisory_summary` — All advisory summary integration tests pass

## Dependencies
- Depends on: Task 5 — Threshold query parameter support
- Depends on: Task 6 — Cache invalidation on ingestion
