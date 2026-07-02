## Implementation Plan: TC-9002 — Improve Search Experience

### Tasks Created

| # | Task | Key Files |
|---|------|-----------|
| 1 | Add database migration for full-text search indexes | `migration/src/m0002_search_indexes/mod.rs` (new), `migration/src/lib.rs` |
| 2 | Enhance SearchService with full-text search ranking | `modules/search/src/service/mod.rs` |
| 3 | Add filter query parameters to search endpoint | `modules/search/src/endpoints/mod.rs`, `modules/search/src/service/mod.rs` |
| 4 | Add integration tests for enhanced search | `tests/api/search.rs` |

### Repos Affected

- **trustify-backend** (all 4 tasks)

### Architecture Summary

The implementation adds PostgreSQL full-text search infrastructure to the trustify-backend search module:

1. **Database layer**: A new migration adds `tsvector` columns and GIN indexes to the `sbom`, `advisory`, and `package` tables, with triggers to keep the search vectors current on data changes.
2. **Service layer**: The `SearchService` is enhanced to use `tsquery` matching against the indexed `tsvector` columns, with `ts_rank()` ordering for relevance-based result ranking.
3. **API layer**: The `GET /api/v2/search` endpoint gains optional filter query parameters (`type`, `severity`, `from`, `to`) that allow users to narrow results. Filters use AND combination semantics and are built using the shared query helpers in `common/src/db/query.rs`.
4. **Testing**: Integration tests in `tests/api/search.rs` validate ranking, filtering, filter combinations, error handling, and backward compatibility against a real PostgreSQL database.

The "Better UI" requirement (non-MVP) is excluded from this plan because no frontend repository is configured and no design mockups are available.

### Ambiguities Flagged

Five ambiguities were identified in the feature description and documented with assumptions pending clarification:
1. No performance baseline or target for "search should be faster"
2. No relevance criteria for "results should be more relevant"
3. No filter specification for "add filters"
4. No quantitative target for "should be fast enough"
5. No design artifacts for "Better UI" (excluded from scope)

### Propagated Fields

- Priority: Normal (propagated to all tasks)
- Fix Versions: RHTPA 1.6.0 (propagated to all tasks, fixVersion scope defaults to 'both')
