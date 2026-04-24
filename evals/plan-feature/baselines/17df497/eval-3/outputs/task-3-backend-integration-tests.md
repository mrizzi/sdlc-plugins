# Task 3 — Backend integration tests for SBOM comparison endpoint

## Repository
trustify-backend

## Description
Add comprehensive integration tests for the SBOM comparison endpoint to the existing test suite. Tests must cover the happy path (valid comparison producing correct diff), error paths (missing/invalid parameters, non-existent SBOMs), edge cases (identical SBOMs, SBOMs with no packages), and performance validation for large SBOMs.

## Files to Modify
- `tests/api/sbom.rs` — Add integration test functions for the comparison endpoint alongside existing SBOM endpoint tests

## Implementation Notes
- Follow the existing test patterns in `tests/api/sbom.rs` — tests use `assert_eq!(resp.status(), StatusCode::OK)` and hit a real PostgreSQL test database.
- Test setup should create two SBOMs with known packages, advisories, and licenses using the ingestion service (`IngestorService` in `modules/ingestor/src/service/mod.rs`) or direct entity creation.
- The test should verify the response body shape matches `SbomComparisonResult` by deserializing the JSON response.
- For the performance-related test, create SBOMs with a moderate number of packages (e.g., 100+) to verify the endpoint handles non-trivial comparisons within acceptable time.
- Reference the existing advisory integration tests in `tests/api/advisory.rs` for patterns on how to set up test data involving advisories.
- Use `entity/src/sbom_package.rs` join table to associate packages with SBOMs in test setup.
- Use `entity/src/sbom_advisory.rs` join table to associate advisories with SBOMs in test setup.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM test patterns for test setup, HTTP client usage, and assertion patterns
- `tests/api/advisory.rs` — advisory test patterns for setting up advisory test data
- `modules/ingestor/src/service/mod.rs::IngestorService` — may be useful for creating test SBOMs with packages

## Acceptance Criteria
- [ ] Integration test verifies successful comparison returns 200 with all six diff categories
- [ ] Integration test verifies added packages are correctly identified
- [ ] Integration test verifies removed packages are correctly identified
- [ ] Integration test verifies version changes include correct direction (upgrade/downgrade)
- [ ] Integration test verifies new vulnerabilities include severity from advisory data
- [ ] Integration test verifies resolved vulnerabilities are correctly identified
- [ ] Integration test verifies license changes are correctly identified
- [ ] Integration test verifies 400 response for missing query parameters
- [ ] Integration test verifies 404 response for non-existent SBOM IDs
- [ ] Integration test verifies empty diff for identical SBOMs

## Test Requirements
- [ ] `test_sbom_compare_valid` — create two SBOMs with overlapping and differing packages, verify all diff categories
- [ ] `test_sbom_compare_missing_left_param` — call without `left`, assert 400
- [ ] `test_sbom_compare_missing_right_param` — call without `right`, assert 400
- [ ] `test_sbom_compare_invalid_uuid` — call with malformed UUID, assert 400
- [ ] `test_sbom_compare_nonexistent_sbom` — call with valid but non-existent UUID, assert 404
- [ ] `test_sbom_compare_identical` — compare SBOM with itself, assert all diff lists are empty
- [ ] `test_sbom_compare_version_direction` — verify upgrade vs downgrade classification is correct
- [ ] `test_sbom_compare_vulnerabilities` — verify new and resolved vulnerabilities include severity and advisory details

## Verification Commands
- `cargo test --test api sbom` — all SBOM integration tests pass including new comparison tests

## Dependencies
- Depends on: Task 2 — Backend comparison endpoint and route registration
