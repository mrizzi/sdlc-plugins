# Task 4: Add integration tests for the license-report endpoint

## Repository

trustify-backend

## Target Branch

main

## Description

Add integration tests for the `GET /api/v2/sbom/{id}/license-report` endpoint. These tests verify the full request-response cycle against a real PostgreSQL test database, covering the happy path, edge cases, and error conditions. The tests also validate that the license policy evaluation produces correct compliance flags.

## Files to Create

- `tests/api/license_report.rs` -- Integration tests for the license-report endpoint. Tests should cover:
  1. **Happy path**: Ingest an SBOM with packages having known licenses, call the endpoint, verify the response contains correctly grouped licenses with accurate compliance flags.
  2. **Non-compliant licenses detected**: Configure a policy that denies a specific license, ingest an SBOM with a package using that license, verify the group is flagged `compliant: false` and the summary reflects the violation.
  3. **Empty SBOM**: Call the endpoint for an SBOM with no packages, verify an empty `groups` array and zeroed summary counts.
  4. **SBOM not found**: Call the endpoint with a non-existent UUID, verify `404` response.
  5. **Summary accuracy**: Verify `total_packages`, `total_licenses`, `compliant_count`, and `non_compliant_count` are correctly computed for a multi-license SBOM.

## Files to Modify

- `tests/Cargo.toml` -- Add the new test file to the test configuration if the test harness requires explicit registration (check existing pattern with `sbom.rs`, `advisory.rs`, `search.rs`).

## Implementation Notes

- Follow the existing integration test pattern in `tests/api/sbom.rs`: set up a test database, use the application's HTTP client to make requests, and assert on response status codes and body content.
- Use `assert_eq!(resp.status(), StatusCode::OK)` for status assertions, matching the convention documented in the repository.
- For test fixtures, ingest a minimal SBOM with a few packages having distinct licenses (e.g., MIT, Apache-2.0, GPL-3.0). Use the existing `IngestorService` to set up test data.
- Provide a test license policy JSON fixture that approves MIT and Apache-2.0 but denies GPL-3.0, so the compliance logic can be verified.
- Deserialize the response body into `LicenseReport` and assert on individual fields rather than comparing raw JSON strings.

## Acceptance Criteria

- [ ] All five test scenarios listed above are implemented and pass
- [ ] Tests use a real PostgreSQL test database (not mocks)
- [ ] Tests follow the existing assertion pattern (`assert_eq!` with `StatusCode`)
- [ ] Test fixtures are self-contained and do not depend on external data
- [ ] Tests validate both the structure and content of the `LicenseReport` response
- [ ] `cargo test` passes with no failures or warnings

## Test Requirements

- This task is entirely about tests. All five scenarios described above must be implemented as `#[tokio::test]` async test functions in `tests/api/license_report.rs`.

[Description digest: sha256-md:d9e52a3b1f6c084275f7e3cb8a512d7f06cf43e91f85b69d73e142a0d9f386c5 would be posted as a comment]
