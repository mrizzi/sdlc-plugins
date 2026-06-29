# Impact Map — TC-9002: Improve search experience

## Ambiguities and Assumptions

The feature description for TC-9002 is underspecified in several critical areas. The following ambiguities were identified, and assumptions were made where necessary to produce a plannable scope. All assumptions are **pending clarification** from the feature owner.

### Ambiguity 1: No quantitative performance targets
**Feature says:** "Search should be faster" / "Currently too slow" / "Should be fast enough"
**What is missing:** There are no measurable latency targets, baseline measurements, or SLA definitions. "Too slow" and "fast enough" are subjective.
**Assumption (pending clarification):** We assume the goal is to add database indexing for full-text search columns and optimize the existing query path in `modules/search/src/service/mod.rs`. Without profiling data, we target the most common optimization patterns (indexes, query structure).

### Ambiguity 2: No definition of relevance ranking criteria
**Feature says:** "Results should be more relevant" / "Users complain about irrelevant results"
**What is missing:** There is no specification of what "relevant" means — no ranking algorithm, no weighting of fields (e.g., name vs. description), no examples of poor results, no user research data.
**Assumption (pending clarification):** We assume relevance means introducing weighted full-text search scoring using PostgreSQL `ts_rank` or similar, prioritizing name/title matches over description matches. The exact field weights need product owner input.

### Ambiguity 3: Filter dimensions unspecified
**Feature says:** "Add filters — Some kind of filtering capability"
**What is missing:** No specification of which fields to filter on, which entity types support filtering, what filter operators to support (exact match, range, multi-select), or how filters interact with each other.
**Assumption (pending clarification):** We assume filters for the primary entity types returned by search: entity type (SBOM, advisory, package), severity (for advisories), and date range. The filter implementation will reuse the existing query builder helpers in `common/src/db/query.rs`.

### Ambiguity 4: Search scope undefined
**Feature says:** "Make the search better"
**What is missing:** The feature does not specify which entity types the search covers. The current `modules/search/` module has a `SearchService` for full-text search across entities, but it is unclear whether improvements should target all entities equally or focus on specific ones.
**Assumption (pending clarification):** We assume improvements apply to the existing search service which covers SBOMs, advisories, and packages.

### Ambiguity 5: "Better UI" cannot be planned
**Feature says:** "Better UI — Make it look nicer" (marked Non-MVP)
**Assessment:** This is a non-MVP requirement with no design mockups, wireframes, or UI specifications. It targets a frontend that is not part of the trustify-backend repository. **This item cannot be planned without design mockups and a frontend repository.** It is excluded from this plan entirely.

### Ambiguity 6: No breaking change policy stated
**Feature says:** "Don't break existing functionality"
**What is missing:** No specification of whether API response shape changes are acceptable, whether new query parameters are additive-only, or whether existing search behavior must be preserved as a fallback.
**Assumption (pending clarification):** We assume all API changes must be backward-compatible — new query parameters are optional, response shapes add fields but do not remove or rename existing ones.

## Impacted Repository

| Repository | Impact |
|---|---|
| trustify-backend | Search service optimization, filter parameters, relevance scoring, database indexing |

## Impacted Modules

| Module | Files | Change Type |
|---|---|---|
| `modules/search/` | `service/mod.rs`, `endpoints/mod.rs` | Modify — add filter parameters, relevance scoring |
| `common/src/db/` | `query.rs` | Modify — extend query helpers with search-specific filters |
| `entity/` | `sbom.rs`, `advisory.rs`, `package.rs` | Modify — add or verify full-text search indexes |
| `migration/` | new migration file | Create — database migration for search indexes |
| `tests/api/` | `search.rs` | Modify — add integration tests for new search capabilities |

## Task Summary

| Task | Title | Dependency |
|---|---|---|
| Task 1 | Add database indexes for full-text search optimization | None |
| Task 2 | Implement relevance-scored search ranking | Task 1 |
| Task 3 | Add search filter parameters to the search endpoint | Task 2 |
| Task 4 | Add integration tests for search improvements | Task 3 |

## Out of Scope

- **Better UI** (non-MVP): Cannot be planned without design mockups and a frontend repository. This is a backend-only repository.
- **Performance benchmarking**: No baseline measurements are available. Recommend establishing benchmarks before and after as a separate effort.
