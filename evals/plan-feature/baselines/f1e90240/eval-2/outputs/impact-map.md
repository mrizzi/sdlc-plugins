# Impact Map: TC-9002 -- Improve Search Experience

## Feature Summary

Improve the search experience in the trustify-backend platform by optimizing search performance, improving result relevance, and adding filtering capabilities.

## Scope Decision

**Included (MVP):**
- Search performance optimization (Task 1)
- Search relevance improvements (Task 2)
- Search filters (Task 3)

**Excluded from scope:**
- **"Better UI" (non-MVP)** -- Cannot be planned without design mockups or a frontend repository. The trustify-backend repository contains only the REST API backend. UI improvements require a frontend repository (not provided) and design specifications (not provided). This requirement is excluded entirely from the implementation plan.

**No documentation task generated** -- The feature description does not include a "Documentation Considerations" section.

**No testing tasks generated** -- No testing readiness template (`docs/testing-readiness.md`) exists in the target repository.

## Workflow Mode

**direct-to-main** -- Single repository (trustify-backend), all tasks target `main`.

## Ambiguities Identified

The feature description (TC-9002) is intentionally vague in several areas. The following ambiguities were identified and handled with documented assumptions:

### Ambiguity 1: No Performance Baseline or Target

**What's missing:** The feature states search is "currently too slow" and the non-functional requirement says "should be fast enough," but no current latency measurements, target response times, or performance benchmarks are provided.

**Assumption (pending clarification):** Task 1 assumes a target of sub-500ms p95 response time for typical search queries. Stakeholders should provide actual performance baselines and targets before implementation begins.

### Ambiguity 2: No Definition of "Relevant" Results

**What's missing:** The feature states "results should be more relevant" and "users complain about irrelevant results," but provides no definition of relevance, no examples of bad results, and no ranking criteria.

**Assumption (pending clarification):** Task 2 assumes relevance means: (1) exact matches ranked above partial matches, (2) name/title field matches ranked above description/body field matches, (3) results ordered by computed relevance score. These criteria need stakeholder validation.

### Ambiguity 3: Filter Types and Fields Are Unspecified

**What's missing:** The feature requires "some kind of filtering capability" but does not specify which fields should be filterable, what filter operators to support, or how filters interact with search.

**Assumption (pending clarification):** Task 3 assumes an initial filter set of entity_type, severity, date range, and license filters with AND combination logic. Stakeholders should confirm the required filter set before implementation.

### Ambiguity 4: Scope of "Search" Is Undefined

**What's missing:** The feature does not specify whether "search" refers to the dedicated `/api/v2/search` endpoint, the list endpoints on individual entity modules (`/api/v2/sbom`, `/api/v2/advisory`, `/api/v2/package`), or both.

**Assumption (pending clarification):** All tasks target the dedicated `SearchService` and `/api/v2/search` endpoint in the `modules/search/` module, as it is the purpose-built search module. Per-entity list endpoint improvements are out of scope for this feature.

### Ambiguity 5: Non-Functional Requirements Lack Quantitative Measures

**What's missing:** The NFRs state "should be fast enough" and "don't break existing functionality" without quantitative measures, regression test baselines, or SLA definitions.

**Assumption (pending clarification):** These are interpreted as: maintain sub-500ms p95 latency (Task 1 target) and ensure all existing integration tests in `tests/api/search.rs` continue to pass.

## Task Dependency Graph

```
Task 1: Optimize search performance
  |
  v
Task 2: Improve search relevance (depends on Task 1)
  |
  v
Task 3: Add search filters (depends on Task 1, Task 2)
```

Task 1 is the foundation -- it introduces search indexes and query optimizations. Task 2 builds on those indexes to add relevance scoring. Task 3 extends the search service with filters that work alongside both performance optimizations and relevance ranking.

## Impacted Files

| File | Task(s) | Change Type |
|---|---|---|
| `modules/search/src/service/mod.rs` | 1, 2, 3 | Modify |
| `modules/search/src/endpoints/mod.rs` | 2, 3 | Modify |
| `common/src/db/query.rs` | 1, 3 | Modify |
| `common/src/db/limiter.rs` | 1 | Modify |
| `migration/src/m0002_search_indexes/mod.rs` | 1 | Create |
| `tests/api/search.rs` | 1, 2, 3 | Modify |

## Field Inheritance

- **Priority:** Normal (inherited from TC-9002 to all tasks)
- **Fix Versions:** RHTPA 1.6.0 (inherited from TC-9002 to all tasks)
