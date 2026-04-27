# Task 5 — Add integration tests for advisory-summary endpoint

## Repository
trustify-backend

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint covering all acceptance criteria: correct severity counts with deduplication, 404 for missing SBOMs, threshold filtering, and cache behavior. These tests validate the end-to-end flow from HTTP request through service logic to database query and response serialization.

## Files to Create
- `tests/api/advisory_summary.rs` — Integration tests for the advisory-summary endpoint

## Files to Modify
- `tests/Cargo.toml` — Add any necessary test dependencies if not already present (unlikely, but verify)

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/sbom.rs` and `tests/api/advisory.rs`. These tests hit a real PostgreSQL test database, use `assert_eq!(resp.status(), StatusCode::OK)` pattern, and set up test data through the ingestion pipeline or direct database insertion.
- Test setup: For each test, create an SBOM and link advisories at various severity levels (critical, high, medium, low) using the existing test fixtures or ingestion service. Ensure at least one test includes duplicate advisory links to verify deduplication.
- Test cases to implement:
  1. **Happy path**: SBOM with advisories at all severity levels returns correct counts
  2. **Empty SBOM**: SBOM with no linked advisories returns all zeros `{ critical: 0, high: 0, medium: 0, low: 0, total: 0 }`
  3. **Non-existent SBOM**: Request with unknown SBOM ID returns 404
  4. **Deduplication**: Same advisory linked multiple times to the same SBOM is counted once
  5. **Threshold filtering**: `?threshold=high` returns counts only for critical and high, with medium and low as zero
  6. **Threshold filtering edge case**: `?threshold=low` returns all counts (no filtering)
- Per `docs/constraints.md` §5.11: Add a doc comment to every test function describing what it verifies.
- Per `docs/constraints.md` §5.12: Add given-when-then inline comments to non-trivial test functions with distinct setup, action, and assertion phases.
- Per `docs/constraints.md` §5.9: Consider using parameterized tests for threshold filtering test cases if the project uses parameterized test patterns (check `tests/api/sbom.rs` for existing patterns).

## Reuse Candidates
- `tests/api/sbom.rs` — Existing SBOM endpoint integration tests showing test setup, database fixtures, HTTP request patterns, and assertion conventions
- `tests/api/advisory.rs` — Existing advisory endpoint integration tests showing how advisories are created in test fixtures
- `modules/ingestor/src/service/mod.rs::IngestorService` — May be used in test setup to ingest test SBOMs and advisories

## Acceptance Criteria
- [ ] All integration tests pass against a PostgreSQL test database
- [ ] Tests cover: happy path, empty SBOM, non-existent SBOM (404), deduplication, threshold filtering
- [ ] Tests follow the project's existing test patterns and conventions
- [ ] Every test function has a doc comment

## Test Requirements
- [ ] Integration test for happy path — correct severity counts returned
- [ ] Integration test for empty SBOM — all zero counts returned
- [ ] Integration test for non-existent SBOM — 404 status returned
- [ ] Integration test for deduplication — duplicate advisory links produce correct count
- [ ] Integration test for threshold filtering — counts below threshold are zero
- [ ] Integration test for threshold=low edge case — all counts returned

## Verification Commands
- `cargo test -p trustify-tests --test api -- advisory_summary` — all tests pass

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint
