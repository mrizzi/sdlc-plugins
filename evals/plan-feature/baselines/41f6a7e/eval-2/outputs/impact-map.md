# Repository Impact Map -- TC-9002: Improve search experience

## Repository: trustify-backend

### Summary

Improve the search experience by adding full-text search indexing, relevance ranking, filtering capabilities, and response caching. All changes are scoped to the trustify-backend repository and can be merged independently to main.

### Impacted Areas

#### Database / Migrations

| File | Change Type | Description |
|---|---|---|
| `migration/src/m0002_search_indexes/mod.rs` | Create | New migration adding PostgreSQL GIN indexes with tsvector columns on searchable fields (SBOM name/description, advisory title/description, package name) |
| `migration/src/lib.rs` | Modify | Register the new search index migration in the migration runner |

#### Search Module

| File | Change Type | Description |
|---|---|---|
| `modules/search/src/service/mod.rs` | Modify | Replace LIKE/ILIKE queries with tsvector/tsquery full-text search; add ts_rank relevance scoring; add filter application logic; optimize query construction |
| `modules/search/src/endpoints/mod.rs` | Modify | Add filter query parameters to GET /api/v2/search; add cache-control headers; wire filter/sort-by-relevance into service calls |
| `modules/search/src/model/mod.rs` | Create | SearchFilter struct defining available filter parameters (entity type, date range, severity, license) |

#### Common / Shared

| File | Change Type | Description |
|---|---|---|
| `common/src/db/query.rs` | Reuse | Existing filtering, pagination, and sorting helpers -- extend if needed for full-text search rank ordering |
| `common/src/model/paginated.rs` | Reuse | PaginatedResults<T> response wrapper -- no changes expected |
| `common/src/error.rs` | Reuse | AppError enum -- no changes expected |

#### Entity Definitions

| File | Change Type | Description |
|---|---|---|
| `entity/src/sbom.rs` | Reuse | SeaORM entity for SBOM -- referenced by search indexing migration |
| `entity/src/advisory.rs` | Reuse | SeaORM entity for advisory -- referenced by search indexing migration |
| `entity/src/package.rs` | Reuse | SeaORM entity for package -- referenced by search indexing migration |

#### Tests

| File | Change Type | Description |
|---|---|---|
| `tests/api/search.rs` | Modify | Expand integration tests to cover relevance ranking, filter combinations, caching behavior, and performance baselines |

#### Server

| File | Change Type | Description |
|---|---|---|
| `server/src/main.rs` | Reuse | Axum server setup and route mounting -- may need minor changes if caching middleware is configured per-route |

### Workflow Mode

**Direct-to-main.** Each task produces an independently mergeable increment. No coordinated branch required.

### Task Dependency Graph

```
Task 1: Search indexes (migration)
  |
  v
Task 2: Relevance ranking (depends on Task 1 indexes)
  |
  v
Task 3: Filter parameters (independent of Task 2, depends on Task 1)
  |
  v
Task 4: Caching and query optimization (independent, can follow any order after Task 1)
  |
  v
Task 5: Integration tests (depends on Tasks 1-4)
```

Tasks 2, 3, and 4 all depend on Task 1 (the indexes must exist) but are independent of each other. Task 5 depends on all prior tasks being complete.

### Risk Notes

- The migration (Task 1) adds GIN indexes which can be expensive on large tables. The migration should use `CREATE INDEX CONCURRENTLY` where possible.
- Full-text search configuration (language, stop words) should default to `english` but be documented for future customization.
- Cache TTL values need tuning based on data change frequency; start conservative (short TTL) and adjust.
