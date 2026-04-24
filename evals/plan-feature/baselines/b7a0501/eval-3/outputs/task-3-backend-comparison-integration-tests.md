## Repository
trustify-backend

## Description
Add comprehensive integration tests for the SBOM comparison endpoint (`GET /api/v2/sbom/compare`). These tests verify the full request-response cycle against a real PostgreSQL test database, covering successful comparisons, error cases, and edge cases like comparing an SBOM against itself. This ensures the comparison feature (TC-9003) works end-to-end at the backend level before frontend integration.

## Files to Create
- `tests/api/sbom_compare.rs` — Integration tests for the comparison endpoint

## Files to Modify
- `tests/api/mod.rs` or equivalent test root — Register the new `sbom_compare` test module (if the test crate uses module declarations)

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/sbom.rs` and `tests/api/advisory.rs` — tests hit a real PostgreSQL test database using the project's test harness.
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern established in existing tests.
- Test setup should ingest two distinct SBOMs with known package sets, advisories, and licenses to produce deterministic diff results.
- For the "same SBOM" test case, compare an SBOM against itself and verify all diff sections are empty arrays.
- For the "different SBOMs" test case, set up SBOMs where:
  - SBOM A has packages P1 and P2; SBOM B has packages P2 and P3 (so P3 is added, P1 is removed)
  - P2 has different versions in each SBOM (to test version changes)
  - SBOM B has an advisory not in SBOM A (to test new vulnerabilities)
  - SBOM A has an advisory not in SBOM B (to test resolved vulnerabilities)
  - P2 has different licenses in each SBOM (to test license changes)
- Test the 400 error response for missing query parameters.
- Test the 404 error response for non-existent SBOM IDs.
- Verify the response JSON deserializes into the `SbomComparison` struct correctly.

## Reuse Candidates
- `tests/api/sbom.rs` — Reference for test structure, setup patterns, and assertion style
- `tests/api/advisory.rs` — Reference for advisory-related test data setup
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion logic for creating test data
- `modules/ingestor/src/graph/advisory/mod.rs` — Advisory ingestion logic for creating test data

## Acceptance Criteria
- [ ] Integration test passes for a successful comparison between two different SBOMs with all six diff categories populated
- [ ] Integration test passes for comparing an SBOM against itself (all diff arrays are empty)
- [ ] Integration test passes for missing `left` query parameter (returns 400)
- [ ] Integration test passes for missing `right` query parameter (returns 400)
- [ ] Integration test passes for non-existent SBOM ID (returns 404)
- [ ] All existing SBOM endpoint tests continue to pass

## Test Requirements
- [ ] Test: `compare_different_sboms` — Ingest two SBOMs with known differences, call the compare endpoint, assert each diff section contains the expected items
- [ ] Test: `compare_same_sbom` — Compare an SBOM against itself, assert all diff arrays are empty
- [ ] Test: `compare_missing_left_param` — Call without `left` parameter, assert 400 status
- [ ] Test: `compare_missing_right_param` — Call without `right` parameter, assert 400 status
- [ ] Test: `compare_nonexistent_sbom` — Call with a non-existent SBOM ID, assert 404 status
- [ ] Test: `compare_version_change_direction` — Verify upgrade/downgrade direction is correctly determined

## Dependencies
- Depends on: Task 2 — Backend comparison endpoint
