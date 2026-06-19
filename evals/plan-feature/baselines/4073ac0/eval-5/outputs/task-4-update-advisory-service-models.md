## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and model structs to use the new `status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join that adds ~40ms to advisory list endpoint p95 latency. All advisory queries (fetch, list, search) must be updated to select `advisory.status` directly and remove `advisory_status` table joins.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — Remove `advisory_status` join from all query methods (fetch, list, search); update status filtering to use `advisory.status` enum column directly; remove any `use` imports for the `advisory_status` entity
- `modules/fundamental/src/advisory/model/summary.rs` — Update `AdvisorySummary` struct to populate `status` field from the advisory entity's enum column instead of from a joined `advisory_status` row
- `modules/fundamental/src/advisory/model/details.rs` — Update `AdvisoryDetails` struct similarly to read status from the enum column
- `modules/fundamental/src/advisory/model/mod.rs` — Update any re-exports or shared model helpers that reference `advisory_status`

## Implementation Notes
Follow the existing query patterns in `modules/fundamental/src/advisory/service/advisory.rs`. The service currently joins `advisory_status` to resolve the status name. After this change, status is read directly from `advisory::Column::Status` which returns an `AdvisoryStatusEnum` value.

For status filtering, replace the join-based filter (e.g., `advisory_status::Column::Name.eq(filter_value)`) with a direct enum filter: `advisory::Column::Status.eq(AdvisoryStatusEnum::from_str(filter_value))`.

The `AdvisorySummary` and `AdvisoryDetails` structs likely have a `status: String` field populated by mapping the joined status row's `name` column. Update the `From` impl (or equivalent constructor) to convert the `AdvisoryStatusEnum` to a string using `.to_string()` or the SeaORM value accessor.

Use the shared query builder helpers in `common/src/db/query.rs` for filtering and pagination — these should not need modification but verify that enum column filtering works through the existing helpers.

## Reuse Candidates
- `common/src/db/query.rs` — Shared query builder helpers for filtering and pagination; verify enum column compatibility
- `modules/fundamental/src/advisory/service/advisory.rs` — Existing query methods to modify in-place
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Existing struct to update field source

## Acceptance Criteria
- [ ] All advisory queries in `AdvisoryService` no longer join the `advisory_status` table
- [ ] Status field in `AdvisorySummary` is populated from `advisory.status` enum column
- [ ] Status field in `AdvisoryDetails` is populated from `advisory.status` enum column
- [ ] Status filtering works using the enum column directly
- [ ] No remaining imports or references to `advisory_status` entity in the advisory module
- [ ] Advisory module compiles successfully

## Test Requirements
- [ ] Advisory list query returns correct status values from enum column
- [ ] Advisory fetch query returns correct status in details
- [ ] Status filtering by enum value (e.g., "Fixed") returns only matching advisories
- [ ] Empty filter returns all advisories with correct statuses

## Verification Commands
- `cargo check -p fundamental` — fundamental module compiles without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
