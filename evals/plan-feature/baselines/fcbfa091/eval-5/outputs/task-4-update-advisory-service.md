# Task 4: Update advisory service layer and models

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and model structs to use the new `status` enum column directly instead of joining the `advisory_status` lookup table. All advisory queries in `AdvisoryService` (fetch, list, search) currently join `advisory_status` to resolve the status string; these joins must be removed and replaced with direct reads from the `status` enum column. The `AdvisorySummary` and `AdvisoryDetails` model structs must be updated to source the status field from the enum column.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` -- remove `advisory_status` table joins from all query methods (fetch, list, search); read `status` directly from the `advisory` entity column
- `modules/fundamental/src/advisory/model/summary.rs` -- update `AdvisorySummary` to populate status from the enum column instead of the joined table
- `modules/fundamental/src/advisory/model/details.rs` -- update `AdvisoryDetails` to populate status from the enum column instead of the joined table
- `modules/fundamental/src/advisory/model/mod.rs` -- update any shared model imports or type aliases if they reference the old status entity

## Implementation Notes
In `modules/fundamental/src/advisory/service/advisory.rs`, the list and fetch methods likely contain `.join()` or `.find_also_related()` calls that bring in the `advisory_status` entity. Remove these joins and instead access `advisory::Column::Status` directly, which now returns an `AdvisoryStatusEnum` value.

For model mapping, the status field in `AdvisorySummary` and `AdvisoryDetails` should convert the enum to a string using `.to_string()` or similar serialization to maintain the same API response shape.

Use the existing query helper patterns from `common/src/db/query.rs` for any status-based filtering. Status filter parameters should compare against `advisory::Column::Status` using the enum value directly rather than joining a lookup table.

Follow the error handling pattern: all service methods return `Result<T, AppError>` with `.context()` wrapping, consistent with `modules/fundamental/src/sbom/service/sbom.rs`.

Per CONVENTIONS.md Key Conventions: handlers return `Result<T, AppError>` with `.context()` wrapping.
Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's `.rs` service file scope.

Per CONVENTIONS.md Key Conventions: use shared query builder helpers for filtering, pagination, sorting from `common/src/db/query.rs`.
Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `common/src/db/query.rs::QueryBuilder` -- shared filtering and pagination helpers; reuse for status-based filtering instead of writing custom filter logic
- `common/src/model/paginated.rs::PaginatedResults` -- list endpoints already return this wrapper; ensure it is preserved

## Acceptance Criteria
- [ ] All `advisory_status` table joins are removed from `AdvisoryService` methods
- [ ] Status is read directly from the `advisory.status` enum column
- [ ] `AdvisorySummary` and `AdvisoryDetails` populate status from the enum column
- [ ] Status filtering works using the enum column (no join required)
- [ ] API response shape remains unchanged (status is still a string)
- [ ] All methods return `Result<T, AppError>` with proper error context

## Test Requirements
- [ ] Advisory list query returns correct status strings without joining the lookup table
- [ ] Advisory fetch by ID returns correct status
- [ ] Status filtering (e.g., filter by "Fixed") works with the enum column
- [ ] `cargo build -p fundamental` compiles successfully

## Verification Commands
- `cargo build -p fundamental` -- module compiles without errors
- `cargo test -p fundamental` -- module tests pass

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum

## additional_fields
- **labels**: ai-generated-jira, workflow:feature-branch
- **priority**: High
- **fixVersions**: RHTPA 2.0.0
