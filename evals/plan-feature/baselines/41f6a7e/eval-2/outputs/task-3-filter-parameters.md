# Task 3: Add filter parameters to search endpoint

## Repository

trustify-backend

## Target Branch

`main`

## Description

Extend the search endpoint with structured filter parameters so users can narrow results by entity type, date range, advisory severity, and package license. Introduce a `SearchFilter` model to encapsulate filter logic and wire it through the endpoint into the service layer.

## Files to Create

- `modules/search/src/model/mod.rs` -- Define the `SearchFilter` struct with the following fields:
  - `entity_type: Option<Vec<EntityType>>` -- Filter by entity kind (enum: `sbom`, `advisory`, `package`). When multiple values are provided, results matching any of the types are returned (OR logic).
  - `date_from: Option<chrono::NaiveDate>` -- Include only results created/modified on or after this date
  - `date_to: Option<chrono::NaiveDate>` -- Include only results created/modified on or before this date
  - `severity: Option<Vec<String>>` -- For advisories: filter by severity level (e.g., `critical`, `high`, `medium`, `low`)
  - `license: Option<String>` -- For packages: filter by license identifier (SPDX expression substring match)

  Also define the `EntityType` enum with `Sbom`, `Advisory`, `Package` variants, implementing `Deserialize` for query parameter parsing.

## Files to Modify

- `modules/search/src/endpoints/mod.rs` -- Update the GET `/api/v2/search` handler to:
  - Accept new query parameters corresponding to `SearchFilter` fields: `entity_type`, `date_from`, `date_to`, `severity`, `license`
  - Deserialize these into a `SearchFilter` instance using Axum's `Query` extractor
  - Pass the filter to the service layer
  - Return 400 with a descriptive error if filter values are malformed (e.g., invalid date format, unknown entity type)

- `modules/search/src/service/mod.rs` -- Update the search method to:
  - Accept a `SearchFilter` parameter
  - Apply entity type filtering by conditionally querying only the relevant tables
  - Apply date range filtering with `WHERE created_at >= $date_from AND created_at <= $date_to` clauses
  - Apply severity filtering for advisory results using a `WHERE severity IN (...)` clause
  - Apply license filtering for package results using `WHERE license ILIKE '%$license%'`
  - Combine filters with AND logic (all specified filters must match)

## API Changes

**GET /api/v2/search**

New query parameters (all optional):
- `entity_type` (string, repeatable): Filter by entity type. Values: `sbom`, `advisory`, `package`. Can be specified multiple times for OR logic (e.g., `?entity_type=sbom&entity_type=advisory`).
- `date_from` (string, ISO 8601 date): Include results created on or after this date. Format: `YYYY-MM-DD`.
- `date_to` (string, ISO 8601 date): Include results created on or before this date. Format: `YYYY-MM-DD`.
- `severity` (string, repeatable): Filter advisory results by severity. Values: `critical`, `high`, `medium`, `low`. Ignored for non-advisory entity types.
- `license` (string): Filter package results by license identifier (substring match). Ignored for non-package entity types.

All parameters are optional and additive (AND logic). Omitting all filters returns unfiltered results (existing behavior preserved).

This is a backward-compatible addition.

## Reuse Candidates

- `common/src/db/query.rs` -- Reuse the existing filtering helpers. The date range and IN-clause patterns likely already exist here for other endpoints. Check for `apply_filter`, `FilterClause`, or similar abstractions before writing new ones.
- `common/src/model/paginated.rs` -- No changes needed; pagination continues to work as before.

## Implementation Notes

- Follow the pattern in `common/src/db/query.rs` for building filter clauses. The existing query builder likely has helpers for date range and set membership filtering -- reuse those rather than writing raw SQL.
- For the `entity_type` filter, the most efficient approach is to skip querying tables that are excluded by the filter rather than querying all tables and filtering in application code.
- Use Axum's `Query<SearchParams>` extractor pattern. Define a `SearchParams` struct that includes the existing `q` parameter alongside the new filter fields. Use `#[serde(default)]` for optional fields.
- For multi-value parameters like `entity_type` and `severity`, use `#[serde(deserialize_with = "...")]` or accept comma-separated values as an alternative to repeated parameters.
- Validate that `date_from <= date_to` when both are provided; return 400 if not.
- The `severity` and `license` filters should be silently ignored when the `entity_type` filter excludes the relevant type (e.g., `severity` is ignored if `entity_type=sbom` only). Do not return an error.

## Acceptance Criteria

- [ ] Filtering by `entity_type=advisory` returns only advisory results
- [ ] Filtering by multiple entity types returns results matching any of the specified types
- [ ] Date range filtering correctly bounds results by creation date
- [ ] Severity filtering narrows advisory results to matching severity levels
- [ ] License filtering narrows package results by license substring
- [ ] Combining multiple filters applies AND logic
- [ ] Omitting all filters returns the same results as before (backward compatible)
- [ ] Invalid filter values return 400 with a descriptive error message
- [ ] `date_from > date_to` returns 400

## Test Requirements

- Integration test: filter by single entity type and verify only that type is returned
- Integration test: filter by multiple entity types and verify union of types is returned
- Integration test: date range filtering with known test data
- Integration test: severity filter on advisories
- Integration test: license filter on packages
- Integration test: combined filters (entity type + date range + severity)
- Integration test: invalid filter values return 400
- Integration test: no filters returns full results (backward compatibility)

## Dependencies

- Task 1 (search indexes) should be completed first for optimal performance, though this task is functionally independent -- filters can be applied to LIKE-based queries too
