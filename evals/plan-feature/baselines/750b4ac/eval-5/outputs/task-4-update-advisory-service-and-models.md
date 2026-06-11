# Task 4 — Update advisory service layer and models to use status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and model structs to use the new `status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join overhead on every advisory query, which was contributing ~40ms to the advisory list endpoint p95 latency. All advisory queries that previously joined `advisory_status` must be rewritten to filter and select from the `status` enum column on the `advisory` table directly.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — remove all `advisory_status` table joins from advisory queries (fetch, list, search); replace with direct `status` column access on the `advisory` entity; update status filtering to use `WHERE advisory.status = <enum_value>` instead of join-based filtering
- `modules/fundamental/src/advisory/model/summary.rs` — update `AdvisorySummary` struct to source status from the `AdvisoryStatusEnum` field instead of a joined string; ensure serialization produces the same string representation as before (e.g., "Fixed", "New")
- `modules/fundamental/src/advisory/model/details.rs` — update `AdvisoryDetails` struct similarly to use the enum status field
- `modules/fundamental/src/advisory/model/mod.rs` — update model module re-exports if needed to include the enum type

## Implementation Notes
- The `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs` currently builds queries that join `advisory` to `advisory_status` via `status_id`. Remove these joins entirely — the `status` field is now directly on the `advisory` entity.
- For list/search operations, update the query builder to filter by `advisory::Column::Status` using `AdvisoryStatusEnum` values instead of joining and filtering by `advisory_status::Column::Name`.
- Use the shared query helpers from `common/src/db/query.rs` for filtering and pagination — do not duplicate query building logic.
- The `AdvisorySummary` struct likely has a `status: String` field populated from the join. Keep the field type as `String` in the API response (no user-facing API changes) but derive the value from `AdvisoryStatusEnum.to_string()` or equivalent serialization.
- Follow the existing service pattern in `modules/fundamental/src/advisory/service/advisory.rs` — all handlers return `Result<T, AppError>` with `.context()` wrapping per the project conventions.
- Per docs/constraints.md section 5.4: reuse existing query helpers from `common/src/db/query.rs` rather than duplicating filtering logic.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting; use these for the updated advisory queries
- `modules/fundamental/src/sbom/service/sbom.rs` — reference service implementation showing the query pattern without joins to lookup tables
- `common/src/model/paginated.rs` — `PaginatedResults<T>` wrapper used by list endpoints

## Acceptance Criteria
- [ ] All advisory queries in `AdvisoryService` no longer join `advisory_status` table
- [ ] Advisory list/search queries filter by `advisory::Column::Status` enum value
- [ ] `AdvisorySummary` and `AdvisoryDetails` structs use the enum status field
- [ ] API response shape for status field is unchanged (still a string like "Fixed", "New")
- [ ] Advisory list endpoint p95 latency improves (join eliminated)

## Test Requirements
- [ ] Advisory service fetch returns correct status from enum column
- [ ] Advisory service list with status filter returns correctly filtered results
- [ ] Advisory service search includes status in results without join

## Verification Commands
- `cargo check -p fundamental` — fundamental module compiles
- `cargo test -p fundamental` — fundamental module tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum

[sdlc-workflow] Description digest: sha256-md:20674a25aee6ef72fe65dc5dea48f50bf1b2d3cff0d1d6db54c04dca725e17fc
