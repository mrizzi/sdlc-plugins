## Repository
trustify-backend

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. These tests verify the full request-response cycle against a real PostgreSQL test database, covering the happy path with correct severity counts, 404 for non-existent SBOMs, advisory deduplication, and empty advisory sets. The tests follow the existing integration test patterns in `tests/api/`.

## Files to Create
- `tests/api/sbom_advisory_summary.rs` — Integration tests for the advisory-summary endpoint

## Files to Modify
- `tests/Cargo.toml` — Add the new test file to the test suite if required by the project's test configuration

## Implementation Notes
- Follow the test patterns in `tests/api/sbom.rs` (SBOM endpoint tests) and `tests/api/advisory.rs` (advisory endpoint tests) for test setup, database fixture loading, HTTP client usage, and assertion style.
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern consistent with existing tests.
- Each test should set up its own fixture data: create an SBOM, create advisories at known severity levels, link them via the `sbom_advisory` join table, then call the endpoint and verify the response.
- Test deduplication: create a scenario where the same advisory is linked to the same SBOM multiple times and verify it is counted only once.
- Test zero advisories: create an SBOM with no linked advisories and verify the response returns all-zero counts.
- Test 404: call the endpoint with a non-existent SBOM ID and verify the response status is 404.
- Per constraints (section 5.11), add a doc comment to every test function explaining what it verifies.
- Per constraints (section 5.12), add given-when-then inline comments to non-trivial test functions with distinct setup, action, and assertion phases.

## Reuse Candidates
- `tests/api/sbom.rs` — Existing SBOM endpoint tests; pattern reference for test setup, fixture creation, and assertion style
- `tests/api/advisory.rs` — Advisory endpoint tests; pattern for advisory fixture creation
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity for setting up test fixture data

## Acceptance Criteria
- [ ] Integration test file exists at `tests/api/sbom_advisory_summary.rs`
- [ ] Test: valid SBOM with known advisories returns 200 with correct severity counts
- [ ] Test: non-existent SBOM ID returns 404
- [ ] Test: SBOM with no advisories returns 200 with all-zero counts and total=0
- [ ] Test: duplicate advisory links are deduplicated (same advisory counted once)
- [ ] All tests pass against the PostgreSQL test database
- [ ] Every test function has a doc comment

## Test Requirements
- [ ] `test_advisory_summary_happy_path` — Create SBOM with advisories at each severity level, verify counts match
- [ ] `test_advisory_summary_not_found` — Request summary for non-existent SBOM, verify 404
- [ ] `test_advisory_summary_empty` — Create SBOM with no advisories, verify all-zero counts
- [ ] `test_advisory_summary_deduplication` — Link same advisory twice, verify count is 1

## Verification Commands
- `cargo test --test api sbom_advisory_summary` — all integration tests pass
- `cargo test --test api` — full integration test suite still passes (no regressions)

## Dependencies
- Depends on: Task 3 — Endpoint (the endpoint must be implemented before integration tests can run)
