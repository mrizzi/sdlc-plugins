## Repository
trustify-backend

## Description
Add integration tests for the license compliance report endpoint. These tests verify the full request-response cycle against a real PostgreSQL test database, ensuring the endpoint returns correct compliance reports for various SBOM and policy configurations. This is the final task that validates the entire feature works end-to-end.

## Files to Create
- `tests/api/license_report.rs` — Integration tests for `GET /api/v2/sbom/{id}/license-report`.

## Files to Modify
- `tests/Cargo.toml` — Add the new test file to the test suite if required by the project's test configuration.

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/sbom.rs` — tests use a shared test harness that spins up a test database, starts the Axum server, and makes HTTP requests using a test client. Assertions use `assert_eq!(resp.status(), StatusCode::OK)` and deserialize response bodies for field-level checks.
- Set up test data by ingesting a sample SBOM with known packages and licenses using the `IngestorService` from `modules/ingestor/src/service/mod.rs`. This ensures realistic package-license relationships exist in the test database.
- Test scenarios to implement:
  1. **Happy path**: Ingest an SBOM with packages having MIT and Apache-2.0 licenses. With the default policy (both allowed), verify all groups have `compliant: true`.
  2. **Non-compliant detection**: Ingest an SBOM with a package using GPL-3.0-only. With the default policy (GPL denied), verify the GPL group has `compliant: false` and `non_compliant_count` is 1.
  3. **Transitive dependencies**: Ingest an SBOM with a transitive dependency chain. Verify transitive packages appear in the report with `transitive: true`.
  4. **404 for unknown SBOM**: Request a license report for a non-existent SBOM ID. Verify HTTP 404 response.
  5. **Empty SBOM**: Ingest an SBOM with no packages. Verify the report returns with empty `groups` and zero counts.
- Place the `license-policy.json` file (or a test-specific variant) in the test fixtures so the endpoint can load it during tests.

## Reuse Candidates
- `tests/api/sbom.rs` — Direct pattern reference for integration test structure, test client setup, and assertion patterns
- `tests/api/advisory.rs` — Additional pattern reference for test setup with entity ingestion
- `modules/ingestor/src/service/mod.rs::IngestorService` — Use to ingest test SBOM data with known packages and licenses
- `entity/src/package_license.rs` — Understand the entity structure to set up correct test data

## Acceptance Criteria
- [ ] All 5 test scenarios pass against a test PostgreSQL database
- [ ] Tests verify both HTTP status codes and response body structure
- [ ] Tests verify compliance flags are correct for allowed, denied, and default-policy license scenarios
- [ ] Tests verify transitive dependency inclusion and marking
- [ ] `cargo test` passes with no errors

## Test Requirements
- [ ] Integration test: Happy path — all-compliant SBOM returns 200 with all groups marked `compliant: true`
- [ ] Integration test: Non-compliant — SBOM with denied license returns report with `compliant: false` group and correct `non_compliant_count`
- [ ] Integration test: Transitive dependencies included and marked with `transitive: true`
- [ ] Integration test: Non-existent SBOM ID returns HTTP 404
- [ ] Integration test: Empty SBOM returns valid report with empty groups and zero counts

## Verification Commands
- `cargo test --test license_report` — All license report integration tests pass

## Dependencies
- Depends on: Task 3 — Add license report REST endpoint
