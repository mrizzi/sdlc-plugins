# Task 5 — Add Integration Tests for Advisory Summary Endpoint

## Repository
trustify-backend

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Tests should cover the happy path with correct severity aggregation, 404 for nonexistent SBOMs, advisory deduplication, and edge cases like SBOMs with no advisories. These tests follow the project's integration test pattern of hitting a real PostgreSQL test database.

## Files to Create
- `tests/api/advisory_summary.rs` — integration tests for the advisory summary endpoint

## Files to Modify
- `tests/Cargo.toml` — add any necessary test dependencies (if not already present)

## Implementation Notes
- Follow the existing integration test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs`. These tests use a real PostgreSQL test database and follow the `assert_eq!(resp.status(), StatusCode::OK)` pattern.
- Test setup should:
  1. Create an SBOM via the ingestion pipeline or direct entity insertion
  2. Create advisories with known severity levels (Critical, High, Medium, Low)
  3. Link advisories to the SBOM via the `sbom_advisory` join table
- Test the response body by deserializing into `AdvisorySeveritySummary` and asserting individual field values.
- The test file should be registered as a test module — check how `tests/api/sbom.rs` and `tests/api/advisory.rs` are included (likely via `mod` declarations or Cargo test configuration in `tests/Cargo.toml`).
- Per `docs/constraints.md` §5.11: every test function must have a doc comment.
- Per `docs/constraints.md` §5.12: non-trivial test functions must have given-when-then inline comments.
- Per `docs/constraints.md` §5.9: prefer parameterized tests when multiple cases exercise the same behavior with different inputs.
- Per `docs/constraints.md` §5.10: do not introduce parameterized test patterns if sibling tests do not use them — check `tests/api/sbom.rs` and `tests/api/advisory.rs` first.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM endpoint integration tests; follow setup patterns, database fixtures, and assertion style
- `tests/api/advisory.rs` — existing advisory endpoint integration tests; reference for advisory entity creation in test fixtures
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity; needed for creating test links between SBOMs and advisories

## Acceptance Criteria
- [ ] Test exists for successful advisory summary with correct severity counts
- [ ] Test exists for 404 response when SBOM ID does not exist
- [ ] Test exists for SBOM with no linked advisories (all counts should be 0, total should be 0)
- [ ] Test exists verifying advisory deduplication (same advisory linked twice should count once)
- [ ] Test exists for SBOM with advisories of a single severity level
- [ ] All tests pass against a PostgreSQL test database

## Test Requirements
- [ ] `test_advisory_summary_success` — create SBOM with advisories of mixed severities, verify correct counts
- [ ] `test_advisory_summary_not_found` — request summary for nonexistent SBOM, verify 404 response
- [ ] `test_advisory_summary_no_advisories` — create SBOM with no linked advisories, verify all-zero response
- [ ] `test_advisory_summary_deduplication` — link same advisory twice, verify it is counted once
- [ ] `test_advisory_summary_single_severity` — create SBOM with only High advisories, verify only `high` and `total` are nonzero

## Verification Commands
- `cargo test -p trustify-tests --test advisory_summary` — all tests should pass

## Dependencies
- Depends on: Task 3 — Add Advisory Summary Endpoint with Caching
