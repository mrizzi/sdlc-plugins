# Repository Impact Map — TC-9002: Improve Search Experience

## Workflow Mode

**Mode:** `direct-to-main`

**Rationale:** No atomicity indicators identified. Each search improvement (indexing, relevance tuning, filtering) can land independently on `main` without breaking existing functionality. There are no coordinated schema migrations, breaking API changes, cross-cutting refactors, or tightly coupled frontend/backend components that require all-or-nothing delivery.

## Ambiguities Identified

The feature description TC-9002 contains significant ambiguity that must be resolved before implementation proceeds with full confidence. The following gaps are flagged as **assumptions pending clarification**:

1. **No quantitative performance targets.** The requirement "Search should be faster" and NFR "Should be fast enough" provide no measurable thresholds — no p95/p99 latency targets, no baseline measurements, no load/concurrency expectations. **Assumption:** Target sub-500ms p95 response time for search queries under typical load. This needs stakeholder confirmation.

2. **No relevance ranking criteria defined.** "Results should be more relevant" does not specify what "relevant" means — no ranking algorithm, no weighting factors, no user-validated examples of good vs. bad results. **Assumption:** Implement PostgreSQL full-text search with `ts_rank` scoring across entity name and description fields as a baseline improvement. Relevance strategy needs product review.

3. **No filter specification.** "Add filters — Some kind of filtering capability" does not define which fields are filterable, what filter operators are supported (exact match, range, multi-select), or how filters compose (AND/OR). **Assumption:** Add filtering by entity type (SBOM, advisory, package) and by date range as initial MVP filters, following the existing `query.rs` filtering pattern. Filter set needs product confirmation.

4. **No performance baseline or regression criteria.** The NFR "Don't break existing functionality" provides no regression test baseline, no backward-compatibility contract for the search API response shape, and no definition of what constitutes "breaking." **Assumption:** Existing `GET /api/v2/search` response shape is preserved; new filter parameters are additive (optional query params); existing integration tests in `tests/api/search.rs` continue to pass.

5. **"Better UI" excluded from scope.** The non-MVP requirement "Better UI — Make it look nicer" cannot be planned: no design mockups or Figma links are provided, and no frontend repository is listed in the Repository Registry. This requirement is **excluded from the implementation plan** entirely. It should be addressed in a separate feature once a frontend repository and design assets are available.

## Impact Map

```
trustify-backend:
  changes:
    - Add database indexes on searchable text columns to improve query performance
    - Implement PostgreSQL full-text search (tsvector/tsquery) in the search service for improved relevance ranking
    - Add filter parameters (entity type, date range) to the search endpoint
    - Extend search endpoint to accept and apply filter query parameters
    - Add integration tests for search performance, relevance ordering, and filtering
```
