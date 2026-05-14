# Impact Map: TC-9001 — Add advisory severity aggregation endpoint

## Repository: trustify-backend

### Workflow Mode
`direct-to-main` — This is a standard feature with no atomicity constraints. No coordinated schema migrations, no breaking API changes spanning tasks, and no cross-cutting refactors.

### Summary of Changes

#### 1. New Model: Advisory Severity Summary
- **Create** `modules/fundamental/src/sbom/model/advisory_summary.rs` — Define `AdvisorySeveritySummary` response struct with fields: `critical`, `high`, `medium`, `low`, `total`

#### 2. Service Layer: Aggregation Query
- **Modify** `modules/fundamental/src/sbom/service/sbom.rs` — Add `get_advisory_severity_summary` method to `SbomService` that queries the `sbom_advisory` join table, joins to `advisory` for severity, groups by severity, and returns deduplicated counts
- **Modify** `modules/fundamental/src/sbom/service/mod.rs` — Re-export new types if needed

#### 3. SBOM Model Module Registration
- **Modify** `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod advisory_summary;` and re-export `AdvisorySeveritySummary`

#### 4. New Endpoint: Advisory Summary
- **Create** `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Implement `GET /api/v2/sbom/{id}/advisory-summary` handler with optional `?threshold` query param, 404 on missing SBOM, caching via `tower-http` cache middleware with 5-minute TTL
- **Modify** `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new `/api/v2/sbom/{id}/advisory-summary` route

#### 5. Cache Invalidation on Advisory Ingestion
- **Modify** `modules/ingestor/src/graph/advisory/mod.rs` — After advisory-to-SBOM correlation, invalidate cached advisory summaries for affected SBOM IDs

#### 6. Integration Tests
- **Create** `tests/api/sbom_advisory_summary.rs` — Integration tests covering: successful aggregation, 404 for missing SBOM, deduplication of advisories, threshold filtering, cache behavior
- **Modify** `tests/Cargo.toml` — Add new test file to test targets if required by project structure

### Entity Layer
- **No changes** — The feature requirement explicitly states no new database tables. The existing `entity/src/sbom_advisory.rs` join table and `entity/src/advisory.rs` entity (which includes severity) provide all necessary data.

### Dependencies Between Changes
1. Model struct (advisory_summary.rs) must exist before the service method and endpoint
2. Service method must exist before the endpoint handler
3. Endpoint must be registered before integration tests can run
4. Cache invalidation is independent of the endpoint but should be delivered together
