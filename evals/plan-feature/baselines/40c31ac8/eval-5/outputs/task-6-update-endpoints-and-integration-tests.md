## Summary
Update advisory endpoints and integration tests for status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory REST endpoints to work with the new enum-based status column and update all integration tests to validate the new schema. The endpoint handlers in `list.rs` and `get.rs` must handle status filtering using the enum column. The integration tests in `tests/api/advisory.rs` must be updated to verify that advisory CRUD operations and status filtering work correctly with the enum column instead of the lookup table join.

## Files to Modify
- `modules/fundamental/src/advisory/endpoints/list.rs` -- Update status filter parameter handling to use `AdvisoryStatusEnum` values instead of status_id
- `modules/fundamental/src/advisory/endpoints/get.rs` -- Update response construction if it directly references status_id or joins advisory_status
- `modules/fundamental/src/advisory/endpoints/mod.rs` -- Update route registration if filter parameter types changed
- `tests/api/advisory.rs` -- Update integration tests to verify enum-based status filtering, remove any test setup that seeds the advisory_status lookup table

## Implementation Notes
Per CONVENTIONS.md §Test Patterns: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern for response validation. Applies: task modifies `tests/api/advisory.rs` matching the convention's `.rs` test file scope.

Per CONVENTIONS.md §Error Handling: endpoint handlers return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's `.rs` scope.

Key changes:
- In `list.rs`, update the status query parameter to accept string values that map to `AdvisoryStatusEnum` variants
- Ensure the API response shape remains unchanged -- status is still serialized as a string
- In `tests/api/advisory.rs`, remove any test fixtures that insert rows into `advisory_status` table
- Add test cases for each status filter value (New, Analyzing, Fixed, Rejected)
- Verify that invalid status filter values return appropriate error responses

Reference `common/src/model/paginated.rs` for `PaginatedResults<T>` response wrapper used by list endpoints.

## Acceptance Criteria
- [ ] Advisory list endpoint supports status filtering using enum values
- [ ] Advisory get endpoint returns status as a string from the enum column
- [ ] API response shape is unchanged (backward compatible)
- [ ] Invalid status filter values return a 400 Bad Request with descriptive error
- [ ] All integration tests pass against the new schema
- [ ] No references to `advisory_status` table remain in endpoint or test code

## Test Requirements
- [ ] Integration test: list advisories without filter returns all statuses correctly
- [ ] Integration test: filter by status=Fixed returns only fixed advisories
- [ ] Integration test: filter by invalid status returns 400 error
- [ ] Integration test: get advisory by ID returns correct status enum value as string
- [ ] All existing advisory integration tests pass after migration

## Verification Commands
- `cargo test -p tests --test advisory` -- all advisory integration tests pass
- `cargo test` -- full test suite passes

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 4 -- Update advisory service and model layer to use status enum
- Depends on: Task 5 -- Update advisory ingestion pipeline to write enum values directly

## Additional Fields
- priority: High
- fixVersions: RHTPA 2.0.0
- labels: ai-generated-jira
