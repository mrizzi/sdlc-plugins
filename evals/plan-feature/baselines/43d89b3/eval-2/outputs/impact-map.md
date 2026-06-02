# Repository Impact Map — TC-9002: Improve Search Experience

## Ambiguities Identified

The feature description (TC-9002) contains several ambiguities that must be resolved
before a complete implementation plan can be finalized. The following ambiguities are
flagged for product owner clarification:

### Ambiguity 1: "Search should be faster" — No performance baseline or target defined

The requirement states search is "currently too slow" and should be "fast enough," but
provides no measurable performance criteria. There is no current latency baseline (e.g.,
p50/p95 response times), no target latency threshold (e.g., "results within 200ms"), and
no specification of which search operations are slow (full-text search, filtered queries,
or both).

**Assumption pending clarification:** We assume the goal is to optimize the existing
`SearchService` in `modules/search/src/service/mod.rs` by adding database indexes and
query optimization. A reasonable target is sub-500ms p95 response time for typical
queries. This assumption should be validated with the product owner.

### Ambiguity 2: "Results should be more relevant" — No relevance criteria defined

The requirement says users complain about "irrelevant results" but does not define what
constitutes relevance. There is no specification of ranking factors (recency, severity,
exact match vs fuzzy match), no indication of which entity types should be prioritized
(SBOMs, advisories, packages), and no examples of queries that return poor results.

**Assumption pending clarification:** We assume relevance improvements should include
implementing weighted full-text search ranking (prioritizing exact matches over partial
matches) and allowing results to be sorted by relevance score. The specific ranking
weights should be validated with the product owner.

### Ambiguity 3: "Add filters" — Filter types and fields not specified

The requirement says "some kind of filtering capability" without specifying which fields
should be filterable, what filter types are needed (dropdown, range, text, date), or
whether filters apply to the unified search endpoint or to individual entity list
endpoints.

**Assumption pending clarification:** We assume filters should be added to the unified
search endpoint (`GET /api/v2/search`) and should cover: entity type (SBOM, advisory,
package), severity (for advisories), and date range (for creation/modification dates).
The exact filter set should be validated with the product owner.

### Ambiguity 4: "Better UI" — Out of scope

The "Better UI" requirement is marked as non-MVP and cannot be planned without design
mockups or a frontend repository. The trustify-backend repository is a Rust backend
service with no frontend code. This requirement is **excluded from the current plan
scope** entirely. It should be revisited when a frontend repository is available and
Figma mockups have been provided.

### Ambiguity 5: Non-functional requirements are vague

"Should be fast enough" and "Don't break existing functionality" are not measurable.
There are no specific SLAs, no load/concurrency requirements, and no definition of what
"existing functionality" must be preserved beyond basic regression.

**Assumption pending clarification:** We assume standard regression testing (existing
integration tests in `tests/api/search.rs` must continue to pass) and that no specific
SLA beyond reasonable response times is required. The product owner should confirm whether
there are specific performance SLAs or load requirements.

---

## Impact Map

```
trustify-backend:
  changes:
    - Add database indexes to improve search query performance
    - Implement weighted full-text search ranking in SearchService for improved relevance
    - Add filter parameters (entity type, severity, date range) to the search endpoint
    - Update search endpoint to accept and apply filter query parameters
    - Add integration tests for search performance, relevance ranking, and filtering
```

## Workflow Mode

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators are present. Each change (indexing, relevance
ranking, filtering) can be merged independently without leaving `main` in a broken
state. The search endpoint already exists and each enhancement is additive — no
coordinated schema migrations, no breaking API changes (filters are additive query
parameters), and no cross-cutting refactors that span multiple tasks.
