# Task 3 -- Backend Comparison Integration Tests

## Repository
trustify-backend

## Description
Add comprehensive integration tests for the SBOM comparison endpoint that exercise the full request-response cycle through a real PostgreSQL test database. Tests should cover normal diff scenarios, empty diffs, error cases, and edge cases like large SBOMs.

## Files to Create
- `tests/api/sbom_compare.rs` -- integration tests for the comparison endpoint

## Files to Modify
- `tests/api/mod.rs` or test runner configuration -- register the new test module (if a mod.rs exists)

## Implementation Notes
- Follow the existing integration test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs`. These tests hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` pattern.
- Set up test data by ingesting two SBOMs with known differences: different package sets, different advisory associations, and different licenses on shared packages.
- Test the full HTTP request-response cycle through Axum, not just the service layer.
- Include a test with two identical SBOMs to verify all diff categories are empty.
- Include a test comparing an SBOM with itself (same ID for left and right) to verify it returns an empty diff.
- Include error case tests: missing parameters, non-existent IDs.

## Reuse Candidates
- `tests/api/sbom.rs` -- existing SBOM integration test patterns including test data setup and assertion conventions
- `tests/api/advisory.rs` -- advisory test patterns for setting up advisory test data
- `common/src/model/paginated.rs::PaginatedResults` -- not directly needed but shows the response deserialization pattern used in other tests

## Acceptance Criteria
- [ ] Integration tests pass against a PostgreSQL test database
- [ ] Tests cover: normal diff with added/removed/changed packages, empty diff, vulnerability diff, license diff
- [ ] Tests cover error cases: missing query parameters (400), non-existent SBOM IDs (404)
- [ ] Tests verify the response JSON structure matches SbomComparisonResult
- [ ] Test for comparing an SBOM with itself returns all-empty diff categories

## Test Requirements
- [ ] Test: two SBOMs with different packages produce correct added_packages and removed_packages
- [ ] Test: two SBOMs with shared package at different versions produce correct version_changes with upgrade/downgrade direction
- [ ] Test: two SBOMs with different advisory associations produce correct new_vulnerabilities and resolved_vulnerabilities
- [ ] Test: two SBOMs with license changes on shared packages produce correct license_changes
- [ ] Test: two identical SBOMs produce empty diff
- [ ] Test: same SBOM ID for left and right produces empty diff
- [ ] Test: missing left or right query parameter returns 400
- [ ] Test: non-existent SBOM ID returns 404

## Dependencies
- Depends on: Task 2 -- Backend Comparison Endpoint
