# Repository Impact Map — TC-9002: Improve search experience

## Ambiguities Identified

The feature description for TC-9002 is underspecified in several critical areas. The following ambiguities were identified and must be clarified with the product owner. Where noted, assumptions have been made to allow planning to proceed.

### Ambiguity 1: No quantitative performance targets

The requirement "Search should be faster" and the NFR "Should be fast enough" provide no measurable targets. There is no baseline latency documented, no target latency specified (e.g., p95 < 200ms), and no definition of what "too slow" means.

**Assumption (pending clarification):** We assume the goal is to add database indexing for full-text search columns and optimize the existing query path in the search module. Without concrete targets, we will focus on structural improvements (indexes, query optimization) and add instrumentation so performance can be measured and iterated on.

### Ambiguity 2: No definition of "relevant results"

The requirement "Results should be more relevant" provides no ranking criteria, no examples of irrelevant results, and no specification of what relevance means in this context. It is unclear whether this means improving full-text search ranking, adding field weighting, supporting exact-match vs fuzzy matching, or something else entirely.

**Assumption (pending clarification):** We assume relevance improvement means enhancing the existing `SearchService` in `modules/search/src/service/mod.rs` to use PostgreSQL full-text search ranking functions (`ts_rank`) and to support search across multiple entity fields (name, description, identifiers) rather than a single field. We assume no external search engine (e.g., Elasticsearch) is being introduced.

### Ambiguity 3: Filter specification is vague

The requirement "Add filters" says only "Some kind of filtering capability." It does not specify:
- Which entities should be filterable (SBOMs, advisories, packages, or all)
- Which fields should be filter criteria
- What filter UI types are needed (dropdowns, free text, date ranges)
- Whether filters combine with AND or OR logic

**Assumption (pending clarification):** We assume filters will be added to the existing search endpoint (`GET /api/v2/search`) allowing users to filter by entity type (SBOM, advisory, package) and by severity (for advisories). We will leverage the existing query builder helpers in `common/src/db/query.rs` which already support filtering and pagination patterns.

### Ambiguity 4: "Don't break existing functionality" is untestable as stated

The NFR "Don't break existing functionality" is not specific enough to be an acceptance criterion. No regression scenarios are identified.

**Assumption (pending clarification):** We interpret this as: all existing search endpoint integration tests in `tests/api/search.rs` must continue to pass, and the existing `GET /api/v2/search` API contract must remain backward-compatible (new query parameters are additive, not breaking).

### Ambiguity 5: "Better UI" is out of scope

The non-MVP requirement "Better UI" cannot be planned because:
- No frontend repository is listed in the Repository Registry (only `trustify-backend` is available)
- No Figma mockups or design specifications have been provided
- No design criteria for "better" have been defined

**This requirement is excluded from the implementation plan.** It should be revisited when a frontend repository is available and design mockups have been created.

---

## Impact Map

```
trustify-backend:
  changes:
    - Add PostgreSQL full-text search index migration for SBOM, advisory, and package searchable fields
    - Enhance SearchService to use ts_rank for relevance-based ordering of search results
    - Add entity-type and severity filter parameters to the search endpoint
    - Add query instrumentation/logging to measure search latency for future optimization
    - Update search endpoint integration tests to cover ranking, filtering, and performance scenarios
```

## Scope exclusion

- **"Better UI" requirement (non-MVP):** Excluded. No frontend repository exists in the Repository Registry and no design mockups were provided. This requirement cannot be planned without both a frontend codebase and Figma designs.
