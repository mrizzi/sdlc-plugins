# Plan Summary — TC-9001: Add advisory severity aggregation endpoint

## Tasks Created

| # | Summary | Repository | Type |
|---|---|---|---|
| 1 | Add AdvisorySeveritySummary model and aggregation service method | trustify-backend | Implementation |
| 2 | Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching and threshold filter | trustify-backend | Implementation |
| 3 | Add cache invalidation for advisory-summary during advisory ingestion | trustify-backend | Implementation |
| 4 | Add integration tests for advisory-summary endpoint | trustify-backend | Implementation |
| 5 | Add advisory-summary endpoint to REST API reference documentation | trustify-backend | Documentation |
| 6 | Smoke Tests — advisory severity aggregation endpoint | trustify-backend | Testing |
| 7 | Performance Benchmarks — advisory severity aggregation endpoint | trustify-backend | Testing |

## Repositories Affected

- **trustify-backend** — all 7 tasks target this repository

## Architecture Summary

The implementation adds a new aggregation endpoint to the existing SBOM module following the established model/service/endpoints pattern. A new `AdvisorySeveritySummary` model struct captures severity counts (critical, high, medium, low, total). The `SbomService` gains an aggregation method that queries the existing `sbom_advisory` join table with deduplication by advisory ID — no new database tables are required. The endpoint is registered under the SBOM route tree at `GET /api/v2/sbom/{id}/advisory-summary` with 5-minute tower-http caching and an optional `?threshold` query parameter for severity filtering. Cache invalidation is added to the advisory ingestion pipeline in `modules/ingestor/src/graph/advisory/mod.rs` to ensure freshness when new advisories are correlated. Integration tests follow the existing `tests/api/` patterns against a real PostgreSQL test database.

## Inherited Field Values

- **Priority**: Major — propagated to all created tasks via `additional_fields.priority`
- **fixVersions**: RHTPA 1.5.0 — propagated to all created tasks via `additional_fields.fixVersions` (fixVersion scope defaults to "both" since no `### Jira Field Defaults` section exists in CLAUDE.md)

## Workflow Mode

**direct-to-main** — tasks can be merged independently without breaking main. No atomicity indicators (coordinated schema migrations, breaking API changes, cross-cutting refactors, or tightly coupled components) were identified.
