## Repository
trustify-backend

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Tests must cover the success path with correct severity counts, 404 for missing SBOMs, deduplication of advisories, zero-count scenarios, and performance characteristics for SBOMs with many advisories.

## Files to Create
- `tests/api/sbom_advisory_summary.rs` — Integration tests for the advisory-summary endpoint

## Files to Modify
- `tests/Cargo.toml` — Add any necessary test dependencies if not already present

## Implementation Notes
- Follow the existing integration test patterns in `tests/api/sbom.rs` (SBOM endpoint tests) and `tests/api/advisory.rs` (advisory endpoint tests). These tests hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` pattern.
- Set up test data by creating an SBOM and linking advisories at various severity levels using the existing entity models in `entity/src/sbom.rs`, `entity/src/advisory.rs`, and `entity/src/sbom_advisory.rs`.
- For the deduplication test, insert multiple `sbom_advisory` rows linking the same advisory ID to the same SBOM, then verify the advisory is counted only once.
- For the zero-count test, create an SBOM with no linked advisories and verify all counts are 0.
- For the 404 test, request an advisory-summary for a non-existent SBOM ID and verify the response status is 404.
- Verify the JSON response shape matches `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` exactly.
- Per the repository's key conventions: integration tests are in `tests/api/` and hit a real PostgreSQL test database.

## Reuse Candidates
- `tests/api/sbom.rs` — Existing SBOM integration tests; follow the test setup, HTTP client configuration, and assertion patterns.
- `tests/api/advisory.rs` — Existing advisory integration tests; follow the pattern for creating advisory test data with severity levels.
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity; use for setting up test data linking SBOMs to advisories.

## Acceptance Criteria
- [ ] Integration tests pass against a real PostgreSQL test database
- [ ] Test coverage includes: success with mixed severities, all-zero counts, 404 for missing SBOM, deduplication
- [ ] Response JSON shape is validated in each success test
- [ ] Tests follow the established patterns in `tests/api/`

## Test Requirements
- [ ] Test: GET advisory-summary for SBOM with advisories at all four severity levels returns correct counts and total
- [ ] Test: GET advisory-summary for SBOM with no linked advisories returns all-zero counts with total = 0
- [ ] Test: GET advisory-summary for non-existent SBOM ID returns 404
- [ ] Test: GET advisory-summary deduplicates advisories — same advisory linked multiple times is counted once
- [ ] Test: Response JSON has exactly the fields: critical, high, medium, low, total

## Verification Commands
- `cargo test --test api -- sbom_advisory_summary` — all tests pass

## Dependencies
- Depends on: Task 3 — Add advisory-summary endpoint
