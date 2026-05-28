# Repository Impact Map -- TC-9001

## Feature: Add advisory severity aggregation endpoint

### trustify-backend:
  changes:
    - Add `AdvisorySeveritySummary` response model for severity counts (critical, high, medium, low, total)
    - Add `advisory_summary` method to `SbomService` that queries the `sbom_advisory` join table, deduplicates by advisory ID, and aggregates counts by severity
    - Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint with 5-minute cache and 404 handling for missing SBOMs
    - Support optional `?threshold` query parameter to filter severity counts above a given level
    - Add cache invalidation in the advisory ingestion pipeline when new advisories are linked to an SBOM
    - Add integration tests for the new endpoint covering success, 404, caching, deduplication, and threshold filtering

## Workflow Mode

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators are present:
- No coordinated schema migrations -- the feature uses existing tables (`sbom_advisory` join table) with no new migrations
- No breaking API changes -- this is a new additive endpoint that does not modify existing API contracts
- No cross-cutting refactors -- changes are contained within the SBOM module and advisory ingestion pipeline
- No tightly coupled cross-repo components -- this is a backend-only change
