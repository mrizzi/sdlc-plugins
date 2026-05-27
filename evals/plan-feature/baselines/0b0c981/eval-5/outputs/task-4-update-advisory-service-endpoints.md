## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer, model structs, and endpoint handlers to use the new `status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join overhead from all advisory queries, reducing the advisory list endpoint p95 latency by approximately 40ms. The response shape remains identical — status is still returned as a string to API consumers.

## Files to Modify
- `modules/fundamental/src/advisory/model/summary.rs` — update `AdvisorySummary` struct to source status from the enum column instead of a joined table field
- `modules/fundamental/src/advisory/model/details.rs` — update `AdvisoryDetails` struct to source status from the enum column instead of a joined table field
- `modules/fundamental/src/advisory/service/advisory.rs` — remove all `advisory_status` table joins from query builders; use `advisory::Column::Status` directly for filtering and selection
- `modules/fundamental/src/advisory/endpoints/list.rs` — update status filter logic to use `WHERE advisory.status = 'Fixed'` pattern instead of join-based filtering
- `modules/fundamental/src/advisory/endpoints/get.rs` — remove any advisory_status join if present in the single-advisory fetch query

## Implementation Notes
- In `advisory.rs` (service), remove all `.join()` calls that reference the `advisory_status` entity. Replace with direct column access on `advisory::Column::Status`.
- For status filtering in `list.rs`, use `advisory::Column::Status.eq(AdvisoryStatusEnum::Fixed)` instead of joining and filtering on the lookup table.
- The `AdvisorySummary` and `AdvisoryDetails` model structs should read status directly from the advisory entity's `status` field. The serialization to string in API responses should happen automatically via SeaORM's enum serialization (the enum variant names match the expected API string values).
- Follow the existing query builder patterns in `common/src/db/query.rs` for filtering and pagination helpers.
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` for how model structs map entity fields.
- No API response shape changes — the status field in the JSON response remains a string with the same values.
- Per constraints §5.1: scope changes to advisory module files only. Per §5.3: follow patterns referenced in Implementation Notes.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination; reuse for status filter implementation
- `modules/fundamental/src/sbom/model/summary.rs` — reference pattern for how model structs map from entity fields
- `modules/fundamental/src/sbom/service/sbom.rs` — reference pattern for service query construction without unnecessary joins

## Acceptance Criteria
- [ ] All advisory queries no longer join the `advisory_status` table
- [ ] `AdvisorySummary` and `AdvisoryDetails` read status from `advisory.status` enum column
- [ ] Advisory list endpoint supports filtering by status using the enum column directly
- [ ] API response shape is unchanged — status field returns the same string values as before
- [ ] Advisory list and get endpoints compile and function correctly (`cargo check -p fundamental`)

## Test Requirements
- [ ] Advisory list endpoint returns correct results when filtering by each status value (New, Analyzing, Fixed, Rejected)
- [ ] Advisory detail endpoint returns the correct status string for an advisory
- [ ] Verify no SQL queries reference the `advisory_status` table

## Verification Commands
- `cargo check -p fundamental` — module compiles cleanly
- `cargo test -p fundamental -- advisory` — advisory-related tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main

[sdlc-workflow] Description digest: sha256:7004fd4c4796b8082574234a67cf3775ac5e5c4ff0886ded52440a50a45b912d
