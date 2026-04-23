## Repository
trustify-backend

## Description
Add filtering capabilities to the search endpoint, allowing users to narrow results by entity type, advisory severity, and date range. This addresses the "Add filters — some kind of filtering capability" requirement.

**Assumption pending clarification**: The feature description does not specify which filters to add, what fields should be filterable, or how filters combine. We assume the following filters based on the data model: entity type (sbom, advisory, package), advisory severity (low, medium, high, critical), and date range (created_after, created_before). We assume filters combine with AND logic. These choices should be validated with the product owner.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Add query parameters to the `GET /api/v2/search` handler for entity type (`type`), severity (`severity`), date range (`created_after`, `created_before`). Parse and validate these parameters before passing them to the search service.
- `modules/search/src/service/mod.rs` — Extend `SearchService` to accept a filter struct and apply WHERE clauses conditionally based on which filters are present. Compose filter conditions with the existing full-text search query from Task 2.
- `common/src/db/query.rs` — Add reusable filter builder functions for enum-based filtering (e.g., severity levels) and date range filtering. These follow the existing shared query builder pattern for filtering, pagination, and sorting already in this file.

## Files to Create
- `modules/search/src/model/mod.rs` — Define a `SearchFilter` struct that holds optional fields for each filter type (entity_type, severity, date range). Also define a `SearchResultItem` response struct that wraps results from different entity types in a uniform shape.

## API Changes
- `GET /api/v2/search` — MODIFY: Add optional query parameters: `type` (enum: sbom, advisory, package), `severity` (enum: low, medium, high, critical), `created_after` (ISO 8601 date), `created_before` (ISO 8601 date). When no filters are provided, behavior is unchanged (backward compatible).

## Implementation Notes
- In `modules/search/src/endpoints/mod.rs`, use Axum's `Query<SearchFilter>` extractor to deserialize filter parameters from the query string. All filter fields should be `Option<T>` so they are optional.
- In `modules/search/src/service/mod.rs`, build the WHERE clause conditionally: only add a filter condition when the corresponding `Option` is `Some`. Use SeaORM's `.filter()` with `Condition::all()` for AND combination.
- The severity filter should reference the severity field in `entity/src/advisory.rs` and match the enum values used in `modules/fundamental/src/advisory/model/summary.rs` (`AdvisorySummary`).
- Date range filters apply to the created/modified timestamp columns in `entity/src/sbom.rs`, `entity/src/advisory.rs`, and `entity/src/package.rs`.
- Follow the existing module structure pattern (`model/ + service/ + endpoints/`) visible in `modules/fundamental/src/sbom/` and `modules/fundamental/src/advisory/`. The search module currently lacks a `model/` directory, so this task creates one.
- Wrap filtered results in `PaginatedResults<T>` from `common/src/model/paginated.rs`.

## Reuse Candidates
- `common/src/db/query.rs::*` — Existing filtering and pagination helpers to extend
- `common/src/model/paginated.rs::PaginatedResults` — Response wrapper
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Reference for severity field/enum values

## Acceptance Criteria
- [ ] `GET /api/v2/search?type=advisory` returns only advisory results
- [ ] `GET /api/v2/search?severity=critical` returns only advisories with critical severity
- [ ] `GET /api/v2/search?created_after=2024-01-01` returns only results created after the given date
- [ ] Multiple filters can be combined: `?type=advisory&severity=high` returns only high-severity advisories
- [ ] Omitting all filters returns the same results as before (backward compatible)
- [ ] Invalid filter values return a clear 400 error with a descriptive message
- [ ] Results are still ranked by relevance score when filters are applied

## Test Requirements
- [ ] Integration test: filtering by entity type returns only that type
- [ ] Integration test: filtering by severity returns only matching advisories
- [ ] Integration test: date range filtering includes/excludes results correctly
- [ ] Integration test: combining multiple filters applies AND logic
- [ ] Integration test: invalid filter values return 400 status
- [ ] Integration test: no filters returns same results as unfiltered search
- [ ] Integration test: filters work correctly with pagination (PaginatedResults)

## Dependencies
- Depends on: Task 2 — Improve search relevance with weighted full-text ranking
