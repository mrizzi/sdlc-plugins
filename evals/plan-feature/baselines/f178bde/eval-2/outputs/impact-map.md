# Repository Impact Map — TC-9002: Improve search experience

## Ambiguities and Clarification Needs

This feature description is significantly underspecified. The following ambiguities
must be resolved before implementation can proceed with confidence. The impact map
below represents a conservative scope based on available information, but tasks are
flagged where actual scope depends on answers to open questions.

### Critical Ambiguities

1. **No performance baseline or targets.** "Search should be faster" and "should be
   fast enough" provide no quantitative benchmarks. Current search latency is unknown;
   acceptable latency is undefined (e.g., p95 < 200ms?). Without measurable targets,
   the "faster" requirement cannot be verified as complete.

2. **"More relevant results" is undefined.** No definition of relevance is given. Does
   this mean improving full-text search ranking (e.g., `ts_rank` tuning, field boosting)?
   Adding typo tolerance or fuzzy matching? Supporting synonyms? Weighting by recency
   or severity? "Users complain about irrelevant results" does not specify what users
   expected vs. what they received.

3. **"Add filters" has no filter specification.** The feature says "some kind of
   filtering capability" without specifying:
   - Which entities support filtering (SBOMs, advisories, packages, or all?)
   - Which fields are filterable (severity? date range? license? package name?)
   - Whether filters apply to the unified search endpoint (`GET /api/v2/search`) or
     per-entity list endpoints (which already exist)
   - API shape for filter parameters (query params, request body, etc.)

4. **Search scope is unspecified.** The existing `modules/search/` module provides a
   unified search endpoint (`GET /api/v2/search`). It is unclear whether "improve
   search" targets this unified endpoint, the per-entity list endpoints (which already
   exist for SBOMs, advisories, packages), or both.

5. **Technology approach is unspecified.** No indication whether improvements should
   use PostgreSQL-native features (tsvector/tsquery, GIN indexes, `ts_rank`), an
   external search engine (Elasticsearch, Meilisearch), or application-layer changes
   only. The choice fundamentally changes the scope and complexity.

6. **No frontend repository configured.** The feature mentions "Better UI" (non-MVP)
   but the Repository Registry contains only `sdlc-plugins` (this plugin repo). No
   frontend repository is configured. All UI-related requirements cannot be planned.

7. **No Figma designs.** No UI mockups are linked or provided. Filter UI, result
   display improvements, and "Better UI" cannot be planned without visual specifications.

8. **"Don't break existing functionality" lacks a regression baseline.** Existing
   integration tests in `tests/api/search.rs` presumably cover current behavior, but
   the extent of backward-compatibility requirements is undefined. Can query parameters
   be added? Can response shape be extended? Must the current endpoint path be preserved?

### Assumptions Made for Planning

Given the ambiguities, the following conservative assumptions scope the tasks below.
These must be validated with the feature requester before implementation begins:

- **A1**: Performance improvements target the existing `GET /api/v2/search` endpoint
  and use PostgreSQL-native features (indexes, query optimization), not an external
  search engine.
- **A2**: "Filters" means adding query-parameter-based filtering to the existing
  search endpoint, covering the most commonly requested fields per entity type.
- **A3**: "More relevant" means improving full-text search ranking using PostgreSQL
  `ts_rank` or equivalent, not implementing a custom ML-based ranking system.
- **A4**: "Better UI" (non-MVP) is excluded from this plan due to no frontend
  repository and no Figma designs.
- **A5**: The existing `GET /api/v2/search` endpoint contract is extended (new
  parameters) but not broken (existing parameters and response shape remain functional).

---

## Impact Map

```
trustify-backend:
  changes:
    - Add database indexes to improve search query performance (specific indexes TBD pending baseline profiling)
    - Improve search result ranking using PostgreSQL full-text scoring (ts_rank or equivalent)
    - Add query-parameter-based filtering to the search endpoint (filter fields TBD pending clarification)
    - Extend SearchService to support filtered queries and improved ranking
    - Add integration tests for new search filters, ranking, and backward compatibility
    - Update API documentation (README.md) to reflect new search query parameters
```

## Repositories Involved

| Repository | Role |
|---|---|
| trustify-backend | All search improvements (API, service, database) |

## Task Breakdown

| Task | Title | Repository | Depends On |
|---|---|---|---|
| Task 1 | Add database indexes for search performance | trustify-backend | -- |
| Task 2 | Improve search result ranking with full-text scoring | trustify-backend | Task 1 |
| Task 3 | Add filtering parameters to search endpoint | trustify-backend | -- |
| Task 4 | Add integration tests for search improvements | trustify-backend | Task 2, Task 3 |

## Open Questions for Stakeholder

These questions should be answered before implementation begins. Without answers,
early tasks may require rework:

1. What is the current search latency, and what is the acceptable target? (e.g.,
   p95 < 200ms, p99 < 500ms)
2. What does "relevant" mean for search results? Should results be ranked by
   text-match quality, recency, severity, or a weighted combination?
3. Which specific filters are needed? Which entity fields should be filterable?
4. Should filters apply to the unified `GET /api/v2/search` endpoint, per-entity
   list endpoints, or both?
5. Is PostgreSQL-native search sufficient, or is an external search engine expected?
6. Are there specific user complaints or support tickets that illustrate the
   relevance and performance problems?
7. Is a frontend repository in scope for this feature? If so, which repository?
