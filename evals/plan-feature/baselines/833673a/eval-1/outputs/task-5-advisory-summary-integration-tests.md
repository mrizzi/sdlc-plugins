## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the advisory severity aggregation endpoint. These tests verify the full request-response cycle against a real PostgreSQL test database, covering the happy path, error cases, deduplication logic, threshold filtering, and cache header behavior.

## Files to Modify
- `tests/api/sbom.rs` — add integration tests for `GET /api/v2/sbom/{id}/advisory-summary`

## Implementation Notes
- Follow the existing integration test patterns in `tests/api/sbom.rs` (SBOM endpoint tests) and `tests/api/advisory.rs` (advisory endpoint tests) for test setup, database seeding, HTTP client usage, and assertion style.
- Per Key Conventions §Testing: integration tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task modifies `tests/api/sbom.rs` matching the convention's integration test file scope.
- Test setup should: create an SBOM, create multiple advisories with varying severities, link them via the `sbom_advisory` join table. Use the existing test helper infrastructure for database seeding found in the test files.
- Test cases to implement:
  1. **Happy path**: SBOM with advisories at all severity levels returns correct counts and total
  2. **Empty advisories**: SBOM with no linked advisories returns all zeros
  3. **404 for unknown SBOM**: Request with non-existent SBOM ID returns HTTP 404
  4. **Deduplication**: Same advisory linked to SBOM multiple times is counted only once
  5. **Threshold filter — critical**: `?threshold=critical` returns only critical count, others zeroed
  6. **Threshold filter — high**: `?threshold=high` returns critical and high counts, medium and low zeroed
  7. **Cache header**: Response includes `Cache-Control: max-age=300`
- Each test should make a `GET` request to `/api/v2/sbom/{id}/advisory-summary` and assert on both the HTTP status code and the JSON response body fields.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM integration tests; reference for test setup, database seeding, and assertion patterns
- `tests/api/advisory.rs` — advisory integration tests; reference for creating advisory test data and making advisory-related assertions

## Acceptance Criteria
- [ ] All seven test cases listed above are implemented and pass
- [ ] Tests use real PostgreSQL test database per project conventions
- [ ] Tests follow existing assertion patterns (`assert_eq!` on status codes and JSON fields)
- [ ] Tests are added to the existing `tests/api/sbom.rs` file, not a separate file

## Test Requirements
- [ ] Happy path test: SBOM with 2 critical, 3 high, 1 medium, 0 low advisories returns `{ critical: 2, high: 3, medium: 1, low: 0, total: 6 }`
- [ ] Empty advisories test: SBOM with no advisories returns `{ critical: 0, high: 0, medium: 0, low: 0, total: 0 }`
- [ ] 404 test: random UUID returns HTTP 404
- [ ] Deduplication test: advisory linked twice to same SBOM is counted once
- [ ] Threshold critical test: `?threshold=critical` with mixed advisories returns only critical count
- [ ] Threshold high test: `?threshold=high` returns critical and high counts only
- [ ] Cache header test: response contains `Cache-Control` header with `max-age=300`

## Dependencies
- Depends on: Task 3 — Add advisory-summary endpoint with caching

[sdlc-workflow] Description digest: sha256-md:1f746dec1513a9a89da732f92b27e59034bd7719d67981d6c878dd678cdd9d0e
