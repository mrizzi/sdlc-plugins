# Task 4 -- Update advisory service and model layers

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service and model layers to use the new `status` enum column directly instead of joining the `advisory_status` lookup table. All advisory queries in the service layer must remove the `advisory_status` join and read/filter status from the enum column. The model structs (`AdvisorySummary`, `AdvisoryDetails`) must be updated to populate their status field from the enum column.

## Files to Modify
- `modules/fundamental/src/advisory/model/summary.rs` -- Update `AdvisorySummary` struct to derive status from the `AdvisoryStatusEnum` column instead of a joined table field
- `modules/fundamental/src/advisory/model/details.rs` -- Update `AdvisoryDetails` struct to derive status from the `AdvisoryStatusEnum` column instead of a joined table field
- `modules/fundamental/src/advisory/model/mod.rs` -- Remove any imports or re-exports related to `advisory_status` entity
- `modules/fundamental/src/advisory/service/advisory.rs` -- Remove all `advisory_status` table joins from advisory queries; update status filtering to use `advisory::Column::Status` with enum comparison

## Implementation Notes
- In `modules/fundamental/src/advisory/service/advisory.rs`, the `AdvisoryService` methods (`fetch`, `list`, `search`) currently join `advisory_status` to resolve the status string. Remove these joins entirely. For example, replace:
  ```rust
  advisory::Entity::find()
      .join(JoinType::InnerJoin, advisory::Relation::AdvisoryStatus.def())
      .column(advisory_status::Column::Name)
  ```
  with:
  ```rust
  advisory::Entity::find()
      .column(advisory::Column::Status)
  ```
- For status filtering in the list/search methods, replace the join-based filter with a direct enum column filter:
  ```rust
  .filter(advisory::Column::Status.eq(AdvisoryStatusEnum::Fixed))
  ```
- In `modules/fundamental/src/advisory/model/summary.rs`, update `AdvisorySummary`'s `From` or construction logic to read `status` directly from the `advisory::Model` struct's `status` field (which is now `AdvisoryStatusEnum`). Convert to string for the API response using `.to_string()` or a match expression.
- In `modules/fundamental/src/advisory/model/details.rs`, apply the same pattern as for `AdvisorySummary`.
- In `modules/fundamental/src/advisory/model/mod.rs`, remove any `use entity::advisory_status` imports.
- Use the query helper patterns from `common/src/db/query.rs` for any filter/sort changes on the status column.
- All handlers return `Result<T, AppError>` with `.context()` wrapping -- maintain this pattern.

## Acceptance Criteria
- [ ] `AdvisoryService::list` no longer joins `advisory_status` table
- [ ] `AdvisoryService::fetch` no longer joins `advisory_status` table
- [ ] Status filtering uses `advisory::Column::Status` enum comparison
- [ ] `AdvisorySummary` populates status from enum column
- [ ] `AdvisoryDetails` populates status from enum column
- [ ] No remaining references to `advisory_status` entity in the advisory module
- [ ] `cargo build -p fundamental` compiles without errors

## Test Requirements
- [ ] Unit tests for `AdvisorySummary` construction verify correct status string output for each enum variant
- [ ] Unit tests for status filter queries verify correct SQL generation (no join, enum column filter)
- [ ] Compile check passes for the fundamental module and all downstream dependents

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum
