# Impact Map: TC-9002 — Improve Search Experience

## Feature Summary

Improve the search experience in the trustify-backend platform by making search faster, returning more relevant results, and adding filtering capabilities.

## Ambiguities and Open Questions

The feature description (TC-9002) is vague in several critical areas. The following ambiguities must be resolved before implementation begins:

1. **"Search should be faster" — No performance baseline or target defined.**
   - What is the current p50/p95 latency? What is the acceptable target? (e.g., < 200ms p95)
   - Assumption pending clarification: We assume the goal is sub-500ms p95 for typical queries, and that PostgreSQL full-text search indexing is the primary optimization lever.

2. **"Results should be more relevant" — No relevance criteria defined.**
   - What does "relevant" mean? Ranking by recency? By text-match score? By severity?
   - Which entity types should be searched (SBOMs, advisories, packages, or all)?
   - Assumption pending clarification: We assume relevance means PostgreSQL `ts_rank` scoring on full-text search vectors, searching across SBOMs, advisories, and packages.

3. **"Add filters — Some kind of filtering capability" — No filter fields specified.**
   - Which fields should be filterable? Severity? Date range? Package name? License? Entity type?
   - Should filters be combinable (AND logic)?
   - Assumption pending clarification: We assume MVP filters are: entity type (sbom/advisory/package), date range (created after/before), and severity (for advisories). Filters are combined with AND logic.

4. **"Better UI — Make it look nicer" — No design specifications, no frontend repository.**
   - This requirement cannot be planned without design mockups or access to a frontend repository. It is explicitly excluded from this plan's scope. A separate feature should be created for UI improvements once designs are available.

5. **"Should be fast enough" (non-functional) — No quantitative target.**
   - Assumption pending clarification: We interpret "fast enough" as the performance target in item 1 above.

6. **"Don't break existing functionality" — Standard but worth noting.**
   - Assumption pending clarification: Existing `GET /api/v2/search` contract must remain backward-compatible. New parameters are additive (optional query parameters).

## Scope

### In Scope
- Performance optimization of the existing search service (indexing, query optimization)
- Relevance ranking for search results
- Adding filter parameters to the search endpoint
- Integration tests for all changes
- Database migration for search indexes

### Out of Scope
- "Better UI" requirement — excluded due to lack of design mockups and frontend repository
- Changes to ingestion pipelines (unless required for indexing)
- New search infrastructure (e.g., Elasticsearch) — assumption is PostgreSQL-native search

## Impact Analysis

### Files Modified

| File | Impact | Reason |
|---|---|---|
| `modules/search/src/service/mod.rs` | HIGH | Core search logic: add ranking, filtering, query optimization |
| `modules/search/src/endpoints/mod.rs` | HIGH | Add filter query parameters to `GET /api/v2/search` |
| `common/src/db/query.rs` | MEDIUM | Extend shared query helpers with full-text search and filter support |
| `common/src/model/paginated.rs` | LOW | May need to include relevance score in paginated results |
| `tests/api/search.rs` | HIGH | Add/update integration tests for new search behavior |

### Files Created

| File | Purpose |
|---|---|
| `migration/src/m0002_search_indexes/mod.rs` | Database migration to add GIN indexes for full-text search |
| `modules/search/src/service/filter.rs` | Filter parsing and application logic |
| `modules/search/src/model/mod.rs` | Search result model with relevance score |

### API Changes

| Endpoint | Change | Details |
|---|---|---|
| `GET /api/v2/search` | MODIFY | Add optional query parameters: `type`, `severity`, `created_after`, `created_before`. Add `score` field to result items. |

## Task Breakdown

| # | Task | Depends On | Repository |
|---|---|---|---|
| 1 | Add full-text search indexes via database migration | — | trustify-backend |
| 2 | Implement relevance-ranked search in SearchService | Task 1 | trustify-backend |
| 3 | Add filter parameter support to search endpoint | Task 2 | trustify-backend |
| 4 | Add search result model with relevance score | Task 2 | trustify-backend |
| 5 | Write integration tests for search improvements | Tasks 2, 3, 4 | trustify-backend |

## Assumptions Pending Clarification

All assumptions listed above are working assumptions to unblock planning. They should be validated with the product owner before implementation begins:

- Performance target: sub-500ms p95 response time for search queries
- Relevance: PostgreSQL `ts_rank` scoring on full-text search vectors
- Filter fields: entity type, date range, severity
- Search scope: SBOMs, advisories, and packages
- Backward compatibility: existing search API contract preserved, new parameters are optional
- No new search infrastructure (staying with PostgreSQL)
- "Better UI" is deferred to a separate feature with frontend team involvement
