## Summary
Update advisory service and model layer to use status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service and model layer to use the new `status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join from all advisory queries, simplifying the query logic and reducing the advisory list endpoint p95 latency by approximately 40ms. The `AdvisorySummary` and `AdvisoryDetails` structs must be updated to source the status field from the enum column, and all query builder calls that join `advisory_status` must be removed.

## Files to Modify
- `modules/fundamental/src/advisory/model/summary.rs` -- Update `AdvisorySummary` to read `status` from the enum column instead of the joined table
- `modules/fundamental/src/advisory/model/details.rs` -- Update `AdvisoryDetails` to read `status` from the enum column
- `modules/fundamental/src/advisory/model/mod.rs` -- Update model module if it re-exports or references advisory_status types
- `modules/fundamental/src/advisory/service/advisory.rs` -- Remove all `advisory_status` joins from fetch, list, and search queries; use direct enum column for status filtering

## Implementation Notes
Per CONVENTIONS.md §Error Handling: all service methods return `Result<T, AppError>` with `.context()` wrapping for error propagation. Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's `.rs` scope.

Per CONVENTIONS.md §Module pattern: follow the existing `model/ + service/ + endpoints/` structure for the advisory module. Applies: task modifies `modules/fundamental/src/advisory/model/summary.rs` matching the convention's `.rs` module scope.

Key changes in `advisory.rs` service:
- Remove `.join(advisory_status)` or equivalent SeaORM relation joins from all query methods
- Replace `advisory_status.name` column references with `advisory.status` column
- Update any `Filter` or `Condition` clauses that reference the old `status_id` column
- Use `AdvisoryStatusEnum` for status comparisons in filter logic

Reference `common/src/db/query.rs` for shared query builder helpers (filtering, pagination, sorting) that may need awareness of the schema change.

## Acceptance Criteria
- [ ] All advisory queries use `advisory.status` enum column directly (no joins to `advisory_status`)
- [ ] `AdvisorySummary` and `AdvisoryDetails` correctly populate the status field from the enum column
- [ ] Status filtering works with the enum column (e.g., `WHERE status = 'Fixed'`)
- [ ] No references to `advisory_status` table remain in the service or model layer
- [ ] API response shape is unchanged (status is still returned as a string)

## Test Requirements
- [ ] Advisory list query returns correct status values from enum column
- [ ] Advisory detail query returns correct status value
- [ ] Status filter returns only advisories matching the requested status
- [ ] Service methods compile and pass existing unit tests after refactor

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum

## Additional Fields
- priority: High
- fixVersions: RHTPA 2.0.0
- labels: ai-generated-jira
