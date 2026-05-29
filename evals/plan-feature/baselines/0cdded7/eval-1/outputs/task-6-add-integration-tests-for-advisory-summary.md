## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Tests must cover the core success path, error cases, deduplication behavior, caching, and the optional threshold query parameter. Follow the existing integration test patterns in the `tests/api/` directory, hitting a real PostgreSQL test database.

## Files to Create
- `tests/api/advisory_summary.rs` — integration tests for the advisory-summary endpoint

## Files to Modify
- `tests/Cargo.toml` — add test file to test suite if required by the project's test configuration

## Implementation Notes
- Follow the existing integration test patterns established in `tests/api/sbom.rs` and `tests/api/advisory.rs`. These tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` for status assertions.
- Each test should set up the required data (SBOM, advisories, advisory-SBOM links) before calling the endpoint. Inspect existing test files for the test fixture setup pattern — how SBOMs and advisories are created in the test database.
- Test data should include advisories at multiple severity levels to verify correct counting.
- For the deduplication test, link the same advisory to the same SBOM multiple times (if the join table allows) or create a scenario where deduplication logic is exercised.
- For the cache test, verify that the response includes appropriate cache headers (e.g., `Cache-Control: max-age=300`).
- For threshold tests, verify that filtered counts correctly zero out severities below the threshold and that the total reflects only the filtered counts.

## Reuse Candidates
- `tests/api/sbom.rs` — SBOM endpoint integration tests showing test setup, fixture creation, and assertion patterns
- `tests/api/advisory.rs` — advisory endpoint integration tests showing how advisory test data is created
- `tests/api/search.rs` — additional test pattern reference

## Acceptance Criteria
- [ ] Test for valid SBOM with advisories at all severity levels — returns correct counts
- [ ] Test for SBOM with zero advisories — returns all zeros
- [ ] Test for non-existent SBOM ID — returns 404
- [ ] Test for advisory deduplication — same advisory counted only once
- [ ] Test for cache headers — response includes 5-minute cache control
- [ ] Test for threshold filtering — each threshold level correctly filters counts
- [ ] Test for invalid threshold value — returns 400
- [ ] All tests pass against the PostgreSQL test database

## Test Requirements
- [ ] All tests follow existing test patterns in `tests/api/`
- [ ] Tests use real database fixtures, not mocks
- [ ] Test names are descriptive and follow the naming convention of sibling test files

## Verification Commands
- `cargo test --test advisory_summary` — all advisory-summary integration tests pass

## Dependencies
- Depends on: Task 3 — Add advisory-summary endpoint
- Depends on: Task 5 — Add threshold query parameter

[sdlc-workflow] Description digest: sha256:55beef85a1b5f64bbb11dc6d57c958245e681c220cc57679a5cf82dfd5fe16a6
