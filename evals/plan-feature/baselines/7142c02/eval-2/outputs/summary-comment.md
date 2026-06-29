# Implementation Plan Summary — TC-9002: Improve search experience

## Ambiguity Notice

This feature description is underspecified in several critical areas. **6 ambiguities** were identified and documented in the impact map. Key gaps:

1. **No quantitative performance targets** — "faster" and "fast enough" are not measurable. Assumed: add database indexes and optimize query patterns.
2. **No relevance ranking criteria** — "more relevant" is undefined. Assumed: weighted full-text scoring with name/title priority over description.
3. **Filter dimensions unspecified** — "some kind of filtering" gives no details. Assumed: entity type, severity, and date range filters based on existing entity models.
4. **Search scope undefined** — which entity types are in scope is not stated. Assumed: all entities (SBOMs, advisories, packages).
5. **"Better UI" cannot be planned** — Non-MVP item with no design mockups, targeting a frontend not in this repository. Excluded entirely.
6. **No breaking change policy** — "Don't break existing functionality" lacks specifics. Assumed: all API changes are backward-compatible (additive only).

All assumptions are labeled as **pending clarification** in the task descriptions. The feature owner should review and confirm or adjust before implementation begins.

## Tasks Created

| # | Task | Repository | Key Files |
|---|---|---|---|
| 1 | Add database indexes for full-text search optimization | trustify-backend | `migration/src/m0002_search_indexes/mod.rs` (new), `migration/src/lib.rs` |
| 2 | Implement relevance-scored search ranking | trustify-backend | `modules/search/src/service/mod.rs`, `modules/search/src/endpoints/mod.rs`, `common/src/db/query.rs` |
| 3 | Add search filter parameters to the search endpoint | trustify-backend | `modules/search/src/endpoints/mod.rs`, `modules/search/src/service/mod.rs`, `common/src/db/query.rs` |
| 4 | Add integration tests for search improvements | trustify-backend | `tests/api/search.rs` |

## Repositories Affected

- **trustify-backend** — all 4 tasks target this repository

## Architecture Summary

The implementation follows a bottom-up approach:

1. **Database layer** (Task 1): Add GIN full-text search indexes via a new SeaORM migration. This is the foundation that enables efficient `ts_rank` queries.
2. **Service layer** (Task 2): Replace simple text matching in `SearchService` with PostgreSQL `ts_rank`-based relevance scoring. Adds a `search_rank` helper to the shared query builder in `common/src/db/query.rs`.
3. **API layer** (Task 3): Extend the `GET /api/v2/search` endpoint with filter query parameters (`entity_type`, `severity`, `date_from`, `date_to`). Reuses existing query builder patterns.
4. **Verification** (Task 4): Comprehensive integration tests covering relevance ordering, filter combinations, edge cases, and backward compatibility.

All tasks follow the existing module pattern (`model/ + service/ + endpoints/`), use `Result<T, AppError>` error handling, return `PaginatedResults<T>` responses, and follow the integration test patterns in `tests/api/`.

## Dependency Chain

```
Task 1 → Task 2 → Task 3 → Task 4
```

## Inherited Fields

- **Priority**: Normal (inherited from TC-9002)
- **Fix Version**: RHTPA 1.6.0 (inherited from TC-9002)

## Out of Scope

- **Better UI** (non-MVP): Requires design mockups and a frontend repository. Cannot be planned from the backend repository alone.
- **Performance benchmarking**: No baseline measurements available. Recommend establishing benchmarks as a separate effort.
