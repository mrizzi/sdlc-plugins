# Task 3 — Backend integration tests for comparison endpoint

## Repository
trustify-backend

## Description
Add comprehensive integration tests for the SBOM comparison endpoint to verify end-to-end behavior against a real PostgreSQL test database. Tests cover the happy path (valid comparison with various diff types), error cases (missing parameters, non-existent SBOMs), and performance characteristics for large SBOMs.

## Files to Modify
- `tests/api/sbom.rs` — add comparison-specific integration tests to the existing SBOM test suite

## Implementation Notes
- Follow the existing test patterns in `tests/api/sbom.rs` — see existing SBOM endpoint integration tests for the setup, request, and assertion pattern.
- Tests should use `assert_eq!(resp.status(), StatusCode::OK)` pattern as established in the codebase.
- Test data setup: create two SBOMs with known packages and advisories, then compare them. Include:
  - Packages present only in the left SBOM (will appear as "removed")
  - Packages present only in the right SBOM (will appear as "added")
  - Packages present in both with different versions (will appear as "version_changes")
  - Advisories affecting only the right SBOM (will appear as "new_vulnerabilities")
  - Advisories affecting only the left SBOM (will appear as "resolved_vulnerabilities")
  - Packages with different licenses between the two SBOMs (will appear as "license_changes")
- Verify the response JSON structure matches `SbomComparisonResult` with correct counts and field values.
- Test version change direction: include at least one upgrade and one downgrade case.
- Test critical vulnerability highlighting: verify that `severity` field is correctly populated for vulnerability diffs.

## Reuse Candidates
- `tests/api/sbom.rs` — existing integration test file with test setup patterns, HTTP client configuration, and assertion helpers
- `tests/api/advisory.rs` — reference for advisory-related test data setup

## Acceptance Criteria
- [ ] Integration tests cover valid comparison with all six diff categories populated
- [ ] Integration tests verify correct counts for each diff category
- [ ] Integration tests verify version change direction (upgrade vs downgrade)
- [ ] Integration tests cover 400 response for missing query parameters
- [ ] Integration tests cover 404 response for non-existent SBOM IDs
- [ ] All tests pass against the PostgreSQL test database

## Test Requirements
- [ ] Integration test: compare two SBOMs with known differences, verify all six diff sections have correct entries
- [ ] Integration test: compare two identical SBOMs, verify all diff sections are empty arrays
- [ ] Integration test: compare with missing `left` parameter returns 400
- [ ] Integration test: compare with missing `right` parameter returns 400
- [ ] Integration test: compare with non-existent left SBOM ID returns 404
- [ ] Integration test: compare with non-existent right SBOM ID returns 404
- [ ] Integration test: verify `direction` field is "upgrade" when right version > left version
- [ ] Integration test: verify `direction` field is "downgrade" when right version < left version

## Verification Commands
- `cargo test --test api sbom` — all SBOM integration tests pass (including new comparison tests)

## Dependencies
- Depends on: Task 2 — Backend comparison endpoint and route registration
