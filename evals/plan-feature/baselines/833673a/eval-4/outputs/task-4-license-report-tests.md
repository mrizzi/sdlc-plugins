## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the license compliance report endpoint, covering the full request/response cycle against a real PostgreSQL test database. Tests verify correct grouping, compliance flagging, transitive dependency handling, edge cases (empty SBOMs, unknown licenses), and performance characteristics.

## Files to Create
- `tests/api/license_report.rs` — Integration tests for GET /api/v2/sbom/{id}/license-report

## Files to Modify
- `tests/Cargo.toml` — Add any test dependencies if needed for the license report tests

## Implementation Notes
Follow the integration test pattern established in `tests/api/sbom.rs` and `tests/api/advisory.rs`:
- Tests hit a real PostgreSQL test database
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern for status checks
- Set up test data by ingesting an SBOM with known packages and licenses before running report tests

Test scenarios to cover:
1. **Happy path**: SBOM with multiple packages across different licenses — verify grouping and compliance flags
2. **All compliant**: SBOM where every package has an allowed license — all groups show `compliant: true`
3. **Non-compliant detected**: SBOM with at least one denied license — the relevant group shows `compliant: false`
4. **Transitive dependencies**: SBOM with a dependency tree — transitive packages appear with `transitive: true`
5. **Unknown licenses**: Packages with licenses not in the policy — grouped under "Unknown", compliance follows `default_compliance` setting
6. **Empty SBOM**: SBOM with no packages — returns empty groups array
7. **Non-existent SBOM**: Request with invalid ID — returns 404
8. **Performance**: SBOM with a large number of packages (if feasible in test context) — verify response time is within acceptable range

Use a test-specific `license-policy.json` configuration to ensure deterministic compliance results.

## Reuse Candidates
- `tests/api/sbom.rs` — follow this file's test setup pattern for database initialization and HTTP client configuration
- `tests/api/advisory.rs` — follow this file's assertion patterns for response body validation

## Acceptance Criteria
- [ ] All integration tests pass against the PostgreSQL test database
- [ ] Tests cover happy path, non-compliant detection, transitive dependencies, unknown licenses, empty SBOM, and 404 scenarios
- [ ] Tests are deterministic — use fixed test data and a test-specific license policy
- [ ] Test file follows the naming and structure conventions of existing tests in `tests/api/`

## Test Requirements
- [ ] Integration test: happy path with multiple license groups returns correct grouping
- [ ] Integration test: non-compliant license is flagged with `compliant: false`
- [ ] Integration test: transitive dependencies included with `transitive: true`
- [ ] Integration test: unknown licenses grouped correctly based on `default_compliance`
- [ ] Integration test: empty SBOM returns empty groups
- [ ] Integration test: non-existent SBOM returns 404

## Dependencies
- Depends on: Task 3 — License report endpoint

[sdlc-workflow] Description digest: sha256-md:65c0089b98a9389ea676e83bacefb82766b23ca3b250a9a891eba11173991803
