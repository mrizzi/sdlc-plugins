## Repository
trustify-backend

## Description
Add end-to-end integration tests for the license compliance report endpoint, verifying the complete flow from HTTP request through service layer to database and back. These tests ensure the feature works correctly with a real PostgreSQL test database, covering the happy path, error cases, and compliance logic. This is the final task for TC-9004.

## Files to Create
- `tests/api/license_report.rs` — Integration tests for `GET /api/v2/sbom/{id}/license-report` covering various scenarios including SBOMs with compliant packages, non-compliant packages, mixed compliance, empty SBOMs, and invalid SBOM IDs

## Files to Modify
- `tests/Cargo.toml` — Add the test file to the test harness if needed (depending on how the test suite is organized)

## Implementation Notes
- Follow the integration test pattern established in `tests/api/sbom.rs` — set up a test database, ingest test SBOM data with known packages and licenses, then call the endpoint and assert on the response.
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern documented in the repository conventions.
- Test data setup should insert SBOM records with packages having known licenses that map to both allowed and denied entries in the test license policy. This verifies the compliance flagging end-to-end.
- Include a test with an SBOM containing packages with licenses from different categories (e.g., MIT as allowed, GPL-3.0 as denied) to verify that groups have the correct `compliant` flag values.
- Include a test that verifies the `summary` field counts match the actual groups in the response.
- Include a test for a non-existent SBOM ID returning a 404 status.
- Include a test for an SBOM with no packages, verifying the response has an empty `groups` array and zero counts in `summary`.
- Reference the existing test setup helpers used in `tests/api/sbom.rs` and `tests/api/advisory.rs` for database initialization and HTTP client setup.

## Reuse Candidates
- `tests/api/sbom.rs` — Test structure, database setup, and HTTP client patterns to follow
- `tests/api/advisory.rs` — Additional reference for integration test patterns

## Acceptance Criteria
- [ ] Integration tests cover the happy path with compliant and non-compliant packages
- [ ] Integration tests cover the 404 case for non-existent SBOM IDs
- [ ] Integration tests cover the edge case of an SBOM with no packages
- [ ] Integration tests verify the response JSON structure matches the API contract
- [ ] Integration tests verify compliance flags are correctly derived from the license policy
- [ ] All tests pass against a real PostgreSQL test database

## Test Requirements
- [ ] Test: Valid SBOM with mixed licenses returns 200 with correct compliance flags per group
- [ ] Test: Non-existent SBOM ID returns 404
- [ ] Test: SBOM with no packages returns 200 with empty groups and zero summary counts
- [ ] Test: Response `summary.total` equals the sum of packages across all groups
- [ ] Test: All packages with allowed licenses are in groups marked `compliant: true`
- [ ] Test: All packages with denied licenses are in groups marked `compliant: false`

## Verification Commands
- `cargo test --test api -- license_report` — All integration tests pass

## Dependencies
- Depends on: Task 3 — License report endpoint (provides the endpoint to test)
