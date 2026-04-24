# Impact Map: TC-9002 — Improve Search Experience

## Feature Summary

Improve the search experience in the trustify-backend platform by making search faster, more relevant, and adding filtering capabilities.

## Ambiguities and Open Questions

The feature description TC-9002 contains significant ambiguities that must be resolved with the product owner before implementation begins. The following items are flagged for clarification:

1. **No performance baseline or target latency defined.** The requirement states search should be "faster" and "fast enough," but provides no current latency measurements, no target SLA (e.g., p95 < 200ms), and no benchmark methodology. Without concrete targets, it is impossible to verify that performance improvements meet expectations.

2. **"More relevant results" is undefined.** There is no specification of what constitutes relevance — no ranking algorithm requirements, no weighting criteria (e.g., recency, severity, exact vs. fuzzy match), and no examples of searches that currently return poor results. Relevance is subjective without a scoring model.

3. **"Add filters" lacks specificity.** The requirement does not specify which entity fields should be filterable, what filter operators are needed (equality, range, multi-select, date range), or whether filters apply to the unified search endpoint (`/api/v2/search`) or to individual entity list endpoints (`/api/v2/sbom`, `/api/v2/advisory`, `/api/v2/package`), or both.

4. **No performance SLA for non-functional requirements.** "Should be fast enough" is not a measurable criterion. Need concrete thresholds (e.g., response time, throughput under load, maximum acceptable query plan cost).

5. **Scope of "search" is ambiguous.** It is unclear whether the improvements target the dedicated search module (`modules/search/`) for cross-entity full-text search, the individual list endpoints that already support filtering via `common/src/db/query.rs`, or both.

6. **No indication of indexing strategy.** If full-text search performance is the concern, the feature does not specify whether PostgreSQL full-text search (tsvector/tsquery), a dedicated search engine (Elasticsearch, Meilisearch), or query optimization alone is expected.

7. **"Better UI" requirement has no frontend repository or design mockups.** This is marked non-MVP and cannot be planned — there is no frontend repository in scope and no design specifications. This requirement is **excluded from this plan**.

## Scope Decisions

- **In scope**: Backend search performance improvements, search relevance improvements, and adding filter parameters to search/list endpoints — all within the `trustify-backend` repository.
- **Out of scope**: "Better UI" (non-MVP, no frontend repository or design mockups available).

## Impacted Repository: trustify-backend

### Module: `modules/search/`
| Area | Files | Change Type | Notes |
|---|---|---|---|
| Search service | `modules/search/src/service/mod.rs` | MODIFY | Optimize query execution, add relevance scoring, add filter parameter support |
| Search endpoint | `modules/search/src/endpoints/mod.rs` | MODIFY | Accept new filter query parameters, return relevance-scored results |
| Search tests | `tests/api/search.rs` | MODIFY | Add tests for filters, relevance, and performance |

### Module: `common/`
| Area | Files | Change Type | Notes |
|---|---|---|---|
| Query helpers | `common/src/db/query.rs` | MODIFY | Extend shared query builder with new filter types and full-text search ranking support |
| Paginated model | `common/src/model/paginated.rs` | MODIFY (potentially) | May need to add a relevance score field to paginated results |

### Module: `entity/`
| Area | Files | Change Type | Notes |
|---|---|---|---|
| Entity definitions | `entity/src/sbom.rs`, `entity/src/advisory.rs`, `entity/src/package.rs` | MODIFY (potentially) | May need to add or update indexes for search performance |

### Module: `migration/`
| Area | Files | Change Type | Notes |
|---|---|---|---|
| Database migration | `migration/src/` | CREATE | New migration to add full-text search indexes (GIN indexes on tsvector columns) if PostgreSQL full-text search is chosen |

### Module: `modules/fundamental/`
| Area | Files | Change Type | Notes |
|---|---|---|---|
| List endpoints | `modules/fundamental/src/sbom/endpoints/list.rs`, `modules/fundamental/src/advisory/endpoints/list.rs`, `modules/fundamental/src/package/endpoints/list.rs` | MODIFY (potentially) | Add filter query parameters if filtering applies to individual list endpoints |

## Task Breakdown

| Task | Title | Dependency |
|---|---|---|
| 1 | Add database indexes and full-text search migration | None |
| 2 | Extend query builder with filter and relevance support | Task 1 |
| 3 | Improve SearchService with relevance scoring and filters | Task 2 |
| 4 | Update search endpoint to expose filters and relevance | Task 3 |
| 5 | Add integration tests for search improvements | Task 4 |
