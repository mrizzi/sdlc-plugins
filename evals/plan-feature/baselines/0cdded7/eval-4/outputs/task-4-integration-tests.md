# Task 4 — Add integration tests for the license report endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/license-report` endpoint. The tests verify the full stack from HTTP request through service layer to database, covering compliant SBOMs, non-compliant SBOMs, transitive dependency resolution, mixed license scenarios, and edge cases. These tests follow the existing integration test patterns in `tests/api/`.

## Files to Create
- `tests/api/license_report.rs` — Integration tests for the license report endpoint

## Files to Modify
- `tests/Cargo.toml` — Add the license_report test module if test modules are declared there (verify existing pattern)

## Implementation Notes
- Follow the integration test patterns established in `tests/api/sbom.rs` and `tests/api/advisory.rs`:
  - Tests hit a real PostgreSQL test database
  - Use `assert_eq!(resp.status(), StatusCode::OK)` pattern for status code assertions
  - Set up test data by ingesting SBOMs with known package-license configurations
- Test scenarios to cover:
  1. **All compliant**: Ingest an SBOM with packages all under MIT/Apache-2.0 licenses. Verify all groups have `compliant: true` and `summary.non_compliant_count == 0`
  2. **Non-compliant present**: Ingest an SBOM with a package under GPL-3.0-only (denied). Verify the GPL group has `compliant: false` and `summary.non_compliant_count > 0`
  3. **Transitive dependencies**: Ingest an SBOM with a direct dependency that has its own transitive dependencies. Verify transitive packages appear in the report
  4. **Empty SBOM**: Ingest an SBOM with no packages. Verify 200 response with empty groups
  5. **Unknown licenses**: Ingest an SBOM with a package whose license is not in the policy. Verify it uses the default policy action
  6. **Non-existent SBOM**: Request a report for a UUID that does not exist. Verify 404 response
  7. **CI/CD gate scenario**: Verify the response structure supports automated compliance checking (the `summary.non_compliant_count` field enables pipeline pass/fail decisions)
- Each test function must have a doc comment explaining the scenario
- Use given-when-then inline comments for test functions with distinct setup, action, and assertion phases

## Reuse Candidates
- `tests/api/sbom.rs` — Follow the test setup, data seeding, and assertion patterns
- `tests/api/advisory.rs` — Additional reference for integration test structure
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion logic used for test data setup

## Acceptance Criteria
- [ ] All integration tests pass against a PostgreSQL test database
- [ ] Tests cover the compliant, non-compliant, transitive, empty, and 404 scenarios
- [ ] Test assertions verify both HTTP status codes and response body content
- [ ] Tests are independent and can run in any order

## Test Requirements
- [ ] Integration test: SBOM with all-compliant licenses returns report with zero non-compliant groups
- [ ] Integration test: SBOM with denied licenses returns report with non-compliant groups flagged
- [ ] Integration test: SBOM with transitive dependencies includes transitive packages in the report
- [ ] Integration test: empty SBOM returns 200 with empty groups array
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: package with unknown license uses default policy action

## Verification Commands
- `cargo test --test api -- license_report` — Run all license report integration tests, expect all to pass
- `cargo test --test api` — Run full API integration test suite to verify no regressions

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/license-report endpoint

[sdlc-workflow] Description digest: sha256:6ed4380f2789922a5b6abdc9b870a2f4178da69146d626e826dc9e1e5ab9f86b
