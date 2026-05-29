# Task 8 — Add integration tests for the SBOM comparison endpoint

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/compare` endpoint. These tests verify the full request-response cycle against a real PostgreSQL test database, covering all diff categories, edge cases, and error handling.

## Files to Create
- `tests/api/sbom_compare.rs` — integration tests for the comparison endpoint

## Files to Modify
- `tests/api/mod.rs` or equivalent test module file — register the new test module (if the test harness uses module registration)

## Implementation Notes
- Follow the integration test pattern in `tests/api/sbom.rs` for test setup, database fixture loading, Axum test server configuration, and assertion style (`assert_eq!(resp.status(), StatusCode::OK)` pattern).
- Test fixtures should create two SBOMs with known differences: some shared packages (with version/license variations), some unique packages, and different advisory associations.
- Test the response JSON structure explicitly to ensure field names match the expected contract.
- Include a performance-oriented test that verifies the endpoint responds within a reasonable time for moderately-sized SBOMs (not a strict p95 benchmark, but a sanity check).

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM endpoint integration tests (test setup patterns, fixture loading, assertion style)
- `tests/api/advisory.rs` — advisory endpoint tests (useful for advisory-related fixture setup)

## Acceptance Criteria
- [ ] Integration test: two SBOMs with added packages (right-only) — verify `added_packages` field is populated correctly
- [ ] Integration test: two SBOMs with removed packages (left-only) — verify `removed_packages` field is populated correctly
- [ ] Integration test: two SBOMs with version changes — verify `version_changes` with correct direction
- [ ] Integration test: two SBOMs with different advisory associations — verify `new_vulnerabilities` and `resolved_vulnerabilities`
- [ ] Integration test: two SBOMs with license changes — verify `license_changes` field
- [ ] Integration test: compare identical SBOMs — verify all diff sections are empty arrays
- [ ] Integration test: missing `left` parameter — verify 400 response
- [ ] Integration test: non-existent SBOM ID — verify 404 response
- [ ] All tests pass with `cargo test`

## Test Requirements
- [ ] Write integration tests covering all acceptance criteria above
- [ ] Tests must use real PostgreSQL test database (following existing test infrastructure patterns)
- [ ] Each test should be independent and not rely on shared mutable state

## Verification Commands
- `cargo test --test api sbom_compare` — expected: all tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Add SBOM comparison REST endpoint

[sdlc-workflow] Description digest: sha256:a08e19c81b5ab129278e41903024a09c083f6f7cb50a4c5eafa500ca5047ff1f
