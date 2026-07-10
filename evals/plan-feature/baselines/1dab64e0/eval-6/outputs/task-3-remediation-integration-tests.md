**Summary:** Add remediation endpoint integration tests
**Issue Type:** Task
**Parent Epic:** TC-9006: trustify-backend

## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the remediation API endpoints (`GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`) following the established integration test patterns in `tests/api/`. These tests validate end-to-end behavior against a real PostgreSQL test database.

## Files to Create
- `tests/api/remediation.rs` — Integration tests for both remediation endpoints

## Implementation Notes
Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task creates `tests/api/remediation.rs` matching the convention's `.rs` test file scope.

Follow the integration test pattern established in `tests/api/sbom.rs` and `tests/api/advisory.rs`:
- Set up test data by inserting SBOMs with correlated advisories at various severities and statuses
- Call the endpoints via the test HTTP client
- Assert response status codes and response body shapes
- Test edge cases: empty database, single product, multiple products

Test scenarios to implement:
1. Summary endpoint with mixed severity/status data returns correct aggregation
2. Summary endpoint with empty database returns valid response with all-zero counts
3. By-product endpoint with multiple products returns correct per-product breakdowns
4. By-product endpoint pagination: verify offset=0&limit=5 and offset=5&limit=5 return correct subsets
5. By-product endpoint with a single product returns one-element result
6. Verify all responses have content-type application/json

## Reuse Candidates
- `tests/api/sbom.rs` — integration test structure and assertion patterns for endpoint testing
- `tests/api/advisory.rs` — integration test patterns including severity-related test data setup and assertions

## Acceptance Criteria
- [ ] Integration tests pass against a real PostgreSQL test database
- [ ] Summary endpoint test verifies correct aggregation of severity x status counts
- [ ] By-product endpoint test verifies correct per-product breakdown with accurate totals
- [ ] Pagination test verifies correct offset/limit behavior for the by-product endpoint
- [ ] Empty database edge case returns a valid JSON response with zero counts

## Test Requirements
- [ ] Test: GET /api/v2/remediation/summary returns expected severity x status aggregation for seeded test data
- [ ] Test: GET /api/v2/remediation/by-product returns paginated results with correct per-product counts
- [ ] Test: empty database returns valid JSON with zero counts (not an error)
- [ ] Test: by-product pagination with offset and limit returns correct subsets of results

## Dependencies
- Depends on: Task 2 — Add remediation REST API endpoints
