# Task 4 — Add comprehensive integration tests for advisory summary endpoint

## Repository
trustify-backend

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. These tests exercise the full HTTP request-response cycle against a real PostgreSQL test database, validating correct severity counts, deduplication, 404 handling, threshold filtering, and cache behavior. This ensures the feature works end-to-end and provides a regression safety net.

## Files to Modify
- `tests/Cargo.toml` — add test dependencies if needed

## Files to Create
- `tests/api/advisory_summary.rs` — integration tests for the advisory-summary endpoint

## Implementation Notes
- Follow the integration test pattern established in `tests/api/sbom.rs` (SBOM endpoint tests) and `tests/api/advisory.rs` (advisory endpoint tests). These tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
- Test setup should:
  1. Ingest a test SBOM using the existing test helpers
  2. Ingest test advisories at known severity levels (e.g., 2 Critical, 3 High, 1 Medium, 1 Low)
  3. Correlate the advisories with the SBOM via the ingestion pipeline
- Test cases to implement:
  - **Happy path**: `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with correct counts matching the test data
  - **Empty SBOM**: An SBOM with no linked advisories returns all-zero counts and total=0
  - **404**: Request with non-existent SBOM ID returns 404
  - **Deduplication**: Link the same advisory to an SBOM twice, verify it is counted only once
  - **Threshold filter (critical)**: `?threshold=critical` returns only the critical count
  - **Threshold filter (high)**: `?threshold=high` returns critical and high counts
  - **Threshold filter (invalid)**: `?threshold=invalid` returns 400 Bad Request
- Per constraints doc section 5.9-5.10: Prefer parameterized tests when multiple test cases exercise the same behavior with different inputs. However, check if the existing test files use parameterized patterns before introducing them.
- Per constraints doc section 5.11: Add a doc comment to every test function.
- Per constraints doc section 5.12: Add given-when-then inline comments to non-trivial test functions.

## Reuse Candidates
- `tests/api/sbom.rs` — SBOM endpoint integration tests; follow the same test setup, assertion, and database fixture patterns
- `tests/api/advisory.rs` — advisory endpoint integration tests; reference for advisory ingestion in test setup
- `modules/ingestor/src/service/mod.rs::IngestorService` — used in test setup to ingest SBOMs and advisories

## Acceptance Criteria
- [ ] Integration test file exists at `tests/api/advisory_summary.rs`
- [ ] All test cases pass against a PostgreSQL test database
- [ ] Tests cover: happy path, empty SBOM, 404, deduplication, and threshold filtering
- [ ] Tests follow the existing integration test patterns in `tests/api/`
- [ ] Each test function has a doc comment

## Test Requirements
- [ ] Test: happy path returns correct severity counts (critical, high, medium, low, total)
- [ ] Test: SBOM with no advisories returns all-zero counts
- [ ] Test: non-existent SBOM ID returns 404
- [ ] Test: duplicate advisory links are deduplicated in counts
- [ ] Test: `?threshold=critical` filters to critical only
- [ ] Test: `?threshold=high` filters to critical and high
- [ ] Test: invalid threshold value returns 400

## Verification Commands
- `cargo test --test api -- advisory_summary` — run all advisory summary integration tests
- `cargo test --test api` — run all API integration tests to verify no regressions

## Dependencies
- Depends on: Task 2 — Add advisory summary endpoint with caching and route registration
