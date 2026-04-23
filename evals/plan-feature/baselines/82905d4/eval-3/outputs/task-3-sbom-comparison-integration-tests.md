## Repository
trustify-backend

## Description
Add comprehensive integration tests for the SBOM comparison endpoint. These tests validate the full request/response cycle against a real PostgreSQL test database, ensuring the diff logic produces correct results for various scenarios including edge cases like empty SBOMs, identical SBOMs, and large package sets.

## Files to Create
- `tests/api/sbom_compare.rs` — Integration test module for the comparison endpoint

## Files to Modify
- `tests/api/mod.rs` — Add `mod sbom_compare;` if a module file exists, or ensure the test is discovered by the test harness

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/sbom.rs` — set up test data by ingesting two SBOMs with known package/advisory differences, then call the endpoint and assert on the response body.
- Use the same test database setup and teardown approach as existing tests in `tests/api/`.
- Use `assert_eq!(resp.status(), StatusCode::OK)` for success cases and `assert_eq!(resp.status(), StatusCode::BAD_REQUEST)` / `StatusCode::NOT_FOUND` for error cases.
- Test scenarios should cover:
  - Two SBOMs where the right has additional packages (tests `added_packages`)
  - Two SBOMs where the left has packages removed in the right (tests `removed_packages`)
  - Two SBOMs with shared packages at different versions (tests `version_changes` with both upgrade and downgrade)
  - Two SBOMs with different advisory associations (tests `new_vulnerabilities` and `resolved_vulnerabilities`)
  - Two SBOMs with packages whose licenses changed (tests `license_changes`)
  - Comparing an SBOM with itself (all diff sections empty)
  - Missing query parameters (400 response)
  - Non-existent SBOM IDs (404 response)

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM integration test patterns for test setup, HTTP client usage, and assertion style

## Acceptance Criteria
- [ ] All integration tests pass against the test database
- [ ] Tests cover all six diff categories (added, removed, version changes, new vulns, resolved vulns, license changes)
- [ ] Tests cover error cases (missing params, non-existent IDs)
- [ ] Tests cover the identity case (comparing an SBOM with itself)
- [ ] Test data setup uses the ingestion pipeline to create realistic test SBOMs

## Test Requirements
- [ ] Test: two SBOMs with 3 added packages — response `added_packages` has length 3 with correct names
- [ ] Test: two SBOMs with 2 removed packages — response `removed_packages` has length 2
- [ ] Test: packages with version changes — `version_changes` entries have correct `direction` values
- [ ] Test: SBOM with new critical advisory — `new_vulnerabilities` includes entry with `severity: "critical"`
- [ ] Test: SBOM with resolved advisory — `resolved_vulnerabilities` includes the previously-present advisory
- [ ] Test: package license changed from MIT to Apache-2.0 — `license_changes` entry reflects both licenses
- [ ] Test: self-comparison returns empty diff sections
- [ ] Test: missing `left` query param returns 400
- [ ] Test: non-existent SBOM ID returns 404

## Verification Commands
- `cargo test -p trustify-tests sbom_compare` — all tests pass

## Dependencies
- Depends on: Task 2 — SBOM comparison service and endpoint
