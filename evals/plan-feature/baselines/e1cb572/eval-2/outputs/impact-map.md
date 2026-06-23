# Repository Impact Map: TC-9002 — Improve Search Experience

## Feature Summary

TC-9002 requests improvements to the search experience across three dimensions: performance ("search should be faster"), relevance ("results should be more relevant"), and filtering ("some kind of filtering capability"). The feature description is notably underspecified; this impact map documents identified ambiguities, assumptions made, and the resulting scope.

## Workflow Mode

**Direct-to-main** — Single repository (trustify-backend), no linked epic or feature branch required. Tasks target `main`.

## Ambiguities Identified

The feature description (TC-9002) is intentionally vague. The following ambiguities were identified and must be clarified with the product owner before implementation begins. In the interim, assumptions are documented below to make tasks actionable.

### Ambiguity 1: No Performance Targets for "Faster" Search

The requirement states "Search should be faster" and "Currently too slow" without specifying:
- Current search latency (baseline measurement)
- Target latency or throughput (e.g., p95 < 200ms)
- Whether the concern is database query time, network latency, or perceived UI responsiveness
- Scale parameters (dataset size, concurrent users)

**Assumption (pending clarification):** The primary bottleneck is database query performance. We will add a database index on commonly searched text columns and optimize the full-text search query in `SearchService`. Performance improvement will be validated by integration test timing but no specific SLA is assumed.

### Ambiguity 2: No Definition of "Relevance"

The requirement states "Results should be more relevant" and "Users complain about irrelevant results" without specifying:
- What makes a result "relevant" (exact match priority? recency? severity weighting?)
- Which entity types are most affected (SBOMs, advisories, packages, or all?)
- Whether relevance means ranking order, filtering out noise, or both
- Whether full-text search should support stemming, fuzzy matching, or phrase matching

**Assumption (pending clarification):** We will implement PostgreSQL full-text search with `ts_vector`/`ts_query` to replace any naive `LIKE`/`ILIKE` queries, providing ranking via `ts_rank`. This gives built-in stemming and relevance scoring. All searchable entity types (SBOM, Advisory, Package) will be covered.

### Ambiguity 3: No Specification of Filter Types

The requirement states "Some kind of filtering capability" without specifying:
- Which fields should be filterable (entity type? severity? date range? license? vendor?)
- Whether filters are combinable (AND/OR logic)
- Whether filters apply to the unified search endpoint or per-entity list endpoints
- Filter UX expectations (faceted counts? autocomplete?)

**Assumption (pending clarification):** We will add query parameter filters to the `GET /api/v2/search` endpoint for: entity type (sbom/advisory/package), severity (for advisories), and date range (created_after/created_before). Filters will be combinable with AND semantics. This leverages the existing query builder helpers in `common/src/db/query.rs`.

### Ambiguity 4: No Concrete Non-Functional Requirements

"Should be fast enough" and "Don't break existing functionality" provide no measurable criteria. There are no defined:
- Latency SLAs
- Regression test requirements
- Load/stress test expectations

**Assumption (pending clarification):** Existing integration tests in `tests/api/search.rs` serve as the regression baseline. New functionality will include corresponding integration tests. No load testing is in scope for this iteration.

### Ambiguity 5: Scope of "Better UI" Is Undefined and Out of Scope

The non-MVP requirement "Better UI — Make it look nicer" cannot be planned because:
- There is no frontend repository in scope (only `trustify-backend`)
- No design mockups or wireframes are referenced
- "Look nicer" has no actionable specification

**Decision:** "Better UI" is **excluded from this plan**. It requires a frontend repository, design mockups, and a separate feature ticket. This plan covers backend-only changes.

## Impacted Areas

### Primary Impact

| File/Directory | Impact | Reason |
|---|---|---|
| `modules/search/src/service/mod.rs` | MODIFY | Rewrite search logic to use PostgreSQL full-text search with ranking |
| `modules/search/src/endpoints/mod.rs` | MODIFY | Add filter query parameters to search endpoint |
| `common/src/db/query.rs` | MODIFY | Extend query builder with full-text search and filter helpers |
| `migration/src/` | CREATE (new migration) | Add `tsvector` columns and GIN indexes for full-text search |
| `tests/api/search.rs` | MODIFY | Add tests for relevance ranking, filters, and performance |

### Secondary Impact

| File/Directory | Impact | Reason |
|---|---|---|
| `entity/src/sbom.rs` | MODIFY | Add search vector column to SBOM entity |
| `entity/src/advisory.rs` | MODIFY | Add search vector column to Advisory entity |
| `entity/src/package.rs` | MODIFY | Add search vector column to Package entity |
| `modules/search/src/lib.rs` | MODIFY | Update module exports if new model types are added |
| `modules/fundamental/src/advisory/service/advisory.rs` | REVIEW | Ensure AdvisoryService severity field is accessible for filtering |

### Out of Scope

- Frontend/UI changes ("Better UI" requirement) — no frontend repository available
- Load testing / performance benchmarking infrastructure
- Search analytics or telemetry
- Autocomplete or typeahead functionality

## Task Breakdown

| Task | Title | Dependencies |
|---|---|---|
| Task 1 | Add database migration for full-text search indexes | None |
| Task 2 | Update entities with search vector columns | Task 1 |
| Task 3 | Extend query builder with full-text search helpers | None |
| Task 4 | Implement full-text search with relevance ranking in SearchService | Tasks 1, 2, 3 |
| Task 5 | Add filter parameters to search endpoint | Task 4 |
| Task 6 | Add integration tests for search improvements | Task 5 |
