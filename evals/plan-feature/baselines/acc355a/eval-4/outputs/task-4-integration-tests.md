# Task 4 — Add integration tests for license report endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the `GET /api/v2/sbom/{id}/license-report` endpoint that verify the end-to-end behavior against a real PostgreSQL test database. Tests should cover the happy path, error cases, and compliance policy behavior.

## Files to Create
- `tests/api/license_report.rs` — Integration test module for the license report endpoint

## Files to Modify
- `tests/Cargo.toml` — Add the new test module if test discovery requires explicit registration (verify against existing test setup)

## Implementation Notes
- Follow the existing integration test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs` — these demonstrate the test database setup, HTTP client usage, and assertion patterns (`assert_eq!(resp.status(), StatusCode::OK)`).
- Test against a real PostgreSQL test database as per the project convention documented in repo-backend.md.
- Each test should:
  1. Set up test data (ingest an SBOM with known packages and licenses)
  2. Call `GET /api/v2/sbom/{id}/license-report`
  3. Assert the response status and body structure
- Test cases to cover:
  - SBOM with packages across multiple license types, verifying correct grouping
  - SBOM with a non-compliant license, verifying `compliant: false` flag
  - SBOM with only compliant licenses, verifying all groups have `compliant: true`
  - Non-existent SBOM ID returns 404
  - SBOM with no packages returns empty groups array
  - SBOM with transitive dependencies includes them in the report
- Use the existing SBOM ingestion test utilities from `tests/api/sbom.rs` to set up test fixtures if helper functions exist there.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM integration tests demonstrating test setup, fixture creation, and assertion patterns
- `tests/api/advisory.rs` — alternative integration test example showing the testing pattern
- `tests/api/search.rs` — additional example of integration test conventions

## Acceptance Criteria
- [ ] All integration tests pass against a PostgreSQL test database
- [ ] Tests cover happy path, error cases, and compliance policy scenarios
- [ ] Tests verify the response structure matches the documented API contract
- [ ] Test file follows the existing naming and organization conventions in `tests/api/`

## Test Requirements
- [ ] Integration test: GET with valid SBOM ID returns 200 and correctly grouped license report
- [ ] Integration test: GET with non-existent SBOM ID returns 404
- [ ] Integration test: report correctly flags non-compliant licenses as `compliant: false`
- [ ] Integration test: report includes transitive dependency licenses
- [ ] Integration test: SBOM with no packages returns report with empty groups

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/license-report endpoint
