# Impact Map — TC-9002: Improve Search Experience

## Feature Summary

Improve the search experience in the trustify-backend platform by making search faster, returning more relevant results, and adding filtering capabilities.

## Ambiguities Identified

The feature description (TC-9002) contains several ambiguities that must be clarified before or during implementation. These are flagged below and referenced in individual task descriptions.

| # | Ambiguity | Impact | Recommendation |
|---|-----------|--------|----------------|
| A1 | **"Search should be faster" — no performance target defined.** The feature says "currently too slow" and the NFR says "should be fast enough" but provides no latency target (e.g., p95 < 200ms), no baseline measurement, and no benchmark methodology. | Cannot objectively verify the acceptance criterion without a measurable target. | Clarify with product: define a target latency (e.g., p95 response time < 500ms for typical queries) and establish a baseline measurement of current performance. Tasks assume a goal of measurable improvement over the current baseline, pending clarification. |
| A2 | **"Results should be more relevant" — no definition of relevance.** There is no specification of what "relevant" means: no ranking algorithm guidance, no example queries with expected results, no user research on what "irrelevant results" look like. | Cannot design a relevance improvement without understanding what is wrong with current ranking. | Clarify with product: provide example queries that return poor results today and the expected ordering. Tasks assume basic improvements (weighted field scoring, exact-match boosting) pending clarification. |
| A3 | **"Add filters — some kind of filtering capability" — filter dimensions unspecified.** The feature does not specify which fields should be filterable, what filter types are needed (exact match, range, multi-select), or whether filters combine with AND/OR logic. | Cannot implement filters without knowing the filter schema. | Clarify with product: enumerate the filterable fields and filter types. Tasks assume filters on entity type, severity (for advisories), and date range, as these are fields visible in the existing entity models. This is an assumption pending clarification. |
| A4 | **"Don't break existing functionality" — no regression test baseline.** The NFR is vague about what "existing functionality" is protected. There is no mention of backwards compatibility requirements for the search API contract. | Risk of breaking API consumers if response shape changes. | Tasks assume the existing `GET /api/v2/search` endpoint contract is preserved and any new parameters are additive (optional query parameters). |
| A5 | **Search scope undefined.** The feature does not specify which entities should be searchable. The current `SearchService` performs "full-text search across entities" but it is unclear if all entities (SBOMs, advisories, packages) are in scope or only a subset. | Could lead to over- or under-engineering the solution. | Tasks assume all three entity types (SBOM, advisory, package) remain in scope, consistent with the existing search module. |

## Out-of-Scope Items

| Item | Reason |
|------|--------|
| **Better UI (non-MVP)** | Explicitly marked as non-MVP in the feature requirements. Additionally, the trustify-backend repository is a Rust backend service with no frontend code. UI improvements require design mockups and a frontend repository, neither of which are available. This item is excluded from the plan entirely. |

## Assumptions

These assumptions are made to allow planning to proceed. They are documented as **pending clarification** and should be validated with the product owner before implementation begins.

1. **Performance target**: "Faster" means measurable improvement in p95 latency over the current baseline, verified by benchmark tests. No specific SLA is assumed.
2. **Relevance improvements**: Weighted full-text search scoring (boosting title/name fields over description/body fields) is the intended approach. More sophisticated relevance (e.g., ML-based ranking, user behavior signals) is out of scope for MVP.
3. **Filter fields**: Filters will cover entity type, severity (advisories), and date range as these map to existing entity model fields (`entity/src/advisory.rs`, `entity/src/sbom.rs`).
4. **API compatibility**: The `GET /api/v2/search` endpoint remains backwards compatible. New filter parameters are optional query parameters.
5. **Search scope**: All three entity types (SBOM, advisory, package) remain searchable.

## Repositories Impacted

| Repository | Impact |
|------------|--------|
| trustify-backend | All changes — search module, common query utilities, entity layer, integration tests |

## Change Summary

### trustify-backend

| Area | Files | Change Type | Task |
|------|-------|-------------|------|
| Search service | `modules/search/src/service/mod.rs` | Modify — optimize query execution and add weighted scoring | Task 1, Task 2 |
| Search endpoints | `modules/search/src/endpoints/mod.rs` | Modify — accept filter query parameters | Task 3 |
| Search module root | `modules/search/src/lib.rs` | Modify — re-export new filter types | Task 3 |
| Common query helpers | `common/src/db/query.rs` | Modify — add search-specific query optimizations and filter combinators | Task 1, Task 3 |
| Common model | `common/src/model/paginated.rs` | Potentially modify — add search metadata (e.g., score) to response | Task 2 |
| Migration | `migration/src/` | New migration — add database indexes for search performance | Task 1 |
| Search tests | `tests/api/search.rs` | Modify — add tests for performance, relevance, and filters | Task 4 |

## Task Breakdown

| Task | Title | Repository | Depends On |
|------|-------|------------|------------|
| Task 1 | Optimize search query performance | trustify-backend | — |
| Task 2 | Improve search result relevance with weighted scoring | trustify-backend | Task 1 |
| Task 3 | Add filter parameters to search endpoint | trustify-backend | Task 1 |
| Task 4 | Add integration tests for search improvements | trustify-backend | Task 2, Task 3 |
