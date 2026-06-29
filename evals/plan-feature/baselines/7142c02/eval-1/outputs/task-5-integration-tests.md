## Repository
trustify-backend

## Target Branch
main

## Description
Write comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Tests run against a real PostgreSQL test database following the project's existing integration test patterns, covering successful aggregation, 404 for missing SBOMs, threshold filtering, deduplication of advisories, and response caching headers.

## Files to Create
- `tests/api/sbom_advisory_summary.rs` — Integration test module for the advisory summary endpoint

## Files to Modify
- `tests/Cargo.toml` — Add the new test file to the test suite if not automatically discovered

## Implementation Notes
Follow the integration test pattern in `tests/api/sbom.rs` which tests existing SBOM endpoints. Tests should:

1. Set up test data: create an SBOM, create advisories with varying severity levels (Critical, High, Medium, Low), and link them via `sbom_advisory` records.
2. For the basic success test: call `GET /api/v2/sbom/{id}/advisory-summary` and verify the response JSON contains correct counts for each severity level and the total.
3. For deduplication: link the same advisory to the SBOM multiple times (if possible via the data model) and verify it is counted only once.
4. For 404: call the endpoint with a non-existent SBOM ID and assert `StatusCode::NOT_FOUND`.
5. For threshold filtering: call with `?threshold=high` and verify that `medium` and `low` are zeroed while `critical` and `high` retain their counts.
6. For cache headers: verify the response includes a `Cache-Control` header with `max-age=300`.

Per CONVENTIONS.md §Testing: use the project's integration test pattern with a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task creates `tests/api/sbom_advisory_summary.rs` matching the convention's `.rs` testing scope.

Per CONVENTIONS.md §Error handling: verify that error responses use the `AppError` format.
Applies: task creates `tests/api/sbom_advisory_summary.rs` matching the convention's `.rs` scope.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM endpoint integration test patterns for test setup and assertion style
- `tests/api/advisory.rs` — advisory test patterns for creating test advisory data

## Acceptance Criteria
- [ ] Integration tests exist for the advisory summary endpoint in `tests/api/sbom_advisory_summary.rs`
- [ ] Tests cover: successful aggregation, 404 for missing SBOM, threshold filtering, deduplication, cache headers
- [ ] Tests use the same test infrastructure as existing tests in `tests/api/`
- [ ] All tests pass against a PostgreSQL test database

## Test Requirements
- [ ] Test: GET with valid SBOM ID returns 200 and correct severity counts
- [ ] Test: GET with non-existent SBOM ID returns 404
- [ ] Test: GET with `?threshold=critical` returns only critical count, others zeroed
- [ ] Test: GET with `?threshold=high` returns critical and high counts, medium and low zeroed
- [ ] Test: advisories are deduplicated by advisory ID in the count
- [ ] Test: SBOM with zero advisories returns all counts as 0 with total 0
- [ ] Test: response includes `Cache-Control` header with `max-age=300`

## Verification Commands
- `cargo test --test api -- sbom_advisory_summary` — all advisory summary integration tests pass

## Dependencies
- Depends on: Task 3 — Advisory summary endpoint (endpoint must exist to test)

## Jira Metadata
additional_fields: {"labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}]}

[sdlc-workflow] Description digest: sha256-md:f2f63da6f075401830ae66d6aadef627661cd616f1f4693f890302a605c10d4e
