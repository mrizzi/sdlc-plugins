## Repository
trustify-backend

## Target Branch
TC-9006

## Description
Add integration tests for both remediation endpoints (`GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`). Tests cover the aggregation logic, edge cases (empty data, single product, multiple products), and error scenarios, following the established integration test pattern in `tests/api/`.

## Files to Create
- `tests/api/remediation.rs` -- integration tests for both remediation endpoints

## Implementation Notes
- Per CONVENTIONS.md $Testing: follow the integration test pattern in `tests/api/advisory.rs` -- tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` assertions.
  Applies: task creates `tests/api/remediation.rs` matching the convention's Rust test file scope.
- Set up test fixtures with known vulnerability data across multiple severities and products to verify aggregation counts.
- Test both endpoints with populated data and with empty datasets.
- Verify response shapes match the model structs (RemediationSummary, ProductRemediation) defined in Tasks 2 and 3.

## Reuse Candidates
- `tests/api/advisory.rs` -- reference implementation for integration test structure, database setup, and assertion patterns
- `tests/api/sbom.rs` -- additional reference for test patterns including fixture setup and response validation

## Acceptance Criteria
- [ ] Integration tests for GET /api/v2/remediation/summary pass
- [ ] Integration tests for GET /api/v2/remediation/by-product pass
- [ ] Tests cover empty data, single product, and multi-product scenarios
- [ ] All tests follow the established `assert_eq!(resp.status(), StatusCode::OK)` pattern

## Test Requirements
- [ ] Test summary endpoint returns correct counts grouped by severity and status
- [ ] Test by-product endpoint returns correct per-product breakdown
- [ ] Test empty dataset returns valid response with zero counts
- [ ] Test error handling for database connection failures

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9006 from main
- Depends on: Task 2 -- Add remediation module with summary aggregation service and endpoint
- Depends on: Task 3 -- Add per-product remediation breakdown endpoint
