## Repository
trustify-backend

## Target Branch
main

## Parent Epic
TC-9006: trustify-backend

## Description
Add integration tests for the remediation REST endpoints, covering the summary and by-product aggregation responses, filtering behavior, pagination, and error cases. Tests verify both endpoints against a real PostgreSQL test database following established test patterns in the repository.

## Files to Create
- `tests/api/remediation.rs` — Integration tests for GET /api/v2/remediation/summary and GET /api/v2/remediation/by-product

## Files to Modify
- `tests/Cargo.toml` — Add remediation test module reference if using module-based test organization

## Implementation Notes
Follow the integration test pattern established in `tests/api/` for existing endpoint tests.

- Tests should seed the database with known advisory and SBOM data, then verify aggregation results
- Test the summary endpoint with multiple severity levels and statuses to verify correct grouping
- Test the by-product endpoint with pagination parameters (offset, limit)
- Test filter parameters: severity filter, status filter, product filter individually and in combination
- Test edge cases: empty database returns zero counts, single product scenario
- Verify response body JSON structure matches RemediationSummary and PaginatedResults<ProductRemediation> schemas

Per CONVENTIONS.md §Test Patterns: use assert_eq!(resp.status(), StatusCode::OK) pattern. Applies: task creates tests/api/remediation.rs matching the convention's .rs test file scope.

## Acceptance Criteria
- [ ] Integration tests cover GET /api/v2/remediation/summary with seeded data
- [ ] Integration tests cover GET /api/v2/remediation/by-product with pagination
- [ ] Filter parameter tests verify severity, status, and product filtering
- [ ] Edge case test verifies empty database returns zero counts
- [ ] All tests use `assert_eq!(resp.status(), StatusCode::OK)` pattern
- [ ] All tests pass against a real PostgreSQL test database

## Test Requirements
- [ ] Summary endpoint returns correct aggregated counts for seeded vulnerabilities across severity levels
- [ ] By-product endpoint returns correct per-product breakdown with total, open, resolved counts
- [ ] Pagination test verifies offset/limit behavior on by-product endpoint
- [ ] Filter tests verify each filter parameter independently and in combination

## Dependencies
- Depends on: Task 2 (remediation endpoints must be implemented and routes registered)

## Additional Fields
- priority: Major
- fixVersions: RHTPA 1.5.0
- labels: ai-generated-jira
