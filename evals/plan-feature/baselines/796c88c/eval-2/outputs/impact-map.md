# Impact Map: TC-9002 — Improve Search Experience

## Feature Summary

TC-9002 requests improvements to the search experience across several dimensions: performance, relevance, filtering, and UI. The feature description is intentionally broad, stating goals like "make the search better" and "should be faster" without specifying measurable targets or detailed requirements.

## Identified Ambiguities

The following ambiguities were identified in the feature description and MUST be resolved with the product owner before implementation can be considered complete:

1. **"Search should be faster" — No performance target defined.** The requirement says search is "currently too slow" but provides no baseline metrics (current p50/p95 latency) and no target metrics (e.g., "search should return results in under 200ms"). Without measurable targets, there is no way to validate whether the improvement is sufficient.

2. **"Results should be more relevant" — No definition of relevance.** The feature says users complain about "irrelevant results" but does not define what constitutes a relevant result. Is this about ranking order, missing results, false positives, or all three? Are there specific search queries that produce poor results today? Without examples or a relevance definition, improvements are speculative.

3. **"Add filters" — Filter types not specified.** The requirement says "some kind of filtering capability" but does not specify which fields should be filterable. Candidates include: entity type (SBOM, advisory, package), severity, date range, license type, package name. The plan assumes a reasonable set of filters based on existing entity fields, but this is an assumption pending clarification.

4. **"Better UI" — No design specifications.** The feature lists "Make it look nicer" as a non-MVP requirement. There are no mockups, wireframes, or design specifications. Additionally, the target repository (trustify-backend) is a backend service — UI improvements would require a frontend repository that is not in scope.

5. **"Should be fast enough" (non-functional requirement) — No quantitative threshold.** This repeats the performance ambiguity in vaguer terms. "Fast enough" is not a testable criterion.

6. **"Don't break existing functionality" — No regression test baseline mentioned.** While this is a reasonable constraint, there is no mention of what existing search behavior must be preserved or what the current test coverage looks like.

## Scope Decision

### In Scope (MVP — Backend)

The following can be planned against the `trustify-backend` repository with reasonable assumptions:

| Task | Rationale |
|------|-----------|
| Add PostgreSQL full-text search indexing | Addresses "faster" and "more relevant" by replacing naive LIKE/ILIKE queries with GIN-indexed tsvector search |
| Improve search result ranking and relevance | Addresses "more relevant" by implementing ts_rank scoring and result ordering |
| Add filter parameters to search endpoint | Addresses "add filters" by extending the search API with query parameters for entity type, severity, and date range |

### Out of Scope

| Requirement | Reason |
|-------------|--------|
| Better UI | Non-MVP. No design mockups or frontend repository available. Cannot be planned without design specifications and access to the frontend codebase. |
| Performance benchmarking | No baseline or target metrics provided. Tasks include basic indexing improvements, but validating "fast enough" requires defined SLAs from the product owner. |

## Impacted Components

### Repository: trustify-backend

| Component | Path | Impact |
|-----------|------|--------|
| Search service | `modules/search/src/service/mod.rs` | Modify to use full-text search queries with ts_rank scoring |
| Search endpoints | `modules/search/src/endpoints/mod.rs` | Modify to accept filter query parameters |
| Database migrations | `migration/src/` | New migration for GIN index and tsvector columns |
| Query helpers | `common/src/db/query.rs` | Extend with full-text search and filter helpers |
| Search integration tests | `tests/api/search.rs` | Extend with tests for new search and filter behavior |
| Entity definitions | `entity/src/sbom.rs`, `entity/src/advisory.rs`, `entity/src/package.rs` | May need tsvector column mappings |

## Task Dependency Graph

```
Task 1: Database migration for full-text search indexes
  |
  v
Task 2: Full-text search service with relevance ranking
  |
  v
Task 3: Filter parameters for search endpoint
```

Tasks 2 and 3 both depend on Task 1 (the migration). Task 3 can be developed in parallel with Task 2 but should be merged after Task 2 for cleaner integration.

## Assumptions Pending Clarification

- **A1**: Full-text search should cover SBOM names/descriptions, advisory titles/descriptions, and package names. (Pending: confirmation of which fields to index.)
- **A2**: Filter dimensions are: entity type, advisory severity, and date range. (Pending: confirmation of which filters are needed.)
- **A3**: Relevance ranking uses PostgreSQL ts_rank with default weights. (Pending: whether custom weighting or external search engines like Elasticsearch are desired.)
- **A4**: Performance improvement from GIN indexes is sufficient to address "faster" without introducing caching or external search infrastructure. (Pending: performance targets.)
