# Repository Impact Map -- TC-9002: Improve search experience

## Repositories

### trustify-backend

The entire feature scope is contained within the trustify-backend repository. The search module (`modules/search/`) is the primary target, with supporting changes in the common query infrastructure (`common/src/db/`) and entity layer.

#### Concrete Changes

1. **Search performance optimization** -- Investigate and optimize the full-text search implementation in `modules/search/src/service/mod.rs`. Add database indexes for search-relevant columns and optimize the query path.

2. **Search relevance improvements** -- Enhance the `SearchService` in `modules/search/src/service/mod.rs` to implement ranked/scored results. Update the search endpoint in `modules/search/src/endpoints/mod.rs` to return relevance scores.

3. **Add filtering to search** -- Extend the search endpoint (`modules/search/src/endpoints/mod.rs`) to accept filter parameters. Leverage the existing query builder helpers in `common/src/db/query.rs` for filtering infrastructure.

4. **Database migration for search indexes** -- Add a new migration under `migration/src/` to create database indexes that support faster and more relevant full-text search.

5. **Integration tests** -- Extend `tests/api/search.rs` with tests covering filtered search, relevance ordering, and performance baselines.

---

## Ambiguities and Open Questions

The feature description (TC-9002) is deliberately vague. The following ambiguities **must** be resolved with the product owner before implementation begins:

### Ambiguity 1: "Faster" has no measurable target

The requirement says search "should be faster" and is "currently too slow," but provides no latency targets, percentile goals, or baseline measurements. What does "fast enough" mean? Is the target p95 < 200ms? < 500ms? Under what data volume? Without a measurable SLA, there is no way to verify the requirement is met.

**ASSUMPTION -- pending clarification**: We assume the goal is to bring typical search response times under 500ms at p95 for the current production dataset size by adding appropriate database indexes and optimizing query patterns. This assumption needs validation with concrete benchmarks.

### Ambiguity 2: "More relevant results" is undefined

The requirement says results should be "more relevant" but does not define what relevance means in this context. Relevance could mean:
- Full-text ranking by term frequency (ts_rank in PostgreSQL)
- Prioritizing exact matches over partial matches
- Boosting certain entity types (e.g., advisories with high severity)
- Recency-based scoring

Without example queries and expected result orderings, we cannot validate that relevance has improved.

**ASSUMPTION -- pending clarification**: We assume PostgreSQL full-text search ranking (`ts_rank`) on the existing searchable fields is sufficient for MVP. Results will be ordered by relevance score descending, with an option to sort by other fields. This needs validation with real user queries and expected outcomes.

### Ambiguity 3: "Add filters" -- which filters, on which fields?

The requirement says "some kind of filtering capability" without specifying:
- Which entity fields should be filterable (severity? date range? package name? license?)
- Whether filters apply within a single entity type or across the unified search
- Whether filters are AND-combined or support OR logic
- What the filter parameter format should be (query string params? structured body?)

**ASSUMPTION -- pending clarification**: We assume MVP filters include: entity type (sbom, advisory, package), severity (for advisories), and date range (created_after / created_before). Filters are AND-combined and passed as query string parameters. This needs validation with UX research or product input.

### Ambiguity 4: Non-functional requirements are unmeasurable

"Should be fast enough" and "Don't break existing functionality" are not testable requirements. No performance budget, error rate tolerance, or regression test scope is defined.

**ASSUMPTION -- pending clarification**: We interpret "don't break existing functionality" as requiring that all existing integration tests in `tests/api/` continue to pass, and that existing search API consumers receive backward-compatible responses (existing fields preserved, new fields added additively).

### Ambiguity 5: Scope of "search" is unclear

The feature does not specify whether "search" refers only to the unified search endpoint (`GET /api/v2/search`) or also includes the list/filter capabilities on individual entity endpoints (e.g., `GET /api/v2/sbom`, `GET /api/v2/advisory`). It is unclear whether improvements should apply globally or only to the dedicated search module.

**ASSUMPTION -- pending clarification**: We scope this feature to the dedicated search module (`modules/search/`) and its endpoint (`GET /api/v2/search`). Individual entity list endpoints are out of scope for this feature.

---

## Out of Scope

### "Better UI" (Non-MVP)

The feature lists "Better UI -- Make it look nicer" as a non-MVP requirement. This is excluded from the implementation plan for two reasons:

1. **No frontend repository**: The trustify-backend repository is a Rust backend service. UI changes would require a separate frontend repository which is not part of this planning scope.
2. **No design specifications**: "Make it look nicer" provides no actionable design direction. UI work requires mockups, design tokens, or at minimum a description of what "nicer" means. This requirement cannot be planned without design input.

This item should be tracked as a separate feature once design mockups are available and a frontend repository is identified.

---

## Task Breakdown

| Task | Title | Repository | Dependencies |
|------|-------|------------|--------------|
| 1 | Add database migration for full-text search indexes | trustify-backend | None |
| 2 | Optimize SearchService for performance and relevance ranking | trustify-backend | Task 1 |
| 3 | Add filter support to the search endpoint | trustify-backend | Task 2 |
| 4 | Add integration tests for search improvements | trustify-backend | Task 3 |
