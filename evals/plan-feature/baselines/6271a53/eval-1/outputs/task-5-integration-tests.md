# Task 5 — Add integration tests for advisory-summary endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint covering all acceptance criteria: successful severity aggregation, 404 for missing SBOMs, advisory deduplication, threshold filtering, and performance validation. These tests exercise the full request/response cycle against a real PostgreSQL test database, following the established integration test patterns.

## Files to Create
- `tests/api/advisory_summary.rs` — integration tests for the advisory-summary endpoint

## Files to Modify
- `tests/Cargo.toml` — add any new test dependencies if needed (likely none, as existing test infrastructure should suffice)

## Implementation Notes
- Follow the integration test patterns established in `tests/api/sbom.rs` and `tests/api/advisory.rs` for test setup, database fixtures, HTTP client usage, and assertion patterns.
- Tests should use `assert_eq!(resp.status(), StatusCode::OK)` pattern as documented in the repository conventions.
- Test fixture setup:
  1. Create an SBOM via the ingestion pipeline or direct database insertion
  2. Create advisories at various severity levels (critical, high, medium, low)
  3. Link advisories to the SBOM via the `sbom_advisory` join table
  4. For deduplication tests: link the same advisory to the SBOM multiple times (if the schema allows) or verify that the count query handles distinct advisories correctly
- Test cases to implement:
  - **Happy path**: SBOM with advisories at all four severity levels returns correct counts and total
  - **Empty advisories**: SBOM with no linked advisories returns all zeros
  - **404 case**: Non-existent SBOM ID returns 404 status
  - **Deduplication**: Same advisory linked via different paths still counts once
  - **Threshold filtering**: `?threshold=critical` returns only critical count; `?threshold=high` returns critical + high
  - **Performance validation**: SBOM with ~500 advisories returns within reasonable time (optional, may use `#[ignore]` attribute)
- Per constraints doc section 5.9: prefer parameterized tests when multiple test cases exercise the same behavior with different inputs (e.g., threshold filtering with different severity values).
- Per constraints doc section 5.11: add a doc comment to every test function.
- Per constraints doc section 5.12: add given-when-then inline comments to non-trivial test functions.

## Reuse Candidates
- `tests/api/sbom.rs` — SBOM endpoint integration tests for test setup patterns, HTTP client usage, and assertion style
- `tests/api/advisory.rs` — advisory endpoint integration tests for advisory fixture creation patterns
- `tests/api/search.rs` — additional reference for integration test structure

## Acceptance Criteria
- [ ] Integration test file `tests/api/advisory_summary.rs` exists and compiles
- [ ] All test cases pass against the test database
- [ ] Tests cover: happy path, empty advisories, 404, deduplication, threshold filtering
- [ ] Tests follow existing integration test patterns (setup, assertions, error handling)

## Test Requirements
- [ ] Test: SBOM with advisories at all severity levels returns correct counts
- [ ] Test: SBOM with no advisories returns `{ critical: 0, high: 0, medium: 0, low: 0, total: 0 }`
- [ ] Test: Non-existent SBOM ID returns HTTP 404
- [ ] Test: Deduplicated advisory count (same advisory not double-counted)
- [ ] Test: `?threshold=critical` filters to critical-only counts
- [ ] Test: `?threshold=high` filters to critical + high counts
- [ ] Test: `?threshold=medium` filters to critical + high + medium counts

## Verification Commands
- `cargo test --test api advisory_summary` — run all advisory-summary integration tests
- `cargo test --test api` — run full integration test suite to verify no regressions

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint
