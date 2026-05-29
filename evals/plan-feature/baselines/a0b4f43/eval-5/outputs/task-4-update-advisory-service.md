## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and model structs to use the new `status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join overhead on every advisory query and simplifies the query logic. Update `AdvisorySummary` and `AdvisoryDetails` structs to carry the enum status value, and update `AdvisoryService` methods (fetch, list, search) to query `advisory.status` directly.

## Files to Modify
- `modules/fundamental/src/advisory/model/summary.rs` — change the `status` field from a joined string/ID to `AdvisoryStatusEnum` from the entity crate; update any `From` or conversion impl that previously extracted status from a join result
- `modules/fundamental/src/advisory/model/details.rs` — same change for `AdvisoryDetails`; update conversion logic to read status directly from the advisory row
- `modules/fundamental/src/advisory/model/mod.rs` — update re-exports if needed to include the enum type
- `modules/fundamental/src/advisory/service/advisory.rs` — remove all `advisory_status` table joins from query construction; update `fetch`, `list`, and `search` methods to select `advisory.status` directly; update status filtering to use `WHERE status = <enum_value>` instead of joining
- `modules/fundamental/src/advisory/service/mod.rs` — update imports if the service module re-exports types

## Implementation Notes
- In `AdvisoryService` (`service/advisory.rs`), locate all query builder calls that join `advisory_status` (e.g., `.join()` or `.find_also_related(advisory_status::Entity)`). Remove these joins and replace status selection with direct column access on `advisory::Column::Status`.
- For status filtering, replace the join-based filter (e.g., `advisory_status::Column::Name.eq(filter_value)`) with `advisory::Column::Status.eq(AdvisoryStatusEnum::from_str(filter_value))`.
- In model structs, the status field should be typed as `AdvisoryStatusEnum` internally and serialized as a string in API responses (e.g., via `#[serde(rename_all = "PascalCase")]` or a custom serializer) to maintain backward compatibility with the existing API response shape.
- Follow the query patterns in `common/src/db/query.rs` for filtering and pagination — ensure the status filter integrates with the shared query builder helpers.
- Use `PaginatedResults<AdvisorySummary>` from `common/src/model/paginated.rs` for list endpoint responses — this pattern should already be in place.
- Per `docs/constraints.md` §5.4: do not duplicate existing query builder logic — reuse helpers from `common/src/db/query.rs`.
- Per `docs/constraints.md` §5.2: inspect existing service code before modifying.
- Per `docs/constraints.md` §2 (Commit Rules): commit message must follow Conventional Commits format and reference TC-9005.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper used by all list endpoints
- `modules/fundamental/src/sbom/service/sbom.rs` — reference for how `SbomService` constructs queries without lookup table joins (analogous pattern)

## Acceptance Criteria
- [ ] `AdvisoryService::list` no longer joins `advisory_status` table
- [ ] `AdvisoryService::fetch` no longer joins `advisory_status` table
- [ ] Status filtering uses `advisory::Column::Status` directly
- [ ] `AdvisorySummary.status` is typed as `AdvisoryStatusEnum`
- [ ] `AdvisoryDetails.status` is typed as `AdvisoryStatusEnum`
- [ ] API response JSON shape for status field remains unchanged (string value)
- [ ] The fundamental module compiles without errors

## Test Requirements
- [ ] Verify the fundamental module compiles: `cargo check -p fundamental`
- [ ] Verify that no references to `advisory_status::Entity` or `advisory_status::Column` remain in the advisory service or model files

## Verification Commands
- `cargo check -p fundamental` — compiles without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main