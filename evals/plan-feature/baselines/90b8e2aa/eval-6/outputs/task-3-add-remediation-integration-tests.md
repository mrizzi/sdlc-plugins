## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the remediation API endpoints covering both `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`. Tests verify correct aggregation logic, response shapes, filtering behavior, and edge cases with empty or large datasets.

## Files to Create
- `tests/api/remediation.rs` — integration tests for remediation endpoints: summary aggregation correctness, by-product breakdown, empty dataset handling, pagination of by-product results, and response time validation

## Files to Modify
- `tests/Cargo.toml` — add remediation module dependency if needed for test compilation

## Implementation Notes
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database. Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern established in existing tests. See `tests/api/advisory.rs` for the testing pattern.
  Applies: task creates `tests/api/remediation.rs` matching the convention's integration test file scope.
- Set up test fixtures by ingesting sample SBOMs and advisories with known severity and status values, then verify the aggregation endpoints return expected counts.
- Test the p95 < 500ms response time requirement with a dataset of at least 1,000 vulnerabilities to validate performance under load.
- Test pagination parameters on the by-product endpoint.

## Reuse Candidates
- `tests/api/advisory.rs` — advisory endpoint integration tests; reference for test setup, fixture ingestion, and assertion patterns
- `tests/api/sbom.rs` — SBOM endpoint integration tests; reference for how to set up SBOM test data that the remediation aggregation depends on

## Acceptance Criteria
- [ ] Integration tests for `GET /api/v2/remediation/summary` validate correct severity-by-status grouping
- [ ] Integration tests for `GET /api/v2/remediation/by-product` validate correct per-product breakdown
- [ ] Tests cover empty dataset scenario (no advisories/SBOMs ingested)
- [ ] Tests cover multi-product scenario with distinct remediation statuses
- [ ] All tests pass against a real PostgreSQL test database

## Test Requirements
- [ ] Test summary endpoint returns correct counts when advisories span multiple severities and statuses
- [ ] Test by-product endpoint returns correct totals matching the sum of open + in_progress + resolved
- [ ] Test empty state returns valid JSON with zero counts
- [ ] Test pagination on by-product endpoint (offset and limit parameters)

## Verification Commands
- `cargo test --test api -- remediation` — all remediation integration tests pass

## Dependencies
- Depends on: Task 2 — Add remediation API endpoints
