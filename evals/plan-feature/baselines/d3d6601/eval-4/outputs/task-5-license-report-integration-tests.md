## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the license compliance report endpoint. These tests exercise the full request-response cycle against a real PostgreSQL test database, verifying correct grouping, compliance flagging, transitive dependency inclusion, and error handling. The tests follow the existing integration test patterns in `tests/api/`.

## Files to Modify
- `tests/Cargo.toml` — add any test-specific dependencies if needed (e.g., test fixture helpers)

## Files to Create
- `tests/api/license_report.rs` — integration tests for `GET /api/v2/sbom/{id}/license-report`

## Implementation Notes
- Follow the existing integration test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs` — tests use a real PostgreSQL test database and follow the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern.
- Test setup should ingest a known SBOM with packages that have specific licenses (both compliant and non-compliant per the default policy) to verify grouping and flagging behavior.
- Include test cases for:
  - A valid SBOM with a mix of compliant and non-compliant licenses
  - A valid SBOM where all licenses are compliant (no violations)
  - A valid SBOM with transitive dependencies to verify they appear in the report
  - A nonexistent SBOM ID returning HTTP 404
  - An SBOM with no packages (edge case — should return empty groups)
- Ensure the test module is registered in the test crate (add `mod license_report;` to the appropriate module file).
- Performance verification: include at least one test with a moderately sized SBOM to sanity-check that report generation completes within the expected timeframe (though full p95 benchmarking is separate).

## Reuse Candidates
- `tests/api/sbom.rs` — demonstrates the established integration test pattern for SBOM endpoints, including test database setup, request building, and response assertion
- `tests/api/advisory.rs` — shows another example of the integration test pattern with different entity types
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion logic that tests can use to set up test fixtures with known package-license data

## Acceptance Criteria
- [ ] All integration test cases pass against a PostgreSQL test database
- [ ] Tests cover compliant, non-compliant, mixed, and empty SBOM scenarios
- [ ] Tests verify correct HTTP status codes (200, 404)
- [ ] Tests verify the response JSON structure matches the `LicenseReport` schema
- [ ] Tests verify transitive dependency licenses are included

## Test Requirements
- [ ] Integration test: valid SBOM with mixed licenses returns correct groups and compliance flags
- [ ] Integration test: valid SBOM with all-compliant licenses returns all groups as compliant
- [ ] Integration test: nonexistent SBOM ID returns HTTP 404
- [ ] Integration test: SBOM with transitive dependencies includes them in the report
- [ ] Integration test: SBOM with no packages returns empty groups array

## Verification Commands
- `cargo test -p trustify-tests -- license_report` — all integration tests pass

## Dependencies
- Depends on: Task 4 — Add license report endpoint

[sdlc-workflow] Description digest: sha256:1e5dfb97fd01754857f6503d1558bb93e733e2b9c31ae54b373c887de9b00322
