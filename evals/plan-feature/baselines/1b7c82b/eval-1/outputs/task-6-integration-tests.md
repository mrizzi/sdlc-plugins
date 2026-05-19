## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the advisory-summary endpoint, covering the full request lifecycle against a real PostgreSQL test database. These tests validate end-to-end behavior including deduplication, threshold filtering, caching headers, and error responses.

## Files to Create
- `tests/api/advisory_summary.rs` -- Integration test module for `GET /api/v2/sbom/{id}/advisory-summary` covering all acceptance criteria from the feature spec

## Files to Modify
- `tests/api/mod.rs` or test harness entry point -- Register the new `advisory_summary` test module (if the test directory uses a mod structure; otherwise Cargo auto-discovers the file)

## Implementation Notes
Follow the integration test patterns established in `tests/api/sbom.rs` and `tests/api/advisory.rs`. These existing test files demonstrate:
- Test database setup and teardown
- Creating test SBOMs and advisories via the ingestion pipeline or direct entity insertion
- Making HTTP requests to the Axum test server
- Asserting on response status codes, headers, and JSON body content using `assert_eq!(resp.status(), StatusCode::OK)` pattern

Test scenarios to implement:
1. **Happy path**: Create an SBOM with advisories at each severity level, call the endpoint, assert correct counts and total.
2. **Deduplication**: Link the same advisory to the SBOM twice (if possible via the join table), verify it is counted only once.
3. **Empty SBOM**: Create an SBOM with no linked advisories, verify response is `{ critical: 0, high: 0, medium: 0, low: 0, total: 0 }`.
4. **Nonexistent SBOM**: Call with a random UUID, assert 404 response.
5. **Threshold filter - critical**: Assert only critical count is nonzero when `?threshold=critical`.
6. **Threshold filter - high**: Assert critical and high counts are nonzero.
7. **Invalid threshold**: Assert 400 response for `?threshold=invalid`.
8. **Cache header**: Assert `Cache-Control` header contains `max-age=300`.

## Reuse Candidates
- `tests/api/sbom.rs` -- Follow test structure, setup patterns, and assertion style
- `tests/api/advisory.rs` -- Follow advisory-specific test data creation patterns
- `modules/ingestor/src/graph/sbom/mod.rs` -- Use SBOM ingestion for test data setup
- `modules/ingestor/src/graph/advisory/mod.rs` -- Use advisory ingestion for test data setup

## Acceptance Criteria
- [ ] All 8 test scenarios listed above are implemented and passing
- [ ] Tests use the same test infrastructure as existing integration tests in `tests/api/`
- [ ] Tests do not depend on external state -- each test creates its own test data
- [ ] All tests pass in CI with `cargo test`

## Test Requirements
- [ ] Happy path: correct severity counts for a known data set
- [ ] Deduplication: duplicate advisory IDs are not double-counted
- [ ] Empty SBOM: all counts are zero
- [ ] 404: nonexistent SBOM returns 404
- [ ] Threshold critical: only critical count returned
- [ ] Threshold high: critical and high counts returned
- [ ] Invalid threshold: returns 400
- [ ] Cache header: response includes `Cache-Control: max-age=300`

## Verification Commands
- `cargo test -p trustify-tests -- advisory_summary` -- all advisory_summary tests pass

## Dependencies
- Depends on: Task 5 -- Threshold filter (all endpoint functionality must be complete before comprehensive integration tests)
