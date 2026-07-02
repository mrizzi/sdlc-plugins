# Task 7: Update advisory integration tests

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to work with the new enum-based status column. The existing tests in `tests/api/advisory.rs` set up test data using the `advisory_status` lookup table and `status_id` foreign key. These tests must be updated to insert advisory records with the `status` enum column directly. Test assertions that verify status values in API responses should remain unchanged since the response shape is identical.

## Files to Modify
- `tests/api/advisory.rs` -- update test data setup to use `AdvisoryStatusEnum` values instead of inserting into the `advisory_status` lookup table; update any assertions that reference `status_id`

## Implementation Notes
The integration tests hit a real PostgreSQL test database (per project conventions). Test setup code that currently:
1. Inserts rows into `advisory_status` table
2. Creates advisory rows with `status_id` referencing those rows

Must be updated to:
1. Create advisory rows with `status` set to `AdvisoryStatusEnum` variants directly
2. Remove any `advisory_status` table setup/teardown

Follow the existing test patterns in `tests/api/sbom.rs` for test structure and assertions. Use `assert_eq!(resp.status(), StatusCode::OK)` for response status checks (per project convention).

Verify that status filtering tests cover all four enum values: `New`, `Analyzing`, `Fixed`, `Rejected`.

Per CONVENTIONS.md Key Conventions: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task modifies `tests/api/advisory.rs` matching the convention's test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` -- reference for test setup patterns, assertion style, and test database interaction
- `entity/src/advisory_status_enum.rs::AdvisoryStatusEnum` -- enum type for test data setup

## Acceptance Criteria
- [ ] All advisory integration tests pass with the new enum-based schema
- [ ] Test data setup uses `AdvisoryStatusEnum` values directly (no lookup table)
- [ ] No references to `advisory_status` table remain in test code
- [ ] Status filtering tests cover all four enum values
- [ ] Response shape assertions remain unchanged

## Test Requirements
- [ ] `cargo test --test advisory` passes all existing and updated tests
- [ ] Advisory list test verifies correct status strings in response
- [ ] Advisory list with status filter test verifies filtering works with enum values
- [ ] Advisory detail test verifies status field is present and correct

## Verification Commands
- `cargo test --test advisory` -- all advisory integration tests pass
- `cargo test` -- full test suite passes

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 4 -- Update advisory service layer and models
- Depends on: Task 5 -- Update advisory ingestion pipeline
- Depends on: Task 6 -- Update advisory endpoints for enum status

## additional_fields
- **labels**: ai-generated-jira, workflow:feature-branch
- **priority**: High
- **fixVersions**: RHTPA 2.0.0
