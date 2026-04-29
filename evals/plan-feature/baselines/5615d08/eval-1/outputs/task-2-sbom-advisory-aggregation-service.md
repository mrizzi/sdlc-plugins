## Repository
trustify-backend

## Description
Implement the service-layer method that queries the database to compute advisory severity counts for a given SBOM. This method joins the `sbom_advisory` relationship table with the `advisory` table, groups by severity, and returns an `AdvisorySeveritySummary`. It also validates that the SBOM exists, returning an appropriate error if not found.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — Add `async fn advisory_summary(&self, sbom_id: Uuid, db: &DatabaseConnection) -> Result<AdvisorySeveritySummary, AppError>` to `SbomService`
- `modules/fundamental/src/sbom/service/mod.rs` — Ensure the new method is accessible (re-export if needed)

## Implementation Notes
- Add the method to `SbomService` in `modules/fundamental/src/sbom/service/sbom.rs`, following the pattern of existing methods like `fetch` and `list` in the same file.
- Use SeaORM to query the `sbom_advisory` join entity (`entity/src/sbom_advisory.rs`) joined with the `advisory` entity (`entity/src/advisory.rs`) to access the severity column.
- Filter by `sbom_advisory::Column::SbomId == sbom_id`.
- First verify the SBOM exists by calling the existing `fetch` method on `SbomService`; if `None`, return `AppError::NotFound` (defined in `common/src/error.rs`).
- Deduplicate by advisory ID before counting — use `SELECT DISTINCT advisory_id` or group by `advisory.id` to avoid double-counting advisories linked through multiple paths.
- Group the results by severity and count each group. Map severity enum variants to the corresponding `AdvisorySeveritySummary` fields.
- Compute `total` as the sum of all severity counts.
- Use `.context()` wrapping on database errors, consistent with the error handling pattern in `common/src/error.rs`.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService::fetch` — Reuse to validate SBOM existence before aggregation
- `entity/src/sbom_advisory.rs` — The join entity connecting SBOMs to advisories
- `entity/src/advisory.rs` — The advisory entity containing the severity column
- `common/src/error.rs::AppError` — Error type for NotFound and internal errors
- `common/src/db/query.rs` — Shared query builder helpers if needed for filtering

## Acceptance Criteria
- [ ] `SbomService::advisory_summary` method exists and compiles
- [ ] Method returns `AdvisorySeveritySummary` with correct counts grouped by severity
- [ ] Advisories are deduplicated by advisory ID (no double-counting)
- [ ] Method returns `AppError::NotFound` when the SBOM ID does not exist
- [ ] Database errors are wrapped with `.context()` producing meaningful messages

## Test Requirements
- [ ] Unit/service test: given an SBOM with known advisories at various severities, verify the returned counts match expected values
- [ ] Unit/service test: verify that duplicate advisory links are deduplicated (same advisory linked twice yields count of 1)
- [ ] Unit/service test: calling with a non-existent SBOM ID returns a NotFound error

## Dependencies
- Depends on: Task 1 — Advisory severity summary model (provides `AdvisorySeveritySummary` struct)
