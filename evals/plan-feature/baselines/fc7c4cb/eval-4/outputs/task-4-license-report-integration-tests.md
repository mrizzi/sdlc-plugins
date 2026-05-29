## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the license compliance report endpoint. These tests exercise the full request-response cycle against a real PostgreSQL test database, verifying correct license grouping, compliance policy evaluation, transitive dependency inclusion, and error handling. The test suite serves as the primary verification mechanism for the feature's acceptance criteria and as a regression safety net.

## Files to Modify
- `tests/Cargo.toml` — add any necessary test dependencies if not already present

## Files to Create
- `tests/api/license_report.rs` — integration tests for `GET /api/v2/sbom/{id}/license-report`

## Implementation Notes
- Follow the integration test pattern established in `tests/api/sbom.rs` and `tests/api/advisory.rs` for test setup, database fixtures, HTTP client usage, and assertion style (e.g., `assert_eq!(resp.status(), StatusCode::OK)`).
- Set up test fixtures that create:
  - An SBOM with multiple packages having different licenses (e.g., MIT, Apache-2.0, GPL-3.0)
  - A license policy configuration that marks GPL-3.0 as denied
  - An SBOM with transitive dependencies to verify they are included in the report
  - An SBOM with no packages (edge case)
- Test scenarios should cover:
  - Happy path: SBOM with mixed licenses returns correctly grouped report with compliance flags
  - All compliant: SBOM where all package licenses are in the allowed list
  - Policy violations: SBOM with packages using denied licenses are flagged as non-compliant
  - Transitive dependencies: packages from transitive dependencies appear in the report
  - Empty SBOM: returns valid response with empty groups
  - Nonexistent SBOM: returns 404 or appropriate error status
  - Response shape: verify the JSON structure matches the expected `LicenseReport` schema
- Register the new test module in the test harness (check if `tests/api/` uses a `mod.rs` or if Cargo discovers test files automatically).

## Reuse Candidates
- `tests/api/sbom.rs` — direct reference for test setup patterns, fixture creation, HTTP assertions, and database interaction in tests
- `tests/api/advisory.rs` — additional reference for integration test structure and assertion patterns
- `tests/api/search.rs` — reference for testing endpoints that aggregate data from multiple entities

## Acceptance Criteria
- [ ] All integration tests pass against a PostgreSQL test database
- [ ] Tests cover the happy path (mixed licenses grouped correctly), policy violation flagging, transitive dependency inclusion, empty SBOM edge case, and nonexistent SBOM error case
- [ ] Tests verify the JSON response structure matches the `LicenseReport` schema
- [ ] Tests are consistent with the existing test patterns in `tests/api/`
- [ ] No flaky tests — each test creates its own isolated fixtures

## Test Requirements
- [ ] Integration test: happy path — SBOM with 3+ packages across 2+ license types returns grouped report with correct `compliant` flags
- [ ] Integration test: all-compliant — SBOM where every package license is allowed returns all groups with `compliant: true`
- [ ] Integration test: policy violation — SBOM with a package using a denied license returns the group with `compliant: false` and `policy_violations > 0`
- [ ] Integration test: transitive dependencies — packages from transitive dependencies appear in license groups
- [ ] Integration test: empty SBOM — SBOM with no packages returns 200 with empty `groups` array
- [ ] Integration test: nonexistent SBOM — request for non-existent SBOM ID returns 404
- [ ] Integration test: response schema — verify top-level fields (`sbom_id`, `groups`, `policy_violations`, `generated_at`) are present and correctly typed

## Dependencies
- Depends on: Task 1 — License report models and policy configuration
- Depends on: Task 2 — License report service
- Depends on: Task 3 — License report endpoint

[sdlc-workflow] Description digest: sha256:5dc71812f4163d7ce715eebf48e7a7fcb5a1170e1aaa480e00311c5802a29468
