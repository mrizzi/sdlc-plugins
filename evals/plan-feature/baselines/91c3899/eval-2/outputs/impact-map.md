# Repository Impact Map — TC-9002: Improve search experience

## Ambiguities Identified

The feature description (TC-9002) is vague and incomplete. The following ambiguities were identified and must be resolved with the product owner before implementation begins:

1. **"Search should be faster" — no performance baseline or target.** The description says search is "currently too slow" and should be "fast enough," but provides no current latency measurements, no target response time (e.g., p95 < 200ms), and no indication of data volume. **ASSUMPTION pending clarification:** We assume the goal is to add database indexing and optimize the existing `SearchService` query patterns to reduce response time, targeting sub-500ms p95 for typical queries.

2. **"Results should be more relevant" — no relevance criteria defined.** The description says users complain about "irrelevant results" but does not define what makes a result relevant (e.g., field weighting, exact vs fuzzy matching, recency bias, entity-type prioritization). **ASSUMPTION pending clarification:** We assume relevance improvements mean implementing PostgreSQL full-text search with `ts_vector`/`ts_query` and field weighting (e.g., title matches ranked higher than description matches) on SBOM, advisory, and package entities.

3. **"Add filters" — no filter specification.** The requirement says "some kind of filtering capability" without specifying which entities support filtering, which fields are filterable, or what filter operations are needed (exact match, range, multi-select). **ASSUMPTION pending clarification:** We assume filters should be added to the existing search endpoint (`GET /api/v2/search`) covering common entity fields: entity type (SBOM/advisory/package), severity (for advisories), and date range. These align with the existing entity model fields visible in the repository structure.

4. **"Should be fast enough" — undefined non-functional requirement.** No quantitative performance targets. **ASSUMPTION pending clarification:** We assume standard API performance expectations: p95 response time under 500ms for filtered search queries on datasets up to 100K entities.

5. **"Better UI" (non-MVP) — EXCLUDED FROM SCOPE.** This requirement cannot be planned: there is no frontend repository in the Repository Registry, no Figma design mockups are linked or available, and the feature description provides no specifics about what "better" means. This requirement is excluded from the implementation plan entirely. It should be revisited once design mockups are available and a frontend repository is identified.

## Impact Map

```
trustify-backend:
  changes:
    - Add database migration for full-text search indexes (tsvector columns and GIN indexes on SBOM, advisory, and package tables)
    - Extend search service to use PostgreSQL full-text search with field weighting for improved relevance
    - Add filter parameters to the search endpoint (entity type, severity, date range)
    - Update search endpoint to accept and apply filter query parameters
    - Add query builder helpers for full-text search and filtering in common module
    - Update integration tests for search with new filtering and relevance improvements
```

## Workflow Mode Decision

**Selected mode: `direct-to-main`**

**Rationale:** No atomicity indicators are present:
- No coordinated schema migrations across multiple tasks — the migration is a single additive change (new indexes/columns) that does not break existing functionality
- No breaking API changes — the search endpoint changes are additive (new optional query parameters); existing callers are unaffected
- No cross-cutting refactors — changes are localized to the search module, common query helpers, and the migration
- No tightly coupled cross-repo components — only one repository (trustify-backend) is affected, and there is no frontend counterpart in scope

Each task PR can be merged to `main` independently without leaving the codebase in a broken state.
