# Repository Impact Map — TC-9002: Improve Search Experience

## Ambiguities and Assumptions

The feature description (TC-9002) is intentionally vague. The following ambiguities have been identified and must be clarified with the product owner before implementation begins. Where assumptions have been made to unblock planning, they are labeled as such.

### Ambiguity 1: "Search should be faster" — No performance baseline or target defined

The requirement states search is "currently too slow" and should be "fast enough," but provides no measurable performance criteria.

- What is the current p50/p95 latency for search queries?
- What is the target latency? (e.g., sub-200ms p95?)
- Is the bottleneck in the database query, full-text indexing, network, or application layer?

**Assumption (pending clarification):** The current search implementation in `modules/search/` performs unoptimized full-text queries against PostgreSQL. We assume the goal is to add proper full-text search indexing (e.g., PostgreSQL `tsvector`/GIN indexes) and optimize the query path in `SearchService`. Target latency is assumed to be under 500ms p95 for typical queries.

### Ambiguity 2: "Results should be more relevant" — No definition of relevance

The requirement says users complain about "irrelevant results" but does not define what constitutes a relevant result or how relevance should be measured.

- Which entity types should be searched (SBOMs only? Advisories? Packages? All)?
- Should results be ranked by relevance score?
- What ranking factors matter (recency, severity, text match quality)?
- Are there specific user complaints or examples of poor results to reference?

**Assumption (pending clarification):** We assume relevance means implementing proper full-text search ranking (e.g., PostgreSQL `ts_rank`) across SBOMs, advisories, and packages, with results ordered by relevance score. The current `SearchService` in `modules/search/src/service/mod.rs` likely uses basic `LIKE`/`ILIKE` queries without ranking.

### Ambiguity 3: "Add filters — some kind of filtering capability" — Filter criteria unspecified

The requirement asks for "some kind of filtering capability" without specifying:

- Which fields should be filterable (entity type, severity, date range, license, package name)?
- Should filters be combinable (AND/OR logic)?
- Should filters apply before or after text search?
- Are filters faceted (showing counts per filter value)?

**Assumption (pending clarification):** We assume the MVP filter set includes: entity type (SBOM, advisory, package), severity (for advisories), and date range (created/modified). Filters will be applied as query parameters on the search endpoint and combined with AND logic. Faceted counts are out of scope for MVP.

### Ambiguity 4: "Better UI" — Excluded from scope

The "Better UI" requirement is marked as non-MVP and cannot be planned without:

- Design mockups or Figma specifications
- A frontend repository to target (only `trustify-backend` is in scope)

**Decision:** "Better UI" is excluded from this implementation plan entirely. It should be planned separately once design assets and a frontend repository are available.

### Ambiguity 5: Non-functional requirements lack specificity

"Should be fast enough" and "Don't break existing functionality" are not measurable acceptance criteria.

**Assumption (pending clarification):** "Fast enough" is interpreted as the performance target in Ambiguity 1. "Don't break existing functionality" is interpreted as requiring backward-compatible API changes (existing search endpoint behavior must be preserved when no new parameters are supplied) and passing all existing integration tests.

---

## Impact Map

```
trustify-backend:
  changes:
    - Add database migration for full-text search indexes (tsvector columns and GIN indexes on searchable entity fields)
    - Optimize SearchService to use PostgreSQL full-text search with ts_rank relevance scoring
    - Add filter parameters (entity type, severity, date range) to the search endpoint
    - Update search endpoint to accept and apply filter query parameters
    - Update common query builder to support full-text search and filter predicates
    - Add integration tests for improved search performance, relevance ranking, and filtering
```
