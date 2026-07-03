# Impact Map: TC-9001 -- Add advisory severity aggregation endpoint

## Feature
Add a new REST API endpoint `GET /api/v2/sbom/{id}/advisory-summary` that aggregates vulnerability advisory severity counts (critical, high, medium, low, total) for a given SBOM, with optional threshold filtering and 5-minute response caching.

## Repositories Affected

| Repository | Role |
|---|---|
| trustify-backend | Primary -- all implementation, tests, and documentation changes land here. This is the Rust backend service that manages SBOMs, advisories, and exposes the REST API. |

## Specific Changes Needed

### Model Layer
- Create `AdvisorySeveritySummary` struct in `modules/fundamental/src/sbom/model/advisory_summary.rs` with fields: critical, high, medium, low, total
- Create `SeverityThreshold` enum for optional filtering (Critical, High, Medium, Low)
- Register the new model module in `modules/fundamental/src/sbom/model/mod.rs`

### Service Layer
- Add `advisory_severity_summary` method to `SbomService` in `modules/fundamental/src/sbom/service/sbom.rs`
- Aggregation query joins `sbom_advisory` with `advisory` entities, groups by severity, deduplicates by advisory ID
- Supports optional threshold parameter to filter severity levels

### Endpoint Layer
- Create `GET /api/v2/sbom/{id}/advisory-summary` handler in `modules/fundamental/src/sbom/endpoints/advisory_summary.rs`
- Register route in `modules/fundamental/src/sbom/endpoints/mod.rs`
- Apply 5-minute cache TTL via tower-http caching middleware
- Return 404 for non-existent SBOM IDs
- Accept optional `?threshold=critical|high|medium|low` query parameter

### Cache Invalidation
- Modify advisory ingestion pipeline in `modules/ingestor/src/graph/advisory/mod.rs` to invalidate cached advisory-summary when new advisories are linked to an SBOM
- Only invalidate cache entries for the specific SBOM(s) affected

### Integration Tests
- Create `tests/api/sbom_advisory_summary.rs` with test cases covering: valid counts, 404, threshold filter, deduplication, empty SBOM, cache header

### Documentation
- Update REST API reference with endpoint path, parameters, response schema, status codes, and caching behavior

## Workflow Mode Decision

**Mode**: Direct-to-main

**Rationale**: This feature is a single-repository change adding one new endpoint with supporting model, service, and test code. No atomicity indicators were identified:
- No coordinated schema migrations -- no new database tables are required; the feature uses existing `sbom_advisory` join table and `advisory` entity
- No breaking API changes -- all changes are additive (new endpoint, new response type)
- No cross-cutting refactors -- changes are scoped to new files and targeted modifications
- No tightly coupled cross-repo components -- all changes land in a single repository

Individual task PRs can be merged to main independently without leaving the codebase in a broken state.
