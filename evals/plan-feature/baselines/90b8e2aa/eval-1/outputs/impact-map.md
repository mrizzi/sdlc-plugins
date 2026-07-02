# Repository Impact Map — TC-9001

## Workflow Mode

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators were identified:
- No coordinated schema migrations — the feature explicitly requires no new database tables
- No breaking API changes — this adds a new endpoint without modifying existing ones
- No cross-cutting refactors — changes are additive within a single module
- No tightly coupled cross-repo components — all changes are within trustify-backend

All tasks can be merged independently to `main` without leaving the codebase in a broken state.

## Impact Map

```
trustify-backend:
  changes:
    - Add AdvisorySeveritySummary response model struct for severity count response shape
    - Add severity aggregation query method to SbomService that counts advisories by severity using the sbom_advisory join table
    - Add GET /api/v2/sbom/{id}/advisory-summary endpoint handler with 5-minute cache and 404 for missing SBOMs
    - Add optional ?threshold query parameter to filter severity counts above a given level
    - Add cache invalidation in advisory ingestion pipeline when new advisories are linked to an SBOM
    - Add integration tests for the new advisory-summary endpoint covering happy path, 404, deduplication, threshold filtering, and caching
    - Update API documentation to include the new endpoint path, parameters, and response shape
```

## Issue Type Discovery

**Note:** Jira MCP is unavailable in this eval context. Issue type discovery (Step 2.5) could not be performed. No level-1 (Epic) type was discovered. Tasks will be created directly under the Feature using Feature -> Task hierarchy.

## Field Inheritance

- **Priority:** Major (inherited from Feature TC-9001, will be propagated to all tasks)
- **fixVersions:** RHTPA 1.5.0 (inherited from Feature TC-9001; no `fixVersion scope` setting found in Jira Field Defaults, defaulting to "both" — will be propagated to all tasks)
