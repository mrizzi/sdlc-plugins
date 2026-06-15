# Task 3: Add filter parameters to the search endpoint

## Repository

trustify-backend

## Target Branch

main

## Description

Add filtering capabilities to the unified search endpoint (`GET /api/v2/search`) so that users can narrow results by entity type, severity, and date range. The feature requirement states "add filters — some kind of filtering capability" without further specification.

**Ambiguity note:** The feature description does not specify which fields should be filterable, what filter operators are supported, or how multiple filters combine. **Assumption pending clarification:** We implement the following filters as query parameters:
- `type` — Filter by entity type (enum: `sbom`, `advisory`, `package`). Optional, multi-select.
- `severity` — Filter advisories by severity level (enum: `low`, `medium`, `high`, `critical`). Optional, multi-select. Only applies when results include advisories.
- `date_from` / `date_to` — Filter by creation date range (ISO 8601 format). Optional.

Multiple filters combine with AND semantics (e.g., `type=advisory&severity=high` returns only high-severity advisories). Multiple values for the same filter use OR semantics (e.g., `type=sbom&type=advisory` returns both SBOMs and advisories).

## Files to Modify

- `modules/search/src/service/mod.rs` — Extend `SearchService` search method to accept filter parameters and apply them as `WHERE` clause conditions on the search query.
- `modules/search/src/endpoints/mod.rs` — Add query parameter extraction for filter fields (`type`, `severity`, `date_from`, `date_to`) and pass them to the service layer.

## Files to Create

- `modules/search/src/model/mod.rs` — Define `SearchFilter` struct to encapsulate filter parameters, and `SearchEntityType` / `SeverityLevel` enums for type-safe filter values.

## Implementation Notes

- Follow the existing query builder pattern in `common/src/db/query.rs` which already provides shared filtering, pagination, and sorting helpers. The search filters should integrate with this pattern rather than implementing ad-hoc SQL construction.
- Use Axum's query parameter extraction (`axum::extract::Query<T>`) to deserialize filter parameters from the URL, consistent with how other endpoints in the repository handle query parameters (see `modules/fundamental/src/sbom/endpoints/list.rs` and `modules/fundamental/src/advisory/endpoints/list.rs`).
- The `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs` already includes a `severity` field — use the same severity representation for filter values.
- The `PackageSummary` in `modules/fundamental/src/package/model/summary.rs` includes a `license` field — do not add license filtering in this task (out of scope), but note it as a potential future filter.
- Validate filter values at the endpoint layer: return `400 Bad Request` for invalid enum values or malformed dates, following the `AppError` pattern from `common/src/error.rs`.
- Date range filters should use `>=` for `date_from` and `<=` for `date_to`, allowing either or both to be omitted.

## Reuse Candidates

- `common/src/db/query.rs` — Query builder helpers for filtering and pagination. Extend with search-specific filter predicates.
- `common/src/error.rs` — `AppError` enum for returning structured error responses on invalid filter input.
- `modules/fundamental/src/advisory/model/summary.rs` — `AdvisorySummary` severity field as reference for severity enum values.

## Acceptance Criteria

- [ ] `GET /api/v2/search?type=advisory` returns only advisory results
- [ ] `GET /api/v2/search?type=sbom&type=package` returns both SBOM and package results
- [ ] `GET /api/v2/search?severity=high` filters advisory results to high severity only
- [ ] `GET /api/v2/search?date_from=2024-01-01&date_to=2024-12-31` returns results within the date range
- [ ] Multiple filters combine with AND semantics
- [ ] Invalid filter values return `400 Bad Request` with a meaningful error message
- [ ] Filters work correctly in combination with the text search query parameter
- [ ] Omitting all filters returns unfiltered results (backward compatible)
- [ ] Response continues to use `PaginatedResults<T>` format

## Test Requirements

- [ ] Test filtering by single entity type returns only that type
- [ ] Test filtering by multiple entity types returns the union of those types
- [ ] Test severity filter applies only to advisory results
- [ ] Test date range filter with both bounds, only `date_from`, and only `date_to`
- [ ] Test invalid filter values (e.g., `type=invalid`) return 400 status
- [ ] Test that filters combine correctly with a text search query
- [ ] Test that omitting all filters returns the same results as the unfiltered search

## Dependencies

- **Task 1** — Database indexes should be in place for performant filtered queries

---

[Description digest: sha256-md:c8e3f0a14b6d9827e0a3c1f5d4e6a8b0d2f4a6c8e0b2d4f6a8c0e2f4b6d8a0c2 would be posted as a comment]
