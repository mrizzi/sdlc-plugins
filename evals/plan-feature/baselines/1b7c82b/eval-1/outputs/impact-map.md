# Repository Impact Map -- TC-9001

## Feature

**TC-9001**: Add advisory severity aggregation endpoint

## Workflow Mode

**Direct-to-main** -- This feature introduces a single additive REST endpoint with no schema migrations, no breaking API changes, and no cross-cutting refactors. Each task can be merged independently and incrementally.

## Impacted Repositories

### trustify-backend

#### modules/fundamental/src/sbom/model/

- **New file: `severity_summary.rs`** -- New `AdvisorySeveritySummary` response struct containing `critical`, `high`, `medium`, `low`, and `total` counts. Mirrors the module's existing model pattern (`summary.rs`, `details.rs`).
- **Modify: `mod.rs`** -- Add `pub mod severity_summary;` to register the new model submodule.

#### modules/fundamental/src/sbom/service/

- **Modify: `sbom.rs`** -- Add `advisory_severity_summary(&self, sbom_id: Uuid) -> Result<AdvisorySeveritySummary, AppError>` method to `SbomService`. Queries `sbom_advisory` join table joined with `advisory` entity, groups by severity, deduplicates by advisory ID, and returns aggregated counts.

#### modules/fundamental/src/sbom/endpoints/

- **New file: `advisory_summary.rs`** -- Handler for `GET /api/v2/sbom/{id}/advisory-summary`. Extracts path param `id` and optional query param `threshold`. Calls `SbomService::advisory_severity_summary`. Applies `tower-http` cache-control header (max-age=300). Returns 404 via `AppError` when SBOM not found.
- **Modify: `mod.rs`** -- Register the new `/api/v2/sbom/{id}/advisory-summary` route in the existing SBOM route group.

#### entity/src/

- **Read-only: `advisory.rs`** -- Reference the `severity` field on the `Advisory` entity for the aggregation query.
- **Read-only: `sbom_advisory.rs`** -- Reference the join table to correlate advisories with SBOMs.
- **Read-only: `sbom.rs`** -- Reference the SBOM entity for existence checks (404 handling).

#### modules/ingestor/src/graph/advisory/

- **Modify: `mod.rs`** -- After advisory-to-SBOM correlation completes, invalidate cached severity summaries for affected SBOM IDs. Uses the same cache infrastructure referenced by the endpoint.

#### common/src/

- **Read-only: `error.rs`** -- Reuse `AppError` enum for 404 and internal error responses.
- **Read-only: `db/query.rs`** -- Reference query builder helpers if needed for the aggregation query.

#### tests/api/

- **New file: `advisory_summary.rs`** -- Integration tests covering: successful aggregation, 404 for unknown SBOM, deduplication of advisory IDs, threshold filtering, and cache behavior.

## Cross-Cutting Concerns

- **Caching**: The endpoint uses `tower-http` caching middleware with a 5-minute max-age. Cache invalidation is handled in the ingestor pipeline (not a separate cache store).
- **No new database tables**: The aggregation uses existing `advisory`, `sbom`, and `sbom_advisory` entities/tables.
- **Performance target**: p95 < 200ms for SBOMs with up to 500 advisories. The aggregation query should use a SQL `GROUP BY` on severity rather than loading all advisories into memory.
