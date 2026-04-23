## Repository
trustify-backend

## Description
Add an `advisory_severity_summary` method to `SbomService` that queries the existing `sbom_advisory` join table and `advisory` entity to produce an `AdvisorySeveritySummary`. The method must return a 404 `AppError` if the SBOM does not exist, and must deduplicate advisories by advisory ID before counting. No new database tables are introduced — the query works entirely through SeaORM on `entity::sbom_advisory` and `entity::advisory`.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add `pub async fn advisory_severity_summary(&self, sbom_id: Uuid, db: &DatabaseConnection) -> Result<AdvisorySeveritySummary, AppError>`

## Implementation Notes
`SbomService` in `modules/fundamental/src/sbom/service/sbom.rs` already contains methods such as `fetch` and `list` that follow this pattern:

1. Query the `sbom` entity to verify existence; return `AppError::NotFound` (from `common/src/error.rs`) if no row is found.
2. Build a SeaORM select on the join entity. The `entity::sbom_advisory` entity (defined in `entity/src/sbom_advisory.rs`) links SBOM IDs to advisory IDs. Join to `entity::advisory` (defined in `entity/src/advisory.rs`) to retrieve the `severity` column.
3. Use `.distinct()` or group the query by advisory ID to deduplicate before collecting results, since the same advisory can appear in multiple SBOM-advisory rows (e.g., linked through different packages).
4. Iterate the result rows and call `AdvisorySeveritySummary::add_advisory(&row.severity)` to accumulate counts.
5. Return the populated `AdvisorySeveritySummary`.

Refer to `modules/fundamental/src/sbom/service/sbom.rs` for the `use` imports already present (`entity::prelude::*`, `sea_orm::*`, `common::error::AppError`, `uuid::Uuid`). Do not add duplicate imports.

The `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs` may already perform advisory queries that filter by SBOM — check for a reusable inner query before writing a new one from scratch.

Error handling pattern to follow (consistent with existing handlers):
```rust
let sbom = entity::sbom::Entity::find_by_id(sbom_id)
    .one(db)
    .await
    .context("failed to fetch SBOM")?
    .ok_or(AppError::NotFound("sbom not found".into()))?;
```

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService::fetch` — pattern for existence check and `AppError::NotFound` usage
- `entity/src/sbom_advisory.rs` — join table entity with `sbom_id` and `advisory_id` columns
- `entity/src/advisory.rs` — advisory entity with `severity` column
- `common/src/error.rs::AppError` — error enum; use `AppError::NotFound` for missing SBOM

## Acceptance Criteria
- [ ] `advisory_severity_summary` returns `AppError::NotFound` when no SBOM with the given ID exists
- [ ] Advisory deduplication is applied — an advisory linked multiple times to the same SBOM is counted once
- [ ] Returned `AdvisorySeveritySummary::total` equals `critical + high + medium + low`
- [ ] `cargo check -p fundamental` passes with no warnings

## Test Requirements
- [ ] Unit/integration test: SBOM with 2 critical and 1 high advisory returns `{ critical: 2, high: 1, medium: 0, low: 0, total: 3 }`
- [ ] Unit/integration test: SBOM with the same advisory linked twice returns a count of 1 for that advisory (deduplication)
- [ ] Unit/integration test: non-existent SBOM ID returns `AppError::NotFound`

## Dependencies
- Depends on: Task 1 — Add `AdvisorySeveritySummary` response model
