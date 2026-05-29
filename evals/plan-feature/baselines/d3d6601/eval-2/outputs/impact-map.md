# Repository Impact Map — TC-9002: Improve search experience

## Ambiguities Identified

The feature description (TC-9002) contains significant ambiguities that must be resolved before full implementation. The following ambiguities were identified during analysis:

1. **"Search should be faster" — no performance target defined.** The requirement says "currently too slow" but provides no baseline measurement (current latency) or target metric (e.g., "results in under 200ms for 95th percentile"). Without a measurable target, "faster" is subjective and unverifiable. **Assumption pending clarification:** We assume a target of sub-500ms p95 response time for search queries, which can be achieved through query optimization and database indexing.

2. **"Results should be more relevant" — no relevance criteria defined.** The requirement mentions "irrelevant results" but does not specify what makes a result relevant. There is no ranking algorithm preference (e.g., TF-IDF, BM25, exact match priority), no field weighting scheme (e.g., should title matches rank higher than description matches?), and no specification of which entity types should be searchable. **Assumption pending clarification:** We assume relevance improvements should use PostgreSQL full-text search with ts_vector/ts_query, weighting title matches above description matches, and covering SBOMs, advisories, and packages.

3. **"Add filters — some kind of filtering capability" — filter dimensions unspecified.** The requirement does not state which fields should be filterable, what filter types are needed (exact match, range, multi-select), or how filters interact with each other (AND vs OR). **Assumption pending clarification:** We assume filters should cover the primary entity attributes: severity (for advisories), license (for packages), and date range (for SBOMs), using AND composition between filter groups.

4. **"Should be fast enough" — non-functional requirement is unmeasurable.** The non-functional requirement "should be fast enough" provides no quantitative threshold. **Assumption pending clarification:** We apply the same sub-500ms p95 target assumed for the search speed requirement.

5. **"Don't break existing functionality" — no regression test baseline mentioned.** There is no specification of which existing behaviors are critical to preserve or how to verify non-breakage. **Assumption pending clarification:** Existing integration tests in `tests/api/search.rs` serve as the regression baseline; all existing tests must continue to pass.

## Scope Exclusion

**"Better UI" (non-MVP) is excluded from this plan.** This requirement is marked as non-MVP and cannot be planned because:
- No Figma mockups or design specifications are provided
- No frontend repository is available in the Repository Registry (only trustify-backend is in scope)
- "Make it look nicer" is entirely subjective without visual design guidance

This requirement should be planned separately once design mockups are available and a frontend repository is configured.

## Workflow Mode

**Selected mode: `direct-to-main`**

**Rationale:** No atomicity indicators are present. The three MVP requirements (search performance, search relevance, filtering) can each be delivered independently to `main` without breaking existing functionality:
- Search performance improvements (indexing, query optimization) are additive and backward-compatible
- Relevance improvements enhance existing search results without changing the API contract shape
- Filters extend the existing search endpoint with optional query parameters (non-breaking)

No coordinated schema migrations, breaking API changes, cross-cutting refactors, or tightly coupled components were identified.

## Impact Map

```
trustify-backend:
  changes:
    - Add full-text search indexes to SBOM, advisory, and package tables via database migration
    - Refactor SearchService to use PostgreSQL full-text search (tsvector/tsquery) with field weighting for improved relevance
    - Add filter parameters (severity, license, date range) to the GET /api/v2/search endpoint
    - Add query builder helpers for full-text search and filter composition in common/src/db/query.rs
    - Update search endpoint handler to accept and apply filter query parameters
    - Add integration tests for search performance, relevance ordering, and filter combinations
```
