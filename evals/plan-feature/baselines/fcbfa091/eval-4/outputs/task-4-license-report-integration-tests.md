## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the license compliance report endpoint that exercise the full stack against a real PostgreSQL test database. Tests cover the primary use cases: generating a report for an SBOM with mixed compliant/non-compliant licenses, verifying transitive dependency inclusion, handling of empty SBOMs, and the CI/CD compliance gate scenario where the pipeline checks for non-compliant licenses.

## Files to Create
- `tests/api/license_report.rs` — Integration tests for `GET /api/v2/sbom/{id}/license-report`

## Files to Modify
- `tests/Cargo.toml` — Add the new test file to the test targets if needed (depends on project test configuration)

## Implementation Notes
Follow the integration test patterns established in `tests/api/sbom.rs` and `tests/api/advisory.rs`. These tests hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern.

Test setup should:
1. Ingest a test SBOM with known packages and license data (using the ingestion pipeline or direct database setup).
2. Configure a test license policy with specific allowed licenses.
3. Call the endpoint and assert on the response structure and values.

Test cases to implement:

**Test 1: Report with mixed compliance**
- Set up an SBOM with packages under MIT (compliant), Apache-2.0 (compliant), and GPL-3.0 (non-compliant per policy).
- Assert: response has 3 license groups, GPL-3.0 group has `compliant: false`, others have `compliant: true`.
- Assert: `non_compliant_count` equals the number of GPL-3.0 packages.

**Test 2: Transitive dependencies included**
- Set up an SBOM where package A depends on package B (transitive).
- Assert: both A and B appear in the report groups.

**Test 3: All licenses compliant**
- Set up an SBOM with only MIT-licensed packages.
- Assert: all groups have `compliant: true`, `non_compliant_count` is 0.

**Test 4: Non-existent SBOM**
- Call the endpoint with a non-existent SBOM ID.
- Assert: response status is 404.

**Test 5: SBOM with no packages**
- Set up an SBOM with no associated packages.
- Assert: response has empty `groups` array, `total_packages` is 0.

Per CONVENTIONS.md (Key Conventions from repository structure): integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task creates `tests/api/license_report.rs` matching the convention's `.rs` test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — Existing SBOM integration tests; reuse test setup, database fixtures, and assertion patterns
- `tests/api/advisory.rs` — Additional reference for test structure and HTTP client setup

## Acceptance Criteria
- [ ] At least 5 integration tests covering the scenarios listed above
- [ ] Tests run against a real PostgreSQL test database (not mocks)
- [ ] Tests verify response status codes, JSON structure, and compliance flag correctness
- [ ] Tests verify transitive dependency inclusion in the report
- [ ] All tests pass with `cargo test`

## Test Requirements
- [ ] Integration test: mixed compliance report (MIT + GPL-3.0)
- [ ] Integration test: transitive dependencies appear in report
- [ ] Integration test: fully compliant SBOM returns zero non-compliant count
- [ ] Integration test: non-existent SBOM returns 404
- [ ] Integration test: SBOM with no packages returns empty report

## Dependencies
- Depends on: Task 3 — Add license report endpoint handler and route registration

## additional_fields
- labels: ai-generated-jira
- priority: Major
- fixVersions: RHTPA 1.5.0
