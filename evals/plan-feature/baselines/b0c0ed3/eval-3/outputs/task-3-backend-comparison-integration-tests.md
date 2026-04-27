## Repository
trustify-backend

## Description
Add comprehensive integration tests for the SBOM comparison endpoint, covering the full request/response cycle against a real PostgreSQL test database. These tests validate the end-to-end behavior of the comparison feature including edge cases like large SBOMs and identical SBOMs.

## Files to Create
- `tests/api/sbom_compare.rs` — Integration test module for the comparison endpoint

## Files to Modify
- `tests/api/sbom.rs` — Add `mod sbom_compare;` if the test runner uses a module tree, or ensure the new test file is picked up by the test harness (verify existing test discovery pattern)

## Implementation Notes
Follow the integration test pattern established in `tests/api/sbom.rs` and `tests/api/advisory.rs`. These files:
1. Set up a test database with seed data
2. Make HTTP requests to the API endpoints
3. Assert on response status codes and JSON body structure using `assert_eq!(resp.status(), StatusCode::OK)` pattern

For comparison tests, the setup phase must:
- Ingest two SBOMs with overlapping but different package sets
- Ensure some packages have version differences, license differences, and advisory associations
- Use the ingestion infrastructure from `modules/ingestor/src/service/mod.rs` for seeding test data

Test cases should cover:
- **Happy path**: Two SBOMs with known differences produce the expected diff across all six categories
- **Identical SBOMs**: Same SBOM ID for both left and right returns all empty arrays
- **Large diff**: SBOMs with >100 package differences return correct results (validates performance characteristics)
- **Disjoint SBOMs**: Two SBOMs with no overlapping packages — all packages appear in added/removed
- **Error cases**: Already covered by Task 2 endpoint tests, but verify 400/404 responses from integration level as well

## Reuse Candidates
- `tests/api/sbom.rs` — Existing SBOM integration tests demonstrating test setup, HTTP request patterns, and assertion style
- `tests/api/advisory.rs` — Advisory integration tests showing how to seed advisory data and verify advisory-related responses
- `modules/ingestor/src/service/mod.rs::IngestorService` — Used to ingest test SBOM data during test setup

## Acceptance Criteria
- [ ] Integration tests exist in `tests/api/sbom_compare.rs`
- [ ] Tests seed at least two SBOMs with known package, advisory, and license differences
- [ ] Happy path test verifies all six diff categories contain expected entries
- [ ] Identical-SBOM test verifies all categories are empty arrays
- [ ] All tests pass against the PostgreSQL test database
- [ ] Tests follow the established assertion pattern (`assert_eq!(resp.status(), StatusCode::OK)`)

## Test Requirements
- [ ] Integration test: compare two SBOMs with added packages — verify `added_packages` contains correct entries
- [ ] Integration test: compare two SBOMs with removed packages — verify `removed_packages` contains correct entries
- [ ] Integration test: compare two SBOMs with version changes — verify `version_changes` with correct direction
- [ ] Integration test: compare two SBOMs with differing advisories — verify `new_vulnerabilities` and `resolved_vulnerabilities`
- [ ] Integration test: compare two SBOMs with license changes — verify `license_changes` contains correct entries
- [ ] Integration test: compare identical SBOMs — verify all diff categories are empty
- [ ] Integration test: compare two completely disjoint SBOMs — verify all left packages in removed, all right packages in added

## Verification Commands
- `cargo test --test api sbom_compare` — Run all comparison integration tests, expect all to pass

## Dependencies
- Depends on: Task 2 — Backend comparison endpoint
