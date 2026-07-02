# Impact Map: TC-9002 -- Improve Search Experience

## Feature Summary
Improve the search experience in trustify-backend by making search faster, more relevant, and adding filtering capabilities.

## Scope

### In Scope (MVP)
| Requirement | Task | Impact |
|---|---|---|
| Search should be faster | Task 1: Search performance indexes | Database indexes + query optimization in `modules/search/` |
| Results should be more relevant | Task 2: Search relevance ranking | ts_rank scoring in SearchService, sort parameter on endpoint |
| Add filters | Task 3: Search filters | Type, date range, severity query parameters on `GET /api/v2/search` |

### Out of Scope
| Requirement | Reason |
|---|---|
| Better UI (non-MVP) | Cannot be planned without design mockups or a frontend repository. The trustify-backend repository contains only the REST API layer. UI improvements require a separate frontend feature specification with mockups, component designs, and a frontend repository to target. Excluded from this plan. |

## Ambiguities

The feature description TC-9002 is underspecified in several critical areas. The following ambiguities were identified and must be clarified with the product owner before or during implementation:

### Ambiguity 1: No quantitative performance targets
**Feature text:** "Search should be faster" / "Currently too slow" / "Should be fast enough"
**What is missing:** No baseline metrics (current p50/p95 latency, current throughput), no target metrics (target latency, acceptable response time SLA), no load profile (concurrent users, query volume).
**Impact:** Without targets, there is no objective definition of "done" for performance. The implementation adds structural improvements (indexes, query optimization) but cannot be validated against a specific performance bar.
**Assumption (pending clarification):** Performance success is defined as search queries using index scans rather than sequential scans, which provides measurable improvement regardless of the specific target.

### Ambiguity 2: Undefined relevance criteria
**Feature text:** "Results should be more relevant" / "Users complain about irrelevant results"
**What is missing:** No definition of what makes a result "relevant." No ranking algorithm specified. No indication whether relevance means text-match quality alone, or should incorporate domain signals (advisory severity, SBOM recency, package popularity, user context).
**Impact:** Different relevance definitions lead to fundamentally different implementations (text ranking vs. domain-weighted scoring vs. personalized ranking).
**Assumption (pending clarification):** Relevance is implemented as PostgreSQL full-text search ranking (ts_rank) based on text-match quality. Domain-specific boosting factors would require a follow-up specification.

### Ambiguity 3: Unspecified filter set
**Feature text:** "Add filters -- Some kind of filtering capability"
**What is missing:** No specification of which attributes should be filterable, whether filters support multi-select or single-select, whether filters combine with AND or OR semantics, whether filter values should be free-text or constrained enums, and how filters interact with relevance ranking.
**Impact:** Filter design directly affects API contract, query complexity, and UX. Under-specifying filters risks building the wrong filter set or needing breaking API changes later.
**Assumption (pending clarification):** Filters include entity type (sbom/advisory/package), date range (from/to), and severity (for advisories). Filters combine with AND semantics. These are based on the existing data model fields visible in the entity definitions.

### Ambiguity 4: No regression test criteria
**Feature text:** "Don't break existing functionality"
**What is missing:** No definition of what "existing functionality" encompasses, no list of critical user flows that must be preserved, no acceptance test suite referenced.
**Impact:** Without explicit regression criteria, "don't break anything" is unverifiable.
**Assumption (pending clarification):** Existing integration tests in `tests/api/search.rs` serve as the regression baseline. All existing tests must continue to pass after changes.

### Ambiguity 5: No search scope definition
**Feature text:** "Make the search better"
**What is missing:** No specification of which entities the search covers (all entities vs. specific ones), whether search should span across entity types or be entity-specific, whether search covers metadata fields only or also ingested document content.
**Impact:** The scope of search directly affects index design, query complexity, and response format.
**Assumption (pending clarification):** Search scope matches the current SearchService implementation in `modules/search/src/service/mod.rs`, which performs full-text search across SBOM, advisory, and package entities.

## File Impact Analysis

### Files Modified
| File | Tasks | Change Type |
|---|---|---|
| `modules/search/src/service/mod.rs` | 1, 2, 3 | Optimize queries, add ranking, add filter logic |
| `modules/search/src/endpoints/mod.rs` | 2, 3 | Add sort and filter query parameters |
| `migration/src/lib.rs` | 1 | Register new migration module |
| `common/src/db/query.rs` | 3 | Extend shared query helpers with filter predicates (if needed) |

### Files Created
| File | Task | Purpose |
|---|---|---|
| `migration/src/m0002_search_indexes/mod.rs` | 1 | GIN indexes on searchable text columns |

### Files Not Impacted
| File | Reason |
|---|---|
| `entity/src/*.rs` | Entity definitions are read for column references but not modified |
| `server/src/main.rs` | No new modules added; search endpoint already registered |
| `modules/fundamental/` | Fundamental module endpoints are not modified; used as reference patterns only |
| `modules/ingestor/` | Ingestion pipeline is not affected by search improvements |

## Task Dependency Graph

```
Task 1: Search Performance Indexes (no dependencies)
   |
   +---> Task 2: Search Relevance Ranking (depends on Task 1)
   |
   +---> Task 3: Search Filters (depends on Task 1)
```

Tasks 2 and 3 depend on Task 1 (full-text index infrastructure) but are independent of each other and can be implemented in parallel after Task 1 is complete.

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Performance targets undefined -- implementation may not satisfy stakeholder expectations | High | Medium | Document assumptions; request quantitative targets before closing the feature |
| Relevance ranking algorithm may not match user expectations of "relevant" | Medium | High | Start with ts_rank; gather user feedback; iterate on ranking formula |
| Filter set may be incomplete or wrong | Medium | Medium | Implement extensible filter infrastructure; additional filters can be added without breaking changes |
| Migration on production data may lock tables | Low | High | Test migration against production-sized dataset; use CONCURRENTLY for index creation if supported |
