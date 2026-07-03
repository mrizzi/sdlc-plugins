## Repository
trustify-backend

## Target Branch
main

## Description
Write integration tests for the remediation REST endpoints. This task creates a comprehensive test suite that validates the `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product` endpoints against a real PostgreSQL test database, following the established integration test patterns in `tests/api/`. The tests verify correct aggregation logic, pagination, edge cases, and response shapes.

Parent Epic: TC-9006: trustify-backend

additional_fields: { "labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}] }

## Files to Create
- `tests/api/remediation.rs` -- integration tests for both remediation endpoints covering valid data, empty data, pagination, and error cases

## Implementation Notes
Follow the integration test pattern established in `tests/api/sbom.rs` and `tests/api/advisory.rs`. Tests should:
- Use the test database setup from the existing test infrastructure
- Seed test data by creating SBOM and advisory records with known severity and remediation status values using the ingestion pipeline
- Assert response status codes using `assert_eq!(resp.status(), StatusCode::OK)` pattern
- Validate response body JSON shape and values by deserializing into the model structs

Test cases to cover:
1. **Summary with mixed data**: seed advisories with different severity levels (Critical, High, Medium, Low) and statuses (Open, In Progress, Resolved), verify counts match expected values
2. **Summary with empty data**: no vulnerabilities ingested, verify all counts are zero
3. **By-product valid response**: seed multiple products with associated SBOMs and vulnerabilities, verify per-product breakdown is correct
4. **By-product pagination**: verify `offset` and `limit` query parameters return correct subsets
5. **By-product empty**: no products with vulnerabilities, verify empty items list with total of 0
6. **Cache headers**: verify summary endpoint includes cache-control headers

Per CONVENTIONS.md: integration tests use real PostgreSQL test database with `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task creates `tests/api/remediation.rs` matching the convention's `.rs` test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` -- established integration test pattern for endpoint testing; follow test setup and assertion style
- `tests/api/advisory.rs` -- advisory test patterns including severity-related test data setup and assertions
- `tests/api/search.rs` -- search endpoint test pattern for reference

## Acceptance Criteria
- [ ] Integration test suite exists at `tests/api/remediation.rs`
- [ ] Tests cover both endpoints: summary and by-product
- [ ] Tests validate correct aggregation logic with known seeded test data
- [ ] Tests cover edge cases: empty data, pagination boundaries
- [ ] Tests verify response JSON shape matches model definitions
- [ ] All tests pass against the test database

## Test Requirements
- [ ] Test: summary endpoint returns correct severity x status counts for seeded data
- [ ] Test: summary endpoint returns zero counts when no vulnerabilities exist
- [ ] Test: by-product endpoint returns correct per-product breakdown with expected counts
- [ ] Test: by-product endpoint respects pagination parameters (offset, limit)
- [ ] Test: by-product endpoint returns empty results when no product data exists
- [ ] Test: summary endpoint includes cache-control headers

## Verification Commands
- `cargo test --test api remediation` -- all integration tests pass

## Dependencies
- Depends on: Task 2 -- Implement remediation REST endpoints
