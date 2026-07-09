## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add integration tests for the SBOM comparison endpoint (`GET /api/v2/sbom/compare`) that verify the full request-response cycle against a real PostgreSQL test database. Tests should cover all six diff categories, error cases, and edge cases to ensure the endpoint behaves correctly end-to-end.

## Files to Create
- `tests/api/sbom_compare.rs` — Integration tests for the comparison endpoint covering: successful comparison with all diff categories, empty diff (identical SBOMs), error cases (missing params, invalid IDs), and edge cases (large SBOMs)

## Implementation Notes
- Follow the integration test pattern in `tests/api/sbom.rs` for test structure, database setup, and HTTP client usage.
  Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task creates `tests/api/sbom_compare.rs` matching the convention's Rust test file scope.
- Set up test data by ingesting two SBOM fixtures with known differences:
  - SBOM A: packages [pkg-a@1.0, pkg-b@2.0, pkg-c@3.0] with advisories [CVE-2024-001]
  - SBOM B: packages [pkg-a@1.1, pkg-c@3.0, pkg-d@4.0] with advisories [CVE-2024-002]
  - Expected diff: added=[pkg-d], removed=[pkg-b], version_changes=[pkg-a 1.0->1.1 upgrade], new_vulns=[CVE-2024-002], resolved_vulns=[CVE-2024-001]
- Use the `IngestorService` from `modules/ingestor/src/service/mod.rs` to set up test SBOM data.
- Verify response JSON structure matches the SbomComparisonResult contract from `modules/fundamental/src/sbom/model/comparison.rs`.
- Test the p95 < 1s NFR by including a test case with a larger fixture (~100 packages) and asserting response time.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM endpoint tests; follow the same test setup, database initialization, and assertion patterns
- `modules/ingestor/src/service/mod.rs::IngestorService` — use for setting up test SBOM data in the database
- `tests/api/advisory.rs` — existing advisory endpoint tests; reference for advisory-related test data setup

## Acceptance Criteria
- [ ] All integration tests pass against a PostgreSQL test database
- [ ] Tests cover the successful comparison path with all six diff categories populated
- [ ] Tests verify empty diff when comparing identical SBOMs
- [ ] Tests verify 400 response for missing query parameters
- [ ] Tests verify 404 response for non-existent SBOM IDs
- [ ] Tests verify the response JSON structure matches the SbomComparisonResult contract

## Test Requirements
- [ ] Integration test: compare two SBOMs with known package differences; verify added_packages, removed_packages, and version_changes are correct
- [ ] Integration test: compare two SBOMs with known advisory differences; verify new_vulnerabilities and resolved_vulnerabilities are correct
- [ ] Integration test: compare two SBOMs with known license changes; verify license_changes is correct
- [ ] Integration test: compare identical SBOMs; verify all diff categories are empty arrays
- [ ] Integration test: request with missing left parameter returns 400
- [ ] Integration test: request with non-existent SBOM ID returns 404

## Verification Commands
- `cargo test -p trustify-integration-tests -- sbom_compare` — all comparison integration tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 3 — Add SBOM comparison REST endpoint
