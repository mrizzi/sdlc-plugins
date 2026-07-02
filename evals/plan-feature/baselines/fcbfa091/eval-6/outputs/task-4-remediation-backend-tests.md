## Repository
trustify-backend

## Target Branch
main

## Parent Epic
TC-9006: trustify-backend

## Description
Add integration tests for the remediation API endpoints. Tests verify that `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product` return correctly structured responses with accurate aggregation data. Tests follow the existing integration test pattern using a real PostgreSQL test database.

## Files to Create
- `tests/api/remediation.rs` — Integration tests for both remediation endpoints

## Files to Modify
- `tests/Cargo.toml` — Add `trustify-remediation` as a dev-dependency (if needed for test fixtures)

## Implementation Notes
Follow the integration test pattern from `tests/api/advisory.rs` and `tests/api/sbom.rs`. Tests should:

1. Set up test data by ingesting sample SBOMs with known vulnerability/advisory associations
2. Call the remediation endpoints
3. Assert response status and body structure

Per CONVENTIONS.md: integration tests use `assert_eq!(resp.status(), StatusCode::OK)` pattern against a real PostgreSQL test database.
Applies: task creates `tests/api/remediation.rs` matching the convention's `.rs` test file scope.

Test cases for summary endpoint:
- With seeded data: verify severity breakdown counts match expected values
- With empty database: verify zero counts are returned (not errors)

Test cases for by-product endpoint:
- With seeded data for multiple products: verify each product has correct counts
- Pagination: verify limit/offset produce correct page slices
- Large dataset: seed 100+ vulnerabilities to verify performance does not degrade

## Reuse Candidates
- `tests/api/sbom.rs` — Integration test patterns for endpoint testing, test database setup
- `tests/api/advisory.rs` — Integration test patterns including assertion helpers
- `modules/ingestor/src/service/mod.rs::IngestorService` — Use to seed test SBOMs and advisories for the integration tests

## Acceptance Criteria
- [ ] Integration tests for `GET /api/v2/remediation/summary` pass with seeded test data
- [ ] Integration tests for `GET /api/v2/remediation/by-product` pass with seeded test data
- [ ] Empty-database test case passes without errors
- [ ] Pagination test case verifies correct offset/limit behavior
- [ ] All tests pass in CI with `cargo test`

## Test Requirements
- [ ] Test: summary endpoint returns correct severity-by-status counts for known seed data
- [ ] Test: summary endpoint returns zero counts for empty database
- [ ] Test: by-product endpoint returns correct per-product counts
- [ ] Test: by-product endpoint paginates correctly with limit=2 on 5 products
- [ ] Test: both endpoints return 200 status codes

## Verification Commands
- `cargo test -p trustify-tests --test remediation` — All remediation integration tests pass

## Dependencies
- Depends on: Task 3 — Remediation endpoints

## additional_fields
- labels: ["ai-generated-jira"]
- priority: Major
- fixVersions: ["RHTPA 1.5.0"]
