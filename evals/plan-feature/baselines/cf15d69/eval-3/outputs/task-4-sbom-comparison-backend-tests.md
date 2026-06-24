## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the SBOM comparison endpoint. These tests verify the full request-response cycle including query parameter validation, diff computation correctness, and error handling for missing SBOMs.

## Files to Create
- `tests/api/sbom_compare.rs` — Integration tests for `GET /api/v2/sbom/compare`

## Files to Modify
- `tests/api/sbom.rs` — Add `mod sbom_compare;` if tests are organized as submodules, or reference the new test file in the test harness configuration

## API Changes
- None (testing only)

## Implementation Notes
Follow the existing integration test pattern in `tests/api/sbom.rs` and `tests/api/advisory.rs`. Tests should hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` pattern.

Test scenarios to implement:

1. **Happy path**: Ingest two SBOMs with known, overlapping package sets. Call `GET /api/v2/sbom/compare?left={id1}&right={id2}`. Verify response contains correct added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, and license_changes.

2. **Empty diff**: Compare an SBOM with itself. Verify all diff arrays are empty.

3. **Missing left SBOM**: Call with a non-existent left ID. Verify 404 response.

4. **Missing right SBOM**: Call with a non-existent right ID. Verify 404 response.

5. **Missing query params**: Call without `left` or `right`. Verify 400 response.

6. **Version change direction**: Ingest two SBOMs where a package has version "1.0.0" in left and "2.0.0" in right. Verify `direction` is "upgrade". Reverse and verify "downgrade".

7. **Vulnerability diff**: Ingest two SBOMs where the right SBOM has a package with an associated critical advisory not present in the left. Verify it appears in `new_vulnerabilities` with correct severity.

Per Key Conventions (Testing): Integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task creates `tests/api/sbom_compare.rs` matching the convention's test directory scope.

## Acceptance Criteria
- [ ] All seven test scenarios pass against the test database
- [ ] Tests cover all six diff categories in the response
- [ ] Error cases (404, 400) are tested
- [ ] Tests are runnable via `cargo test`

## Test Requirements
- [ ] Happy path comparison with known package sets
- [ ] Self-comparison returns empty diff
- [ ] 404 for non-existent SBOM IDs
- [ ] 400 for missing query parameters
- [ ] Version change direction (upgrade/downgrade) verification
- [ ] Vulnerability diff with severity verification

## Verification Commands
```bash
cargo test --test api -- sbom_compare
```

## Dependencies
- Depends on: Task 3 — SBOM comparison endpoint

[sdlc-workflow] Description digest: sha256-md:c7791219e49819367692bb6e9fba0305c2cdf65152ee2776605200f9566d0737
