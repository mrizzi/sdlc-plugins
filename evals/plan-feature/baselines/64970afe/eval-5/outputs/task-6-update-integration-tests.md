## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory endpoint integration tests to work with the new `advisory_status_enum` column instead of the `advisory_status` lookup table. Tests must verify that advisory list and get endpoints return correct status values and that status filtering works with enum values. Test data seeding must insert enum values directly instead of populating the lookup table and referencing via foreign key.

## Files to Modify
- `tests/api/advisory.rs` -- update test data seeding to use enum status values instead of lookup table inserts; update assertions to verify enum-based status filtering and retrieval

## Implementation Notes
- Update test setup/fixture code to seed advisory records with `status` enum values directly, rather than creating `advisory_status` rows and setting `status_id` FKs.
- Remove any test helper functions that create or reference `advisory_status` table rows.
- Verify that status filtering tests cover all four enum values: New, Analyzing, Fixed, Rejected.
- Ensure that test assertions on response JSON still check for status as a string value (e.g., `"status": "Fixed"`), since the API response shape is unchanged.
- Per CONVENTIONS.md §Testing: integration tests hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern.
  Applies: task modifies `tests/api/advisory.rs` matching the convention's integration test file scope.
- Reference `tests/api/sbom.rs` for the established integration test pattern (test setup, HTTP request building, response assertion style).

## Reuse Candidates
- `tests/api/sbom.rs` -- sibling integration test file demonstrating the standard test setup, request building, and assertion patterns used in the project
- `tests/api/advisory.rs` -- existing advisory tests providing the current test structure and fixtures to adapt

## Acceptance Criteria
- [ ] All advisory integration tests pass against the migrated schema
- [ ] Tests verify status filtering for each enum value (New, Analyzing, Fixed, Rejected)
- [ ] Tests verify advisory get endpoint returns correct status string
- [ ] No test code references the `advisory_status` lookup table
- [ ] No regressions in other integration test suites (sbom, search)

## Test Requirements
- [ ] Test advisory list with status filter "Fixed" returns only advisories with status "Fixed"
- [ ] Test advisory list with status filter "New" returns only advisories with status "New"
- [ ] Test advisory list without status filter returns all advisories with correct status values
- [ ] Test advisory get returns the correct status value for a specific advisory
- [ ] Test that advisory creation through the ingestion pipeline produces correct enum status values in subsequent queries

## Verification Commands
- `cargo test --test advisory` -- advisory integration tests pass
- `cargo test` -- all integration tests pass (no regressions in sbom or search tests)

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 4 -- Update advisory service and endpoints to use enum status column
- Depends on: Task 5 -- Update advisory ingestion pipeline to write enum status directly
