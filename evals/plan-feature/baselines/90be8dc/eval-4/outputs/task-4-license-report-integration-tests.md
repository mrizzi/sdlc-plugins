## Repository
trustify-backend

## Description
Add integration tests for the license report endpoint, covering the happy path (SBOM with mixed compliant and non-compliant licenses), edge cases (SBOM with no packages, packages with no license data), error cases (non-existent SBOM ID), and the automated compliance gate use case (verifying the `compliant` field can be used to gate CI/CD pipelines).

## Files to Create
- `tests/api/license_report.rs` — Integration tests for `GET /api/v2/sbom/{id}/license-report`

## Files to Modify
- `tests/Cargo.toml` — Ensure any new test dependencies are included (if needed)

## Implementation Notes
Follow the integration test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs`. These tests use a real PostgreSQL test database and the `assert_eq!(resp.status(), StatusCode::OK)` pattern. The test setup should:

1. Ingest an SBOM with known packages and licenses via the existing ingestion infrastructure (reference `modules/ingestor/src/graph/sbom/mod.rs` for the ingestion path)
2. Set up a license policy configuration for the test (e.g., MIT allowed, GPL-3.0 denied)
3. Call the endpoint and validate the response structure and compliance flags

Test cases to implement:
- Happy path: SBOM with packages under MIT (compliant) and GPL-3.0 (non-compliant) licenses; verify grouping and flags
- Empty SBOM: SBOM with no packages returns an empty groups array
- Unknown license: Package with no license entry is grouped under "Unknown" and flagged non-compliant
- Non-existent SBOM: Returns 404
- CI/CD gate use case: Verify that the response can be checked programmatically for any `compliant: false` group

## Reuse Candidates
- `tests/api/sbom.rs` — Test setup patterns for SBOM-related integration tests, including test database setup and SBOM ingestion
- `tests/api/advisory.rs` — Additional test patterns for API endpoint testing
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion logic for setting up test data

## Acceptance Criteria
- [ ] All integration tests pass against a test PostgreSQL database
- [ ] Happy path test validates correct grouping by license and correct compliance flags
- [ ] Edge case tests cover empty SBOMs and missing license data
- [ ] Error case test confirms 404 for non-existent SBOM
- [ ] Tests validate the JSON response structure matches the API contract

## Test Requirements
- [ ] Integration test: SBOM with mixed licenses returns correct groups and compliance flags
- [ ] Integration test: SBOM with no packages returns empty groups
- [ ] Integration test: Package with no license is grouped as "Unknown" and non-compliant
- [ ] Integration test: Non-existent SBOM ID returns 404
- [ ] Integration test: Response structure matches `{ groups: [{ license, packages, compliant }] }`

## Verification Commands
- `cargo test -p trustify-tests -- license_report` — All integration tests pass

## Dependencies
- Depends on: Task 3 — Add license report endpoint and route registration
