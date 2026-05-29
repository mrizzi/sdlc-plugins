# Task 4 -- Update advisory service and endpoints to use status enum column

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and HTTP endpoints to query the new `status` enum column directly on the `advisory` table, eliminating all joins to the now-removed `advisory_status` lookup table. Update the advisory model structs (`AdvisorySummary`, `AdvisoryDetails`) to source the status from the enum column. Update the list endpoint's status filtering to use `WHERE status = '<value>'` instead of joining through the lookup table.

## Files to Modify
- `modules/fundamental/src/advisory/model/summary.rs` -- update `AdvisorySummary` struct to source `status` from the enum column instead of a joined `advisory_status` table; update any `From` or conversion impls
- `modules/fundamental/src/advisory/model/details.rs` -- update `AdvisoryDetails` struct similarly to source `status` from the enum column
- `modules/fundamental/src/advisory/model/mod.rs` -- update module-level types or re-exports if they reference `advisory_status`
- `modules/fundamental/src/advisory/service/advisory.rs` -- update `AdvisoryService` query methods (`fetch`, `list`, `search`) to remove the `advisory_status` join and query the `status` column directly; update any status filtering logic
- `modules/fundamental/src/advisory/endpoints/list.rs` -- update list endpoint handler to filter by enum column (`WHERE status = 'Fixed'`) instead of joining
- `modules/fundamental/src/advisory/endpoints/get.rs` -- update get endpoint handler if it references the `advisory_status` join

## Implementation Notes
- Follow the existing query patterns in `AdvisoryService` at `modules/fundamental/src/advisory/service/advisory.rs`. Replace join-based status queries with direct column filters:
  - Before: `advisory.find().join(advisory_status).filter(advisory_status::Column::Name.eq(status_value))`
  - After: `advisory.find().filter(advisory::Column::Status.eq(AdvisoryStatusEnum::Fixed))`
- The `AdvisorySummary` and `AdvisoryDetails` structs likely derive their `status` field from the joined `advisory_status` record. Update the `From` impl (or query select) to read `status` directly from the `advisory` entity's `status` field.
- Reference the query builder helpers in `common/src/db/query.rs` -- if advisory status filtering is implemented there as a shared helper, it must be updated to filter on the enum column.
- The response shape to API consumers remains identical -- `status` is still serialized as a string (e.g., `"Fixed"`). Verify that SeaORM's `DeriveActiveEnum` with `string_value` attributes produces the correct JSON serialization via serde.
- Follow the existing endpoint patterns in `modules/fundamental/src/sbom/endpoints/list.rs` and `modules/fundamental/src/sbom/service/sbom.rs` for reference on how list/get endpoints build queries.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs` -- reference for service query patterns without lookup table joins
- `modules/fundamental/src/sbom/model/summary.rs` -- reference for model struct patterns
- `common/src/db/query.rs` -- shared query builder helpers for filtering and pagination

## Acceptance Criteria
- [ ] All advisory queries use the `status` enum column directly -- no references to `advisory_status` table remain
- [ ] `AdvisorySummary` and `AdvisoryDetails` correctly populate the `status` field from the enum column
- [ ] Advisory list endpoint supports status filtering via the enum column
- [ ] API response shape for advisory endpoints is unchanged (status is still a string)
- [ ] The advisory module compiles without errors

## Test Requirements
- [ ] Advisory list endpoint returns correct results when filtering by status (e.g., `?status=Fixed`)
- [ ] Advisory get endpoint returns the correct status value from the enum column
- [ ] Verify that the JSON response serializes enum values as strings matching the expected format (New, Analyzing, Fixed, Rejected)

## Verification Commands
- `cargo check -p fundamental` -- fundamental module compiles without errors
- `cargo test -p tests --test advisory` -- advisory integration tests pass

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum
