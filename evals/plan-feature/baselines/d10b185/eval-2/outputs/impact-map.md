# Repository Impact Map — TC-9002: Improve search experience

## Ambiguities and Scope Exclusions

The feature description for TC-9002 is underspecified. The following ambiguities were identified and must be clarified with the product owner before implementation begins. Assumptions are documented below where decisions were needed to produce an actionable plan.

### Ambiguities Flagged

1. **No performance targets for "search should be faster."** The description says "currently too slow" and the NFR says "should be fast enough" — neither provides measurable targets. There are no current latency baselines (P50/P95/P99), no target latency SLAs, and no load/concurrency requirements. **Assumption pending clarification:** We assume the goal is to add database indexing for full-text search columns and optimize query execution, targeting sub-200ms P95 response time for typical search queries.

2. **No relevance criteria for "results should be more relevant."** The description does not explain what makes current results irrelevant, what ranking signals matter (recency, severity, exact match vs partial match), or how relevance should be measured. **Assumption pending clarification:** We assume the goal is to implement PostgreSQL full-text search with `tsvector`/`tsquery` and `ts_rank` scoring to replace any naive `LIKE`/`ILIKE` pattern matching in the existing `SearchService`, covering SBOMs (by name/description), advisories (by title/description/severity), and packages (by name/license).

3. **No filter specification for "add filters."** "Some kind of filtering capability" does not define which entity fields are filterable, what operators are supported (exact match, range, contains), whether filters combine with AND/OR logic, or which entity types support filtering. **Assumption pending clarification:** We assume MVP filters are: severity filter for advisories (enum: low/medium/high/critical), entity type filter for search results (enum: sbom/advisory/package), and a date range filter for SBOMs/advisories by ingestion date.

4. **No specification of which search entities are in scope.** The repository has distinct search across SBOMs, advisories, and packages, but the feature does not clarify whether improvements apply to all entity types or a subset. **Assumption pending clarification:** We assume all three entity types (SBOMs, advisories, packages) are in scope for search improvements since the existing `SearchService` in `modules/search/` performs cross-entity search.

5. **Non-functional requirements are unmeasurable.** "Should be fast enough" and "don't break existing functionality" are not testable criteria. **Assumption pending clarification:** We interpret "fast enough" as sub-200ms P95 for search queries and "don't break existing functionality" as requiring all existing integration tests in `tests/api/search.rs` to continue passing.

### Scope Exclusion

- **"Better UI" (non-MVP) is excluded from this plan.** This requirement cannot be planned without design mockups or a frontend repository. The Repository Registry contains only `trustify-backend` — no frontend repository is available. This requirement should be addressed in a separate feature once a Figma design and frontend repository are available.

## Workflow Mode

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators were identified. Each task can be merged independently without breaking `main`:
- The database migration (Task 1) adds new indexes and columns without removing existing ones — existing queries continue to work.
- The search service optimization (Task 2) enhances the existing `SearchService` with backward-compatible changes.
- The filter endpoint additions (Task 3) extend existing query parameter handling without modifying current behavior.

Each PR is independently shippable and does not require the others to avoid breaking `main`.

## Impact Map

```
trustify-backend:
  changes:
    - Add database migration for full-text search indexes (tsvector columns and GIN indexes on sbom, advisory, and package tables)
    - Optimize SearchService to use PostgreSQL full-text search with ts_rank scoring instead of naive pattern matching
    - Add filter query parameters to the search endpoint (severity, entity type, date range)
    - Add filter query parameters to list endpoints for advisory (severity filter) and sbom (date range filter)
    - Update integration tests for search and list endpoints to cover new search behavior and filter parameters
```
