## Repository
trustify-backend

## Description
Add comprehensive integration tests for the license compliance report endpoint. These tests verify the full request-response cycle against a real PostgreSQL test database, covering the happy path, error cases, compliance policy evaluation, and edge cases like SBOMs with no packages or packages with no license data.

## Files to Create
- `tests/api/license_report.rs` — Integration tests for `GET /api/v2/sbom/{id}/license-report` covering multiple scenarios

## Files to Modify
- `tests/Cargo.toml` — Add the new test file to the test suite if required by the project's test configuration

## Implementation Notes
- Follow the existing integration test pattern from `tests/api/sbom.rs` — tests hit a real PostgreSQL test database, use `assert_eq!(resp.status(), StatusCode::OK)` for status assertions, and deserialize response bodies for structural validation
- Test setup: use the existing SBOM ingestion service (`modules/ingestor/src/graph/sbom/mod.rs`) to create test SBOMs with known package-license data before running report assertions
- Each test function must include a doc comment explaining what scenario it covers
- For non-trivial tests (most of these), include given-when-then inline comments to structure the setup, action, and assertion phases
- Test scenarios to cover:
  1. **Happy path**: Ingest an SBOM with packages having MIT and Apache-2.0 licenses, call the report endpoint, verify groups are correct and compliant flags are true
  2. **Non-compliant license**: Ingest an SBOM with a package using a denied license (e.g., GPL-3.0 when policy denies it), verify the corresponding group has `compliant: false`
  3. **Non-existent SBOM**: Call the endpoint with a random UUID, verify 404 response
  4. **SBOM with no packages**: Ingest an empty SBOM, verify the report returns an empty groups array
  5. **Mixed compliance**: Ingest an SBOM with both compliant and non-compliant licenses, verify each group has the correct flag
- Per constraints doc section 5.9: prefer parameterized tests when multiple test cases exercise the same behavior with different inputs (e.g., the compliant vs non-compliant scenarios could be parameterized if the project supports it, but verify sibling test patterns first per section 5.10)
- Per constraints doc section 5.11: add a doc comment to every test function
- Per constraints doc section 5.12: add given-when-then inline comments to non-trivial test functions

## Reuse Candidates
- `tests/api/sbom.rs` — demonstrates the established integration test pattern for SBOM-related endpoints (test setup, HTTP request construction, response assertion)
- `tests/api/advisory.rs` — another integration test example showing how to set up test data and assert response shapes
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion logic to reuse for creating test fixtures with known package-license data

## Acceptance Criteria
- [ ] All integration tests pass against the PostgreSQL test database
- [ ] Tests cover the happy path, error cases (404), compliance evaluation (compliant and non-compliant), and edge cases (empty SBOM)
- [ ] Test assertions verify both HTTP status codes and response body structure/content
- [ ] Each test function has a doc comment and non-trivial tests have given-when-then inline comments

## Test Requirements
- [ ] Integration test: Happy path — SBOM with known licenses returns correct groups with correct compliance flags
- [ ] Integration test: Non-compliant license — denied license produces `compliant: false` in the corresponding group
- [ ] Integration test: Non-existent SBOM — returns HTTP 404
- [ ] Integration test: Empty SBOM — returns 200 with empty groups array
- [ ] Integration test: Mixed compliance — SBOM with both compliant and non-compliant licenses returns correct flags for each group

## Verification Commands
- `cargo test -p trustify-tests --test license_report` — all license report integration tests pass

## Dependencies
- Depends on: Task 3 — License report API endpoint
