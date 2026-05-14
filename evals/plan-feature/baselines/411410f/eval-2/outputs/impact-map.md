# Impact Map — TC-9002: Improve Search Experience

## Feature Summary

The feature requests improvements to the platform's search capability across three MVP dimensions: performance ("search should be faster"), relevance ("results should be more relevant"), and filtering ("add filters"). A fourth requirement ("Better UI") is explicitly non-MVP and out of scope for this plan.

## Workflow Mode

- **Mode**: direct-to-main
- **Target Branch**: `main`

## Ambiguities and Clarification Needed

The feature description (TC-9002) is underspecified in several critical areas. The following ambiguities MUST be resolved with the product owner before implementation can be finalized. Tasks below document assumptions made to unblock planning, but these assumptions are pending clarification.

### Ambiguity 1: "Search should be faster" — No performance baseline or target

The requirement states search is "currently too slow" but provides no metrics. There is no current latency measurement, no target latency (e.g., p95 < 200ms), no indication of data volume, and no clarity on whether "slow" refers to query execution, network latency, or perceived UI responsiveness. The non-functional requirement "should be fast enough" is equally vague.

**Clarification needed**: What is the current measured latency? What is the target latency? At what data scale?

### Ambiguity 2: "Results should be more relevant" — No definition of relevance

"Relevant" is undefined. There is no ranking criteria, no examples of bad results, no indication of whether relevance means full-text matching accuracy, entity-type prioritization, recency weighting, or severity-based ranking. There is no mention of which entity types (SBOMs, advisories, packages) are most important to surface.

**Clarification needed**: What does a "relevant" result look like? Should advisories with higher severity rank above others? Should exact matches rank above partial matches? Is there a golden set of example queries and expected results?

### Ambiguity 3: "Add filters" — No filter types, values, or behavior specified

The requirement says "some kind of filtering capability" with no specifics. There is no list of filterable fields, no indication of whether filters should be AND/OR combinable, no mention of whether filters apply pre-search or post-search, and no clarity on which entity types support which filters.

**Clarification needed**: Which fields should be filterable (e.g., entity type, severity, date range, license, package name)? Should filters be combinable? Should filter values be enumerated or free-form?

### Ambiguity 4: "Better UI" — No design artifacts, and no frontend repository

This is marked non-MVP, but even for future planning there are no mockups, wireframes, or design specifications. Additionally, the target repository (`trustify-backend`) is a backend service — UI changes would require a frontend repository that is not in scope.

**Decision**: Excluded from this plan entirely. Cannot be planned without design mockups and a frontend repository.

### Ambiguity 5: Non-functional requirements are unmeasurable

"Should be fast enough" and "Don't break existing functionality" are not testable as stated. There are no acceptance thresholds for performance and no regression test baseline defined.

**Clarification needed**: What constitutes "fast enough"? Is there an existing test suite that defines "existing functionality" for regression purposes?

## Repository Impact

**Repository**: `trustify-backend`

### Impacted Modules

| Module / Path | Impact | Reason |
|---|---|---|
| `modules/search/src/service/mod.rs` | Heavy | Core search logic: query optimization, relevance scoring, filter application |
| `modules/search/src/endpoints/mod.rs` | Heavy | Endpoint changes: new query parameters for filters, response shape adjustments |
| `modules/search/Cargo.toml` | Light | Possible new dependencies for full-text search or caching |
| `common/src/db/query.rs` | Moderate | Shared query helpers: new filter predicates, search optimization utilities |
| `common/src/db/mod.rs` | Light | May need new exports for filter types |
| `common/src/model/paginated.rs` | Light | May need to include search metadata (e.g., relevance score, total count) |
| `entity/src/sbom.rs` | Light | Possible index annotations for search performance |
| `entity/src/advisory.rs` | Light | Possible index annotations, severity field used in filtering |
| `entity/src/package.rs` | Light | Possible index annotations, license field used in filtering |
| `migration/src/` | Moderate | New migration for database indexes (full-text search, composite indexes) |
| `tests/api/search.rs` | Heavy | New and updated integration tests for performance, relevance, and filters |
| `server/src/main.rs` | None | No changes expected — search module routes already mounted |

### Out of Scope

- Frontend/UI changes (no frontend repository available; "Better UI" is non-MVP)
- Ingestion pipeline changes (`modules/ingestor/`) — search improvements should not alter data ingestion
- SBOM/Advisory/Package list endpoints — these have their own query patterns; search is centralized in `modules/search/`

## Task Breakdown Summary

| Task | Title | Dependencies |
|---|---|---|
| 1 | Add database indexes for search performance | None |
| 2 | Optimize SearchService query execution | Task 1 |
| 3 | Improve search result relevance scoring | Task 2 |
| 4 | Add filter parameters to search endpoint | Task 3 |
| 5 | Add integration tests for search improvements | Task 4 |
