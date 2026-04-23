# Impact Map — TC-9002: Improve Search Experience

## Feature Summary

Improve the platform's search capability so that results are returned faster and are more relevant to user queries, with basic filtering support.

---

## Ambiguities Flagged

The feature description (TC-9002) is intentionally vague. The following ambiguities must be resolved before or during implementation. Tasks carry assumptions labeled "assumption pending clarification" where the description does not provide enough detail to proceed definitively.

### Ambiguity 1 — What does "faster" mean?

The requirement states "search should be faster / currently too slow" but provides no baseline latency measurement and no target SLA. Without a concrete performance target it is impossible to evaluate whether any implementation satisfies this requirement.

**Assumption pending clarification**: Target p95 response time for a search query is <= 500 ms against a dataset of 10,000 SBOMs/advisories. Database indexes and query optimization will be the primary levers; caching will be added if indexes alone are insufficient.

### Ambiguity 2 — What does "more relevant results" mean?

"Relevance" is undefined. The feature does not specify:
- Whether full-text ranking (e.g. PostgreSQL `ts_rank`) should replace or augment the existing search
- Whether relevance is purely textual or incorporates domain-specific signals (e.g. severity for advisories, recency for SBOMs)
- Which entity fields are included in search (name, description, CVE ID, package version, etc.)

**Assumption pending clarification**: Relevance will be implemented as PostgreSQL full-text search (`tsvector`/`tsquery`) with `ts_rank` ordering, applied across the `name` and `description` columns of the SBOM, advisory, and package entities. Domain-specific signals are out of scope until specified.

### Ambiguity 3 — What does "Add filters" mean?

"Some kind of filtering capability" is entirely unspecified:
- Which entity types can be filtered (SBOMs, advisories, packages, or all)?
- Which fields are filterable (severity, date range, license, status)?
- What filter UI contract is needed (does the frontend expect specific query parameter names)?
- Are filters additive (AND) or substitutive (OR)?

**Assumption pending clarification**: Filters will be added as optional query parameters to the existing `GET /api/v2/search` endpoint. Initial filterable fields: `severity` (advisory), `license` (package). Filters are additive (AND logic). Parameter names: `?severity=<value>&license=<value>`. No frontend contract changes are assumed because no frontend repository is in scope.

### Ambiguity 4 — Which search entities are in scope?

The feature says "make the search better" across the platform but does not specify whether all entity types (SBOM, advisory, package) are in scope or only a subset. The existing `modules/search/` module performs full-text search across entities but the scope of improvement is unclear.

**Assumption pending clarification**: All three entity types (SBOM, advisory, package) are in scope for both performance and relevance improvements.

---

## Out of Scope

### "Better UI" (non-MVP)

The feature table marks "Better UI / Make it look nicer" as non-MVP. This item cannot be planned because:

1. No design mockups or Figma links are provided.
2. No frontend repository is included in scope or referenced in the repository structure.
3. UI changes require a defined design contract before any meaningful task decomposition.

**This item is excluded from all tasks.** It should be re-introduced as a separate feature once design artifacts are available and the frontend repository is in scope.

---

## Goals and Actors

| Goal | Actor | Mechanism |
|---|---|---|
| Reduce search response latency | All platform users | PostgreSQL indexes on searchable columns; query optimization in `SearchService` |
| Improve result relevance | All platform users | Full-text search with `tsvector`/`tsquery` and `ts_rank` ranking |
| Enable result filtering | All platform users | Optional query parameters on `GET /api/v2/search`; filter logic in `SearchService` |

---

## Implementation Scope

The following MVP tasks are planned. All work is in the `trustify-backend` repository.

| Task | Title | Key Files |
|---|---|---|
| 1 | Add full-text search indexes via database migration | `migration/src/`, `entity/src/` |
| 2 | Refactor SearchService to use ranked full-text search | `modules/search/src/service/mod.rs` |
| 3 | Add filter query parameters to the search endpoint | `modules/search/src/endpoints/mod.rs`, `common/src/db/query.rs` |
| 4 | Integration tests for improved search behavior | `tests/api/search.rs` |

---

## Dependencies Between Tasks

```
Task 1 (migration + indexes)
  └─> Task 2 (SearchService uses new tsvector columns)
        └─> Task 3 (filter params added to endpoint and service)
              └─> Task 4 (integration tests cover all new behavior)
```

Tasks 2, 3, and 4 depend on the database schema produced by Task 1. Task 4 depends on Tasks 2 and 3 being complete so all new behaviors can be tested together.
