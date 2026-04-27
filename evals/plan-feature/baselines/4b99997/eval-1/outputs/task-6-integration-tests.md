## Repository
trustify-backend

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint in the existing test suite. These tests hit a real PostgreSQL test database and verify the full request-response cycle including correct severity aggregation, advisory deduplication, 404 handling for missing SBOMs, threshold filtering, and caching behavior. This task consolidates end-to-end test coverage for the entire advisory summary feature.

## Files to Modify
- `tests/api/sbom.rs` — add integration test functions for the advisory-summary endpoint covering all acceptance scenarios

## Implementation Notes
- Follow the existing integration test patterns in `tests/api/sbom.rs` (SBOM endpoint tests) and `tests/api/advisory.rs` (advisory endpoint tests). Key patterns to replicate:
  - Use the test database setup and teardown pattern established in existing tests
  - Make HTTP requests via the test server client using the same request builder pattern
  - Assert response status with `assert_eq!(resp.status(), StatusCode::OK)` or `StatusCode::NOT_FOUND`
  - Deserialize response bodies to the expected struct and assert field values
- Test data setup: create test SBOMs and advisories with known severities using the existing test fixture patterns in `tests/api/sbom.rs`. Link advisories to SBOMs via the `sbom_advisory` join table (`entity/src/sbom_advisory.rs`).
- For deduplication testing: insert the same advisory linked to an SBOM via multiple paths and verify it is counted only once.
- For threshold testing: use the `?threshold=high` query parameter and verify that medium and low counts are returned as 0.
- For 404 testing: use a non-existent UUID as the SBOM ID.
- Per `docs/constraints.md` section 5 (Code Change Rules): inspect existing tests in `tests/api/sbom.rs` and `tests/api/advisory.rs` before writing to match their patterns for test setup, assertions, and naming conventions.
- Per `docs/constraints.md` section 5.11: add a doc comment to every test function.
- Per `docs/constraints.md` section 5.12: add given-when-then inline comments to non-trivial test functions with distinct setup, action, and assertion phases.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM endpoint integration tests; use as the primary reference for test structure, database setup, and assertion patterns
- `tests/api/advisory.rs` — existing advisory endpoint integration tests; reference for advisory-specific test data setup
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity; needed for test data linking
- `entity/src/advisory.rs` — Advisory entity; needed for creating test advisories with specific severity values
- `entity/src/sbom.rs` — SBOM entity; needed for creating test SBOMs

## Acceptance Criteria
- [ ] Test for successful aggregation: SBOM with advisories at all four severity levels returns correct counts
- [ ] Test for deduplication: SBOM with duplicate advisory links counts each advisory only once
- [ ] Test for empty results: SBOM with no linked advisories returns all counts as 0 and total as 0
- [ ] Test for 404: nonexistent SBOM ID returns 404 status
- [ ] Test for threshold filtering: `?threshold=high` returns only critical and high counts, medium and low as 0
- [ ] Test for invalid threshold: `?threshold=invalid` returns 400 status
- [ ] Test for caching: second request within 5 minutes returns cached response
- [ ] All tests pass against the PostgreSQL test database

## Test Requirements
- [ ] `test_advisory_summary_all_severities` — create SBOM with 2 critical, 3 high, 1 medium, 4 low advisories; verify response counts match
- [ ] `test_advisory_summary_deduplication` — link the same advisory to an SBOM twice; verify it is counted once
- [ ] `test_advisory_summary_empty` — SBOM with no advisories returns `{ critical: 0, high: 0, medium: 0, low: 0, total: 0 }`
- [ ] `test_advisory_summary_not_found` — request with nonexistent UUID returns 404
- [ ] `test_advisory_summary_threshold_high` — `?threshold=high` returns critical and high counts only
- [ ] `test_advisory_summary_threshold_invalid` — `?threshold=invalid` returns 400
- [ ] `test_advisory_summary_cache` — second identical request returns cached response

## Verification Commands
- `cargo test -p trustify-tests -- advisory_summary` — all advisory summary integration tests pass
- `cargo test -p trustify-tests` — full test suite passes (no regressions)

## Dependencies
- Depends on: Task 3 — Add advisory summary endpoint
- Depends on: Task 4 — Add cache invalidation to advisory ingestion pipeline
- Depends on: Task 5 — Add threshold query parameter support
