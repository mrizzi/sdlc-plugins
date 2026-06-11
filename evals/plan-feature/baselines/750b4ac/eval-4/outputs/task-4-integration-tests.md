## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the license compliance report endpoint. These tests validate the full request-response cycle against a real PostgreSQL test database, covering compliant and non-compliant license scenarios, transitive dependency inclusion, edge cases (empty SBOMs, missing licenses), and performance characteristics. This ensures the endpoint meets the acceptance criteria and NFRs defined in the feature.

## Files to Create
- `tests/api/license_report.rs` — integration tests for `GET /api/v2/sbom/{id}/license-report`

## Files to Modify
- `tests/Cargo.toml` — add the new test file to the test suite if required by the project's test configuration

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/sbom.rs` and `tests/api/advisory.rs` for test setup, database seeding, HTTP request construction, and assertion style.
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern established in existing tests.
- Test scenarios to implement:
  1. **Compliant SBOM**: seed an SBOM with packages that all have allowed licenses; verify all groups have `compliant: true`
  2. **Non-compliant license**: seed an SBOM with a package using a denied license; verify the group is flagged with `compliant: false`
  3. **Mixed compliance**: seed an SBOM with both compliant and non-compliant packages; verify correct per-group flagging
  4. **Transitive dependencies**: seed an SBOM with a dependency tree; verify transitive package licenses appear in the report
  5. **Empty SBOM**: seed an SBOM with no packages; verify the endpoint returns 200 with an empty groups array
  6. **Non-existent SBOM**: request a report for a non-existent ID; verify 404 response
  7. **Missing license data**: seed a package with no license mapping; verify it appears in an "Unknown" or unclassified group
- Seed test data using the existing entity models: `sbom`, `package`, `sbom_package`, `package_license` from `entity/src/`.
- Per constraints (Section 5, Code Change Rules): reuse existing test utilities and database seeding patterns rather than creating new infrastructure.
- Per CONVENTIONS.md §Testing: integration tests hit a real PostgreSQL test database. Applies: task creates `tests/api/license_report.rs` matching the convention's test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM integration tests; follow the same test setup, database seeding, and assertion patterns
- `tests/api/advisory.rs` — additional integration test example showing the project's test conventions
- `entity/src/sbom.rs` — SBOM entity for seeding test data
- `entity/src/package.rs` — Package entity for seeding test packages
- `entity/src/package_license.rs` — Package-License mapping entity for seeding license data
- `entity/src/sbom_package.rs` — SBOM-Package join for associating packages with SBOMs in test setup

## Acceptance Criteria
- [ ] All seven test scenarios pass against the test database
- [ ] Tests follow the existing integration test patterns in `tests/api/`
- [ ] Tests verify both response status codes and response body structure
- [ ] Tests cover the transitive dependency requirement

## Test Requirements
- [ ] Integration test: compliant SBOM returns all groups with `compliant: true`
- [ ] Integration test: non-compliant license is correctly flagged
- [ ] Integration test: mixed compliance produces correct per-group flags
- [ ] Integration test: transitive dependencies are included in the report
- [ ] Integration test: empty SBOM returns 200 with empty groups
- [ ] Integration test: non-existent SBOM returns 404
- [ ] Integration test: packages with missing license data are handled gracefully

## Verification Commands
- `cargo test --package trustify-tests license_report` — all license report integration tests pass
- `cargo test --package trustify-tests license_report -- --nocapture` — run with output for debugging

## Dependencies
- Depends on: Task 3 — Add license report endpoint

[sdlc-workflow] Description digest: sha256-md:580ce03b597ffd0201df525262c0cb308f8a5210f0959c9f1ffa68ea3af2bae0
