# Impact Map: TC-9002 — Improve Search Experience

## Feature Summary

The feature requests improvements to the search experience across the trustify-backend platform: faster search, more relevant results, and filtering capabilities.

## Ambiguities and Open Questions

The feature description (TC-9002) is vague in several critical areas. The following ambiguities must be resolved with the product owner before implementation begins. Until then, the tasks below document explicit assumptions where gaps are filled.

### Ambiguity 1: No performance baseline or target for "faster" search

The requirement says "Search should be faster" and "Currently too slow," but provides no quantitative data. There is no current p50/p95 latency measurement, no target latency threshold (e.g., "results in under 200ms"), and no indication of whether the slowness is in the database query, network, or serialization layer.

**Assumption pending clarification**: We assume the bottleneck is in the database layer (missing indexes and unoptimized full-text queries) and target p95 < 500ms for typical searches. We also assume adding cache headers via the existing `tower-http` caching middleware will help with repeated queries.

### Ambiguity 2: No definition of "more relevant" results

The requirement says "Results should be more relevant" but does not define relevance criteria. It is unclear whether relevance means: ranking by text match quality, recency, severity, popularity, or some combination. It is also unclear which entity types (SBOMs, advisories, packages) should be ranked and whether ranking should differ by entity type.

**Assumption pending clarification**: We assume relevance means PostgreSQL `ts_rank` scoring on full-text search vectors, with advisory severity as a secondary ranking signal. We assume all three entity types (SBOMs, advisories, packages) are searched and results are interleaved by rank score.

### Ambiguity 3: "Add filters" is completely unspecified

The requirement says "Some kind of filtering capability" but does not specify: which fields should be filterable, what filter operators are needed (exact match, range, multi-select), whether filters are combined with AND or OR logic, or how filters interact with the existing search query.

**Assumption pending clarification**: We assume filters for entity type (SBOM, advisory, package), advisory severity, and date range (created/modified). We assume AND combination of filters. We follow the existing `common/src/db/query.rs` filtering pattern.

### Ambiguity 4: "Should be fast enough" is not a measurable NFR

The non-functional requirement "Should be fast enough" provides no quantifiable target. This makes it impossible to verify compliance or write meaningful performance acceptance criteria.

**Assumption pending clarification**: We treat this as equivalent to Ambiguity 1 and use the p95 < 500ms target assumption.

### Ambiguity 5: "Don't break existing functionality" lacks scope

This NFR is reasonable but vague. It is unclear whether it means backward-compatible API responses only, or also covers unchanged database schema for existing queries, unchanged indexing behavior, etc.

**Assumption pending clarification**: We assume backward-compatible API responses (existing clients must not break), and that adding new query parameters and response fields is acceptable as long as existing fields and default behavior are preserved.

## Excluded from Scope

### "Better UI" (Non-MVP)

The "Better UI — Make it look nicer" requirement is marked as non-MVP and **cannot be planned** in this scope for two reasons:

1. **No design mockups or specifications exist** — there is no definition of what "better" or "nicer" means visually.
2. **No frontend repository is available** — the only target repository is `trustify-backend`, which is a Rust REST API backend. UI changes require a frontend codebase that is not part of this planning scope.

This requirement is deferred entirely until design mockups are provided and a frontend repository is identified.

## Repository Impact

### trustify-backend

| Area | Impact | Files |
|---|---|---|
| Search service | Major — rewrite query logic for relevance ranking | `modules/search/src/service/mod.rs` |
| Search endpoints | Major — add filter parameters, update response format | `modules/search/src/endpoints/mod.rs` |
| Database migrations | New — add full-text search indexes | `migration/src/` (new migration) |
| Entity definitions | Minor — add text search vector annotations | `entity/src/sbom.rs`, `entity/src/advisory.rs`, `entity/src/package.rs` |
| Common query helpers | Moderate — extend filter support | `common/src/db/query.rs` |
| Integration tests | Major — new and updated search tests | `tests/api/search.rs` |
| Server setup | Minor — mount updated routes | `server/src/main.rs` |

## Task Breakdown

| Task | Title | Dependencies |
|---|---|---|
| 1 | Add database migration for full-text search indexes | None |
| 2 | Improve search relevance with weighted full-text ranking | Task 1 |
| 3 | Add filter parameters to search endpoint | Task 2 |
| 4 | Add response caching for search queries | Task 3 |
| 5 | Add and update search integration tests | Task 4 |
