## Repository
trustify-backend

## Description
Add comprehensive integration tests for the SBOM comparison endpoint. These tests verify the full request-response cycle against a real PostgreSQL test database, ensuring that the diff logic produces correct results for various scenarios including identical SBOMs, SBOMs with different packages, version changes, vulnerability differences, and license changes.

## Files to Create
- `tests/api/sbom_compare.rs` — Integration tests for `GET /api/v2/sbom/compare`

## Files to Modify
- `tests/api/mod.rs` or equivalent test module root — Register `mod sbom_compare;` if a module file exists, or ensure the new test file is discovered by the test harness

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/sbom.rs`. Tests should set up test data by ingesting two SBOMs with known package sets, then call the comparison endpoint and assert the response structure.
- Use the same test database setup and teardown approach as `tests/api/sbom.rs` and `tests/api/advisory.rs`.
- Use `assert_eq!(resp.status(), StatusCode::OK)` for success cases and `assert_eq!(resp.status(), StatusCode::BAD_REQUEST)` / `StatusCode::NOT_FOUND` for error cases, following the convention in existing test files.
- Test scenarios should cover:
  - Two SBOMs where the right has additional packages (verifies `added_packages`)
  - Two SBOMs where the left has packages removed in the right (verifies `removed_packages`)
  - Packages with version changes between SBOMs (verifies `version_changes` with correct direction)
  - Advisories linked differently between SBOMs (verifies `new_vulnerabilities` and `resolved_vulnerabilities`)
  - Packages with changed licenses (verifies `license_changes`)
  - Comparing an SBOM with itself (verifies all diff arrays are empty)
  - Performance: comparison of SBOMs with a moderate number of packages completes within test timeout
- Use the SBOM ingestion service from `modules/ingestor/src/service/mod.rs` to set up test data, and the advisory ingestion from `modules/ingestor/src/graph/advisory/mod.rs` to link advisories.

## Reuse Candidates
- `tests/api/sbom.rs` — Follow the same test structure and setup patterns
- `tests/api/advisory.rs` — Reference for creating advisory test fixtures
- `modules/ingestor/src/service/mod.rs::IngestorService` — Use to ingest test SBOMs
- `modules/ingestor/src/graph/advisory/mod.rs` — Use to create test advisories

## Acceptance Criteria
- [ ] All integration tests pass against the test PostgreSQL database
- [ ] Tests cover all six diff categories: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, license changes
- [ ] Tests verify error responses for invalid inputs
- [ ] Tests verify empty diff when comparing an SBOM with itself

## Test Requirements
- [ ] Integration test: comparing SBOMs with added packages returns correct `added_packages` array
- [ ] Integration test: comparing SBOMs with removed packages returns correct `removed_packages` array
- [ ] Integration test: comparing SBOMs with version changes returns correct `version_changes` with direction
- [ ] Integration test: comparing SBOMs with different advisories returns correct `new_vulnerabilities` and `resolved_vulnerabilities`
- [ ] Integration test: comparing SBOMs with license changes returns correct `license_changes`
- [ ] Integration test: self-comparison returns empty arrays for all diff categories
- [ ] Integration test: invalid SBOM ID returns 404
- [ ] Integration test: missing query parameters return 400

## Verification Commands
- `cargo test -p trustify-tests -- api::sbom_compare` — All comparison integration tests pass

## Dependencies
- Depends on: Task 2 — SBOM comparison endpoint
