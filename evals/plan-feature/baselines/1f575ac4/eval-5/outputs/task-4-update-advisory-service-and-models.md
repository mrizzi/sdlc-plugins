# Task 4 — Update advisory service layer and models to use enum status

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory model structs (`AdvisorySummary`, `AdvisoryDetails`) and the `AdvisoryService` to use the new `status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join overhead on every advisory query and simplifies the data access layer. The advisory list endpoint p95 latency should decrease by approximately 40ms as a result of removing the join.

## Files to Modify
- `modules/fundamental/src/advisory/model/summary.rs` — update `AdvisorySummary` struct to include a `status` field typed as the enum (or its string representation) instead of deriving status from a joined table
- `modules/fundamental/src/advisory/model/details.rs` — update `AdvisoryDetails` struct similarly to use the enum status directly
- `modules/fundamental/src/advisory/model/mod.rs` — update any model-level type re-exports or conversion logic related to advisory status
- `modules/fundamental/src/advisory/service/advisory.rs` — remove all `.join()` or `.find_also_related()` calls to `advisory_status` entity; update query builders to filter on `advisory::Column::Status` directly using enum values; update the mapping from query results to model structs

## Implementation Notes
- In `AdvisoryService`, replace join-based queries like:
  ```rust
  Advisory::find()
      .find_also_related(AdvisoryStatus)
      .filter(advisory_status::Column::Name.eq("Fixed"))
  ```
  with direct enum filtering:
  ```rust
  Advisory::find()
      .filter(advisory::Column::Status.eq(AdvisoryStatusEnum::Fixed))
  ```
- The `AdvisorySummary` and `AdvisoryDetails` structs likely derive status from the joined `advisory_status` model. Replace this with a direct field from `advisory::Model::status`.
- Check `common/src/db/query.rs` for shared query builder helpers — the filtering and pagination utilities should work with enum columns without modification, but verify the filter builder supports enum type matching.
- Look at how `modules/fundamental/src/sbom/service/sbom.rs` structures its queries for a reference pattern of service methods in this codebase (fetch, list, search).
- The response shape to API consumers must remain identical — status should still be serialized as a string in JSON responses. Verify that Serde serialization of the enum produces the same string values as the old lookup table rows.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers (filtering, pagination, sorting) already used across services; verify enum column compatibility
- `modules/fundamental/src/sbom/service/sbom.rs` — reference implementation for service method patterns (fetch, list)
- `modules/fundamental/src/advisory/model/summary.rs` — existing `AdvisorySummary` struct to understand the current status field derivation

## Acceptance Criteria
- [ ] `AdvisorySummary` includes status as a direct field (not from a join)
- [ ] `AdvisoryDetails` includes status as a direct field (not from a join)
- [ ] `AdvisoryService::list` no longer joins `advisory_status` — queries use `advisory::Column::Status` directly
- [ ] `AdvisoryService::fetch` no longer joins `advisory_status`
- [ ] Status filtering works with enum values (e.g., filtering by "Fixed" returns only fixed advisories)
- [ ] JSON response shape is unchanged — status is still serialized as a string matching the old values
- [ ] No references to `advisory_status` entity remain in the advisory module

## Test Requirements
- [ ] Unit test: verify `AdvisorySummary` and `AdvisoryDetails` serialize status to the expected string values (New, Analyzing, Fixed, Rejected)
- [ ] Verify service methods compile and produce correct queries against the new schema

## Verification Commands
- `cargo check -p modules-fundamental` — module compiles
- `cargo test -p modules-fundamental -- advisory` — advisory-specific tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
