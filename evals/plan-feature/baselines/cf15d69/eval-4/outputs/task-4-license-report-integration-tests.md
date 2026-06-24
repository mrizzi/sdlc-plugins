## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the license compliance report endpoint. Tests exercise the full request path against a real PostgreSQL test database, verifying correct grouping, compliance evaluation, edge cases, and error handling.

## Files to Modify
- `tests/Cargo.toml` — Add any needed test dependencies (if not already present)

## Files to Create
- `tests/api/license_report.rs` — Integration test suite for `GET /api/v2/sbom/{id}/license-report`

## Implementation Notes
- Per Key Conventions (Testing): Integration tests go in `tests/api/` and hit a real PostgreSQL test database. Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern established in `tests/api/sbom.rs` and `tests/api/advisory.rs`. Applies: task creates a test file in `tests/api/` matching the convention's testing scope.
- Set up test fixtures: ingest a test SBOM with packages that have various licenses (MIT, Apache-2.0, GPL-3.0-only, and one with no license) so the compliance report can be verified against a known policy.
- Verify the JSON response structure matches `{ "groups": [{ "license": ..., "packages": [...], "compliant": ... }] }`.
- Test both the happy path and error paths (missing SBOM, empty SBOM).
- Verify performance characteristics: for a test SBOM with ~100 packages, the report should return well under the 500ms p95 target.

## Reuse Candidates
- Test setup utilities from existing integration tests in `tests/api/sbom.rs` — reuse SBOM ingestion helpers and database setup patterns
- Assertion patterns from `tests/api/advisory.rs` — reuse status code and JSON body assertion style

## Acceptance Criteria
- [ ] At least 5 integration tests covering: happy path with mixed licenses, all-compliant SBOM, SBOM with policy violations, non-existent SBOM ID, and empty SBOM
- [ ] Tests use the real PostgreSQL test database pattern from existing tests
- [ ] Tests verify both the HTTP status code and the response body structure
- [ ] All tests pass in CI

## Test Requirements
- [ ] Test: SBOM with MIT and Apache-2.0 packages returns all groups with `compliant: true` under default policy
- [ ] Test: SBOM with a GPL-3.0-only package returns that group with `compliant: false` under default policy
- [ ] Test: SBOM with a package missing license data returns an "Unknown" group with `compliant: false`
- [ ] Test: Non-existent SBOM ID returns 404
- [ ] Test: SBOM with no packages returns 200 with empty `groups` array
- [ ] Test: Response time for a 100-package SBOM is under 500ms

[sdlc-workflow] Description digest: sha256-md:d2eb8b1b8ac7207deed45f322b4379f65be1167c08041d199f97295ae8a55901
