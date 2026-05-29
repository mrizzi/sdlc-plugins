# Repository Impact Map — TC-9002: Improve search experience

## Ambiguities Identified

The feature description TC-9002 contains several critical ambiguities that must be resolved before implementation can proceed with full confidence. The plan below documents assumptions where details are missing and flags items requiring product owner clarification.

### Ambiguity 1: No performance targets for "Search should be faster"

The requirement states search is "currently too slow" and should be "fast enough," but provides no measurable targets. There is no baseline latency measurement, no target response time (e.g., p95 < 200ms), and no definition of the dataset size under which the target should hold.

**Assumption (pending clarification):** We assume the goal is to add database indexing for full-text search columns and optimize the query path in `SearchService` to reduce response time. A follow-up conversation with the product owner should establish concrete latency SLAs (e.g., p95 < 500ms for 100k records).

### Ambiguity 2: No definition of "more relevant" results

The requirement says "users complain about irrelevant results" but does not define what relevance means. There is no ranking algorithm specified, no indication of which fields should be weighted more heavily, and no examples of "good" vs "bad" search results.

**Assumption (pending clarification):** We assume relevance improvement means implementing PostgreSQL full-text search with `ts_vector`/`ts_query` (or equivalent SeaORM constructs) with weighted ranking across entity fields (e.g., name/title weighted higher than description). The product owner should provide examples of searches that currently return poor results and define expected ranking behavior.

### Ambiguity 3: "Add filters" lacks specification

The requirement says "some kind of filtering capability" but does not specify which fields should be filterable, what filter types are needed (exact match, range, multi-select), or whether filters should be combinable (AND/OR logic).

**Assumption (pending clarification):** Based on the existing entity structure, we assume filters for: entity type (SBOM, Advisory, Package), severity (for advisories), and date range. The product owner should confirm the filter set and specify whether filters are AND-combined or support OR logic.

### Ambiguity 4: Non-functional requirements lack concrete metrics

"Should be fast enough" and "Don't break existing functionality" are not measurable. There are no SLA targets, no load/concurrency requirements, and no regression test baseline defined.

**Assumption (pending clarification):** We assume standard integration test coverage for new endpoints and that existing tests in `tests/api/search.rs` serve as the regression baseline.

### Out of Scope: "Better UI" (non-MVP)

The "Better UI" requirement is marked as non-MVP and cannot be planned without:
- Design mockups (no Figma URL provided or linked in the feature)
- A frontend repository (the Repository Registry only contains `trustify-backend`)

This requirement is **excluded from the implementation plan**. It should be revisited when design mockups are available and a frontend repository is identified.

## Workflow Mode

**Mode:** `direct-to-main`

**Rationale:** All changes are within the single `trustify-backend` repository. The tasks can be delivered incrementally — adding database indexes, improving the search service, and adding filter support are independent improvements that each leave `main` in a working state. No atomicity indicators (coordinated migrations, breaking API changes, cross-cutting refactors, tightly coupled cross-repo components) are present.

## Impact Map

```
trustify-backend:
  changes:
    - Add database migration for full-text search indexes on searchable entity columns
    - Refactor SearchService to use full-text search with relevance ranking
    - Add filter parameters to the search endpoint (entity type, severity, date range)
    - Add filter model and query builder integration in common query helpers
    - Update search endpoint to accept and apply filter parameters
    - Add integration tests for improved search relevance and filter functionality
```

## Tasks

| # | Summary | Scope |
|---|---|---|
| 1 | Add full-text search migration for searchable entity columns | Database migration |
| 2 | Refactor SearchService for full-text search with relevance ranking | Search service layer |
| 3 | Add search filter support to query helpers and search endpoint | Filter parameters and endpoint |
| 4 | Add integration tests for search improvements | Test coverage |
