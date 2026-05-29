# Task 4 — Update advisory service and endpoints to use status enum column

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and HTTP endpoints to query the `status` enum column directly on the `advisory` table instead of joining the `advisory_status` lookup table. This eliminates the join overhead on all advisory queries, reducing advisory list endpoint p95 latency by approximately 40ms. The response shape remains identical — status is still returned as a string.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — remove `advisory_status` table join from fetch, list, and search queries; filter and select on `advisory.status` enum column directly
- `modules/fundamental/src/advisory/model/summary.rs` — update `AdvisorySummary` struct to source the status field from the enum column instead of the join result
- `modules/fundamental/src/advisory/model/details.rs` — update `AdvisoryDetails` struct to source the status field from the enum column instead of the join result
- `modules/fundamental/src/advisory/endpoints/list.rs` — update status filter parameter handling to compare against enum values instead of joined table values
- `modules/fundamental/src/advisory/endpoints/get.rs` — update single advisory fetch to use enum column
- `modules/fundamental/src/advisory/model/mod.rs` — update model module if it re-exports or aggregates status-related types

## Implementation Notes
- In `advisory.rs` service, replace all `advisory_status` table joins with direct column access on `advisory.status`. The query pattern changes from:
  ```
  Entity::find().join(advisory_status).filter(advisory_status::Column::Name.eq(value))
  ```
  to:
  ```
  Entity::find().filter(advisory::Column::Status.eq(AdvisoryStatusEnum::Fixed))
  ```
- Follow the existing query builder pattern in `common/src/db/query.rs` for filtering and pagination. The shared query helpers accept column references — pass the new `advisory::Column::Status` column.
- In `summary.rs` and `details.rs`, the status field should serialize to the same string representation as before (e.g., `"Fixed"`, `"New"`) to maintain API response compatibility. SeaORM's `DeriveActiveEnum` handles this via `#[sea_orm(string_value)]` attributes on the enum variants.
- Remove any `use` imports of `advisory_status` entity from all modified files.
- The list endpoint in `list.rs` likely accepts a status query parameter for filtering — update the filter logic to compare against `AdvisoryStatusEnum` values instead of doing a subquery/join.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination, already used by advisory queries
- `modules/fundamental/src/sbom/service/sbom.rs` — reference for SeaORM query patterns (fetch, list) without join tables
- `modules/fundamental/src/advisory/endpoints/mod.rs` — route registration pattern for advisory endpoints

## Acceptance Criteria
- [ ] All advisory queries (fetch, list, search) use `advisory.status` column directly — no joins to `advisory_status` table
- [ ] Advisory list endpoint status filter works with enum values (New, Analyzing, Fixed, Rejected)
- [ ] API response shape is unchanged — status field returns the same string values as before
- [ ] No references to `advisory_status` entity remain in the advisory module
- [ ] `cargo check -p fundamental` compiles without errors

## Test Requirements
- [ ] Verify advisory list endpoint returns correct results when filtering by each status value (New, Analyzing, Fixed, Rejected)
- [ ] Verify advisory detail endpoint returns the correct status string in the response
- [ ] Verify advisory list without status filter returns all advisories with correct status values

## Verification Commands
- `cargo check -p fundamental` — compiles without errors
- `cargo test -p fundamental -- advisory` — advisory-related tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum

[sdlc-workflow] Description digest: sha256:eb6385f0de012157920fbe30ce173cb5ba6e4bfc4e46665b125576ad88b5e751
