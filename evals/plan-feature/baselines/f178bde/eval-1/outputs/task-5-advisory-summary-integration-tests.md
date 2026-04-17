# Task 5 — Add integration tests for advisory-summary endpoint

## Repository
trustify-backend

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. These tests exercise the full request-response cycle against a real PostgreSQL test database, covering success responses, 404 handling, threshold filtering, and correct severity counting with deduplication.

## Files to Modify
- `tests/api/advisory.rs` — add advisory-summary integration tests to the existing advisory test file (or create a dedicated test file if the existing file is large)

## Files to Create
- `tests/api/advisory_summary.rs` — dedicated integration test file for advisory-summary endpoint (if a separate file is preferred over extending `tests/api/advisory.rs`)

## Implementation Notes
- Follow the existing integration test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs` — tests hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` pattern documented in Key Conventions.
- Test setup should: (1) ingest an SBOM, (2) ingest multiple advisories with varying severities, (3) link advisories to the SBOM via the ingestion pipeline.
- Verify deduplication: link the same advisory to the SBOM twice, confirm it is counted once.
- Verify threshold filtering: call with `?threshold=high`, confirm only `critical` and `high` counts are returned.
- Verify 404: call with a non-existent SBOM UUID, confirm 404 response.
- Per constraints §5.11: add a doc comment to every test function. Per constraints §5.12: add given-when-then inline comments to non-trivial tests.

## Reuse Candidates
- `tests/api/sbom.rs` — SBOM integration test patterns for test setup and assertion style
- `tests/api/advisory.rs` — advisory integration test patterns
- `tests/api/search.rs` — additional reference for integration test structure

## Acceptance Criteria
- [ ] Integration tests exist for: 200 success with correct counts, 404 for missing SBOM, threshold filtering, deduplication
- [ ] Tests run against a real PostgreSQL test database
- [ ] All test functions have doc comments
- [ ] Non-trivial tests include given-when-then inline comments

## Test Requirements
- [ ] Test: valid SBOM with 2 critical, 1 high, 3 medium, 0 low advisories returns correct counts and total of 6
- [ ] Test: non-existent SBOM UUID returns 404
- [ ] Test: `?threshold=high` returns only critical and high counts (medium and low are absent or zero)
- [ ] Test: duplicate advisory links to same SBOM are counted once (deduplication)
- [ ] Test: SBOM with zero advisories returns all zeros

## Verification Commands
- `cargo test --test api -- advisory_summary` — all advisory-summary tests pass
- `cargo test --test api` — full integration test suite still passes (no regressions)

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint
- Depends on: Task 4 — Add cache invalidation for advisory-summary on advisory ingestion
