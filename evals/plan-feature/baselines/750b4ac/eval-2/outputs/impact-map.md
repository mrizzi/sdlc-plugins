# Repository Impact Map — TC-9002: Improve search experience

## Ambiguities Identified

The feature description (TC-9002) contains significant ambiguities that must be resolved before or during implementation. The following gaps were identified:

1. **No performance target for "faster" search.** The requirement says "search should be faster" and "should be fast enough" but provides no measurable SLA (e.g., p95 < 200ms). **Assumption pending clarification:** We assume the goal is to add database indexing and optimize query patterns to reduce response time, with performance validated via benchmarks rather than a specific SLA.

2. **No definition of "more relevant" results.** The requirement says "results should be more relevant" but does not define a relevance ranking model, scoring algorithm, or which fields should be weighted. **Assumption pending clarification:** We assume relevance improvement means leveraging PostgreSQL full-text search with `ts_vector`/`ts_query` and applying ranking via `ts_rank` on indexed text fields, replacing any naive LIKE/ILIKE queries.

3. **No specification of filter fields or behavior.** The requirement says "add filters" with "some kind of filtering capability" but does not specify which fields are filterable, whether filters are AND/OR, or what filter types are supported (exact match, range, multi-select). **Assumption pending clarification:** We assume filters should cover the primary entity attributes discoverable from the existing models: entity type, severity (for advisories), and date range. Additional filters can be added incrementally.

4. **No clarity on which entities are searchable.** The feature does not specify whether search covers SBOMs, advisories, packages, or all entities. The existing `SearchService` provides "full-text search across entities." **Assumption pending clarification:** We assume search covers all existing entity types (SBOMs, advisories, packages) as the current SearchService already spans them.

5. **"Better UI" is non-MVP and out of scope.** This requirement is marked non-MVP and cannot be planned without design mockups and a frontend repository. It is excluded from this plan entirely.

## Workflow Mode

**Mode:** `direct-to-main`

**Rationale:** No atomicity indicators are present. All changes target the same repository (trustify-backend) and each task can be merged independently without leaving main in a broken state. The search endpoint already exists — tasks add indexing, improve queries, and add filter parameters incrementally. No coordinated schema migrations or breaking API changes exist between tasks.

## Impact Map

```
trustify-backend:
  changes:
    - Add PostgreSQL full-text search indexes via database migration for SBOM, advisory, and package text fields
    - Refactor SearchService to use ts_vector/ts_query full-text search with ts_rank relevance scoring instead of naive text matching
    - Add filter parameters (entity type, severity, date range) to the GET /api/v2/search endpoint
    - Add database indexes on frequently filtered columns to improve query performance
    - Update integration tests in tests/api/search.rs to cover full-text search, relevance ranking, and filter parameters
```
