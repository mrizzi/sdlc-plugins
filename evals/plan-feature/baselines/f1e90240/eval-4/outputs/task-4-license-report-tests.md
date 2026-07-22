# Task 4: Add integration tests for license report endpoint

- **Jira parent**: TC-9004
- **Repository**: trustify-backend
- **Target Branch**: main
- **Priority**: Major
- **Fix Versions**: RHTPA 1.5.0

## Description

Add integration tests for the `GET /api/v2/sbom/{id}/license-report` endpoint. Tests exercise the full stack from HTTP request through service logic to the database, using the existing test PostgreSQL database infrastructure. Cover the happy path, non-existent SBOM, policy violations, and transitive dependency inclusion.

## Files to Modify/Create

| Action | Path |
|---|---|
| Create | `tests/api/license_report.rs` |
| Modify | `tests/api/mod.rs` or test harness root — register the new test module (if applicable) |

## Implementation Notes

- **`tests/api/license_report.rs`**: Follow the integration test pattern from `tests/api/sbom.rs` and `tests/api/advisory.rs`.
  1. Set up test database with seeded SBOM, packages, and `package_license` data.
  2. Include test fixtures with a mix of compliant (e.g., MIT, Apache-2.0) and non-compliant (e.g., GPL-3.0 against a permissive-only policy) licenses.
  3. Include at least one SBOM with transitive dependencies to verify they appear in the report.
  4. Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern for status code assertions.
  5. Deserialize the JSON response body and assert on the structure: correct grouping, correct `compliant` flags, inclusion of transitive dependency packages.

### Test cases:

- **Happy path**: SBOM with multiple packages having different licenses; verify groups are correctly formed and compliance flags match the policy.
- **All compliant**: SBOM where all licenses are on the allow-list; verify all groups have `compliant: true`.
- **Non-compliant flagging**: SBOM with a denied license; verify the group has `compliant: false`.
- **Transitive dependencies**: SBOM with a transitive dependency chain; verify indirect packages appear in the license groups.
- **SBOM not found**: Request with a non-existent SBOM ID; verify HTTP 404 response.
- **Empty SBOM**: SBOM with no packages; verify empty groups array is returned.

## Acceptance Criteria

- All test cases listed above are implemented and pass.
- Tests use a real PostgreSQL test database (not mocks).
- Tests follow the existing `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern.
- Test data includes both compliant and non-compliant licenses for meaningful coverage.

## Test Requirements

- This task is itself a test task. All described test cases must pass in CI.

## Conventions Applied

- **Testing**: Applies: task modifies `tests/api/` matching the convention's integration tests hitting a real PostgreSQL test database scope.
