## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the license compliance report endpoint. These tests verify the full stack from HTTP request through service logic to database, ensuring the endpoint returns correctly structured reports with proper compliance flagging. This follows the existing integration test pattern used for SBOM and advisory endpoints.

## Files to Create
- `tests/api/license_report.rs` — Integration tests for `GET /api/v2/sbom/{id}/license-report`

## Files to Modify
- `tests/Cargo.toml` — Add the test file to the test suite if required by the project's test configuration

## Implementation Notes
Follow the integration test pattern established in `tests/api/sbom.rs` and `tests/api/advisory.rs`. These tests use a real PostgreSQL test database and follow the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern.

Test setup should:
1. Ingest an SBOM with known packages and license data (leverage the ingestion flow in `modules/ingestor/src/graph/sbom/mod.rs`)
2. Place a test license policy file (or use the default policy)
3. Call the endpoint and verify the response

Key test cases:

**TC-1: Basic report generation** — Ingest an SBOM with packages having MIT and Apache-2.0 licenses. Call the endpoint. Verify the response contains two license groups, both marked compliant (neither is in the default deny list). Verify each group contains the expected packages.

**TC-2: Non-compliant license detection** — Ingest an SBOM with a package having GPL-3.0-only license. Call the endpoint. Verify the GPL-3.0-only group has `compliant: false`.

**TC-3: Unknown license handling** — Ingest an SBOM with a package that has no license data in the `package_license` table. Verify it appears in an "Unknown" group with `compliant: false`.

**TC-4: Non-existent SBOM** — Call the endpoint with a non-existent SBOM ID. Verify HTTP 404 response.

**TC-5: Transitive dependencies** — Ingest an SBOM with a dependency chain (A depends on B, B depends on C). Verify all three packages appear in the report, including the transitively included package C.

**TC-6: Response structure** — Verify the JSON response includes all required fields: `sbom_id`, `groups` (with `license`, `packages`, `compliant`), `generated_at`, and `policy_name`.

All assertions should use `assert_eq!` with `StatusCode` variants as done in sibling test files.

## Reuse Candidates
- `tests/api/sbom.rs` — SBOM endpoint integration tests; follow the same test setup, client configuration, and assertion patterns
- `tests/api/advisory.rs` — advisory endpoint integration tests; additional reference for test structure
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion logic to use in test setup for creating test data

## Acceptance Criteria
- [ ] Integration tests cover: basic report generation, non-compliant license detection, unknown license handling, non-existent SBOM (404), transitive dependencies, and response structure validation
- [ ] All tests follow the existing integration test pattern (real PostgreSQL, `StatusCode` assertions)
- [ ] Tests pass against a clean test database
- [ ] No test creates or relies on backdoor endpoints

## Test Requirements
- [ ] TC-1: SBOM with compliant licenses returns all groups with `compliant: true`
- [ ] TC-2: SBOM with a denied license returns that group with `compliant: false`
- [ ] TC-3: Package without license data appears in "Unknown" group marked non-compliant
- [ ] TC-4: Non-existent SBOM ID returns HTTP 404
- [ ] TC-5: Transitive dependencies are included in the report
- [ ] TC-6: Response JSON contains all required fields with correct types

## Verification Commands
- `cargo test -p trustify-tests license_report` — all integration tests should pass

## Dependencies
- Depends on: Task 4 — Add license report endpoint and route registration
