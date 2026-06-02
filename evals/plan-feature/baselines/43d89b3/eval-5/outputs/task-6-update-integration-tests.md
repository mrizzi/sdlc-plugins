## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to reflect the new schema — all test setup and assertions must use the `status` enum column instead of the `advisory_status` lookup table join. Update test fixtures and helper functions that create advisory records to set the `status` enum value directly. Verify that advisory list filtering by status works correctly with the enum column and that the API response shape is unchanged.

## Files to Modify
- `tests/api/advisory.rs` — update all advisory test functions: replace test data setup that inserts into `advisory_status` table with direct enum value assignment; update assertions to check the `status` field as a string; add test cases for filtering by each enum value

## Implementation Notes
Follow the existing integration test patterns in `tests/api/advisory.rs` and reference the SBOM test patterns in `tests/api/sbom.rs` for the general test structure.

Update test data setup to create advisory records with enum status values:
```rust
let advisory = advisory::ActiveModel {
    status: Set(AdvisoryStatusEnum::New),
    // ... other fields
    ..Default::default()
};
```

Remove any test setup code that creates rows in the `advisory_status` table.

Verify that list endpoint responses still return status as a string value (e.g., `"New"`, `"Fixed"`) — the response shape must be unchanged for API consumers.

Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern consistent with existing tests.

## Reuse Candidates
- `tests/api/sbom.rs` — reference for integration test patterns, test data setup, and assertion style
- `tests/api/advisory.rs` — existing advisory tests to understand current test structure and coverage

## Acceptance Criteria
- [ ] All advisory integration tests pass with the new schema
- [ ] Test data setup uses `AdvisoryStatusEnum` values directly — no `advisory_status` table inserts
- [ ] Tests verify filtering by each status enum value (New, Analyzing, Fixed, Rejected)
- [ ] Tests verify the API response shape is unchanged — status is returned as a string
- [ ] No references to `advisory_status` entity remain in test code

## Test Requirements
- [ ] `cargo test --test api -- advisory` passes with all tests green
- [ ] Coverage includes: list all advisories, filter by each status value, get advisory by ID with correct status
- [ ] Tests verify correct status string representation in JSON response

## Verification Commands
- `cargo test --test api -- advisory` — all advisory integration tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
