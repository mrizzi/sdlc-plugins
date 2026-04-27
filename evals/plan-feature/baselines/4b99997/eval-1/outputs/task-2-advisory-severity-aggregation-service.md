## Repository
trustify-backend

## Description
Add a `get_advisory_severity_summary` method to `SbomService` that queries the database for all advisories linked to a given SBOM, deduplicates by advisory ID, groups by severity level, and returns an `AdvisorySeveritySummary` with the aggregated counts. This method pushes the severity counting computation to the backend, replacing the current pattern where frontends must paginate through all advisories and count client-side.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add `get_advisory_severity_summary(&self, sbom_id: Uuid, db: &DatabaseConnection) -> Result<AdvisorySeveritySummary, AppError>` method to `SbomService`

## API Changes
- Internal service API: `SbomService::get_advisory_severity_summary(sbom_id, db)` — NEW: aggregates advisory severity counts for an SBOM

## Implementation Notes
- Follow the existing service method patterns in `modules/fundamental/src/sbom/service/sbom.rs` (e.g., `fetch`, `list`, `ingest` methods) for error handling with `Result<T, AppError>` and `.context()` wrapping.
- Use SeaORM to query the `sbom_advisory` join table entity (`entity/src/sbom_advisory.rs`) joined with the `advisory` entity (`entity/src/advisory.rs`) to access the severity field.
- Deduplicate by advisory ID before counting -- use `SELECT DISTINCT advisory_id, severity FROM sbom_advisory JOIN advisory ON ...` or equivalent SeaORM query to avoid double-counting advisories linked via multiple paths.
- Group results by severity and count each group. Map severity values to the four levels: critical, high, medium, low. Compute `total` as the sum of all four counts.
- Return a 404 `AppError` if the SBOM ID does not exist -- check SBOM existence before running the aggregation query. Follow the existing 404 pattern used in `modules/fundamental/src/sbom/endpoints/get.rs`.
- Use the shared query helpers from `common/src/db/query.rs` where applicable for building the aggregation query.
- Per `docs/constraints.md` section 5 (Code Change Rules): inspect existing service methods before writing; follow the established patterns for error handling, database interaction, and return types.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service struct to which the new method is added; follow its method signature and error handling patterns
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — reference for how advisory-related queries are structured, including severity field access
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity; defines the relationship used to find advisories for an SBOM
- `entity/src/advisory.rs` — Advisory entity; contains the severity field definition
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` — error enum used for 404 and other error responses

## Acceptance Criteria
- [ ] `SbomService::get_advisory_severity_summary` method exists and compiles
- [ ] Method returns correct severity counts when given an SBOM with known advisories
- [ ] Method deduplicates advisories by advisory ID (same advisory linked multiple times is counted once)
- [ ] Method returns 404 error when SBOM ID does not exist
- [ ] Method uses `Result<AdvisorySeveritySummary, AppError>` return type with `.context()` error wrapping

## Test Requirements
- [ ] Unit/integration test: SBOM with advisories at all four severity levels returns correct counts
- [ ] Unit/integration test: SBOM with duplicate advisory links counts each advisory only once
- [ ] Unit/integration test: nonexistent SBOM ID returns appropriate error

## Verification Commands
- `cargo check -p trustify-module-fundamental` — compiles without errors
- `cargo test -p trustify-module-fundamental -- advisory_severity` — relevant tests pass

## Dependencies
- Depends on: Task 1 — Create advisory severity summary model
