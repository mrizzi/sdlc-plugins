# Repository Impact Map — TC-9002: Improve search experience

## Ambiguities Identified

The following ambiguities were flagged in the feature description. These represent gaps that should be clarified with the product owner before implementation. Tasks below document assumptions where details were filled in, labeled as **assumptions pending clarification**.

1. **"Search should be faster" — no quantitative performance target.** The description says search is "currently too slow" and should be "fast enough," but provides no latency targets (e.g., p50 < 200ms, p95 < 500ms), no baseline measurements, and no load/concurrency requirements. **Assumption pending clarification:** we will target measurable improvements via query optimization and indexing, and add benchmarks so performance can be quantified.

2. **"Results should be more relevant" — no definition of relevance.** There is no specification of what makes results "relevant" vs "irrelevant": no ranking algorithm, no scoring criteria, no examples of bad vs good results, no indication of which fields should be weighted more heavily. **Assumption pending clarification:** we will improve relevance by implementing PostgreSQL full-text search ranking (ts_rank) and weighting title/name fields more heavily than body/description fields.

3. **"Add filters" — filter fields and types unspecified.** The description says "some kind of filtering capability" but does not specify which entity fields should be filterable, what filter types to support (exact match, substring, range, multi-select), or which search entities the filters apply to. **Assumption pending clarification:** we will add filtering by entity type (SBOM, advisory, package) and by key fields (severity for advisories, license for packages), leveraging the existing query builder helpers in `common/src/db/query.rs`.

4. **"Better UI" — excluded from scope.** This is marked as non-MVP, no design mockups or Figma links were provided, and the only repository in scope is `trustify-backend` (a Rust backend service). There is no frontend repository in the Repository Registry. This requirement **cannot be planned** without design mockups and a frontend repository, and is excluded from this implementation plan.

5. **Non-functional requirements lack quantitative targets.** "Should be fast enough" provides no measurable criteria. "Don't break existing functionality" is a standard expectation but defines no regression test baseline. **Assumption pending clarification:** we will add integration tests and verification commands to establish a measurable baseline.

## Workflow Mode

**Mode:** `direct-to-main`

**Rationale:** No atomicity indicators are present. The three planned changes (search performance optimization, search relevance improvements, filter support) are independently deployable. Each task can be merged to `main` without breaking existing functionality or depending on the others being present. No coordinated schema migrations, breaking API changes, cross-cutting refactors, or tightly coupled components span multiple tasks.

## Impact Map

```
trustify-backend:
  changes:
    - Optimize search query performance with database indexing and query improvements in the search module
    - Implement full-text search ranking for improved result relevance in SearchService
    - Add filtering parameters (entity type, severity, license) to the search endpoint
    - Add integration tests for search performance, relevance ranking, and filtering
```
