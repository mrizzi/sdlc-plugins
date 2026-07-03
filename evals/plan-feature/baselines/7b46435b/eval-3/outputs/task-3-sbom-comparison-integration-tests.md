## Repository
trustify-backend

## Target Branch
main

## Description
Write integration tests for the `GET /api/v2/sbom/compare` endpoint. Tests should cover all response scenarios: valid comparison with expected diff results across all six categories, 404 for non-existent SBOM IDs, 400 for missing query parameters, empty diff when comparing identical SBOMs, and advisory deduplication verification. Tests follow the existing integration test pattern in `tests/api/` which hits a real PostgreSQL test database.

additional_fields: { "labels": ["ai-generated-jira"], "priority": "Critical", "fixVersions": "RHTPA 1.5.0" }

## Files to Create
- `tests/api/sbom_compare.rs` -- integration tests for the SBOM comparison endpoint covering: valid comparison with all diff categories, 404, 400, empty diff, and deduplication scenarios

## Files to Modify
- `tests/Cargo.toml` -- add any necessary test dependencies if not already present (verify existing dependencies first before modifying)

## Implementation Notes
Follow the existing integration test pattern in `tests/api/sbom.rs` for test structure, database setup, and assertion style. Tests should:

1. Set up test data: ingest two SBOMs with known packages, advisories, and licenses using the existing ingestion pipeline from `modules/ingestor/src/graph/sbom/mod.rs`
2. Call the comparison endpoint via HTTP client
3. Assert response status and body structure

Test cases to implement:
- `test_compare_sboms_added_removed_packages`: two SBOMs with different package sets, verify added_packages and removed_packages arrays
- `test_compare_sboms_version_changes`: two SBOMs with same packages but different versions, verify version_changes array with correct direction (upgrade/downgrade)
- `test_compare_sboms_vulnerability_diff`: two SBOMs with different advisory links, verify new_vulnerabilities and resolved_vulnerabilities arrays with severity
- `test_compare_sboms_license_changes`: two SBOMs where a package's license changed, verify license_changes array
- `test_compare_sboms_identical`: two identical SBOMs, verify all six diff arrays are empty
- `test_compare_sboms_missing_param`: call without `left` or `right`, verify 400 status
- `test_compare_sboms_not_found`: call with non-existent SBOM UUID, verify 404 status

Use the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern from existing tests in `tests/api/sbom.rs`.

Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern.
Applies: task creates `tests/api/sbom_compare.rs` matching the convention's test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` -- existing SBOM endpoint integration tests; follow the same test setup, database fixtures, and assertion patterns
- `tests/api/advisory.rs` -- existing advisory endpoint tests; reference for advisory-related test data setup
- `modules/ingestor/src/graph/sbom/mod.rs` -- SBOM ingestion logic; use to set up test data with known packages and advisories
- `modules/ingestor/src/graph/advisory/mod.rs` -- advisory ingestion logic; use to set up advisory test data with known severities

## Acceptance Criteria
- [ ] All integration tests pass against a PostgreSQL test database
- [ ] Tests cover all six diff categories (added/removed packages, version changes, new/resolved vulnerabilities, license changes)
- [ ] Tests verify 400 response for missing query parameters
- [ ] Tests verify 404 response for non-existent SBOM IDs
- [ ] Tests verify empty diff when comparing identical SBOMs
- [ ] Advisory deduplication is verified (same advisory linked multiple times does not produce duplicate entries)

## Test Requirements
- [ ] At least 7 test functions covering the scenarios listed in Implementation Notes
- [ ] Each test uses fresh test data to avoid cross-test contamination
- [ ] Tests verify both response status codes and response body content
- [ ] Tests verify the structure and field names of the response JSON match `SbomComparisonResult`

## Verification Commands
- `cargo test -p trustify-tests sbom_compare` -- all integration tests pass

## Dependencies
- Depends on: Task 2 -- Implement SBOM comparison REST endpoint
