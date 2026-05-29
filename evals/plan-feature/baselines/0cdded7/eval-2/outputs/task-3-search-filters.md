## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capabilities to the search endpoint, allowing users to narrow search results by entity type, severity, and date range. This addresses TC-9002 requirement: "Add filters — some kind of filtering capability." Filter parameters are optional and additive (multiple filters can be combined). When no filters are specified, behavior is unchanged from the current search.

## Files to Modify
- `modules/search/src/service/mod.rs` — extend SearchService to accept and apply filter parameters: `entity_type` (enum: sbom, advisory, package), `severity` (advisory severity levels), `date_from` and `date_to` (ISO 8601 date range filtering on created_at/published_at)
- `modules/search/src/endpoints/mod.rs` — add query parameter extraction for filter fields on GET /api/v2/search; validate and pass filters to SearchService
- `common/src/db/query.rs` — add shared filter builder helpers for entity type, severity, and date range filtering if not already present (check existing helpers first)

## API Changes
- `GET /api/v2/search` — MODIFY: accepts new optional query parameters: `entity_type` (string, one of: sbom, advisory, package), `severity` (string, advisory severity level), `date_from` (ISO 8601 date), `date_to` (ISO 8601 date). All parameters are optional. When multiple filters are provided, they are combined with AND logic.

## Implementation Notes
- Review the existing query helpers in `common/src/db/query.rs` for filtering and pagination patterns. The module already has shared filtering helpers — extend these rather than creating search-specific filter logic.
- For `entity_type` filtering: when searching across SBOM, advisory, and package entities, skip the entity types that don't match the filter. This is a query-level optimization, not a post-query filter.
- For `severity` filtering: this only applies to advisory entities. Use the `severity` field from `AdvisorySummary` (defined in `modules/fundamental/src/advisory/model/summary.rs`). When severity filter is specified and entity_type is not advisory, return no advisory results (or ignore the filter for non-advisory entity types — choose the least surprising behavior).
- For date range filtering: use `created_at` for SBOMs and `published_at` for advisories. Reference the entity definitions in `entity/src/sbom.rs` and `entity/src/advisory.rs` for exact column names and types.
- Validate date parameters using standard ISO 8601 parsing. Return `AppError` (from `common/src/error.rs`) with a 400 status for invalid date formats.
- All filter parameters are optional. When omitted, the search behaves identically to the pre-filter implementation (backward compatibility).

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, sorting; extend for the new filter types
- `modules/fundamental/src/advisory/model/summary.rs` — `AdvisorySummary` struct with `severity` field; reference for valid severity values
- `modules/fundamental/src/advisory/service/advisory.rs` — AdvisoryService list/search methods likely already implement severity filtering patterns
- `entity/src/sbom.rs` — SBOM entity definition with `created_at` column
- `entity/src/advisory.rs` — Advisory entity definition with `published_at` column

## Acceptance Criteria
- [ ] GET /api/v2/search accepts optional `entity_type`, `severity`, `date_from`, and `date_to` query parameters
- [ ] Filtering by entity_type returns only results of the specified type
- [ ] Filtering by severity returns only advisory results matching the severity level
- [ ] Filtering by date range returns only results within the specified range
- [ ] Multiple filters combine with AND logic
- [ ] Omitting all filters returns the same results as before (backward compatibility)
- [ ] Invalid filter values (e.g., bad date format, unknown entity type) return 400 with a descriptive error message

## Test Requirements
- [ ] Integration test: filter by entity_type=sbom returns only SBOM results
- [ ] Integration test: filter by entity_type=advisory returns only advisory results
- [ ] Integration test: filter by severity returns only advisories matching that severity
- [ ] Integration test: filter by date_from and date_to returns only results within range
- [ ] Integration test: combining entity_type and severity filters narrows results correctly
- [ ] Integration test: no filters specified returns all results (backward compatibility)
- [ ] Integration test: invalid date format returns 400 error
- [ ] Existing search tests in `tests/api/search.rs` continue to pass

## Verification Commands
- `cargo test -p search` — search module tests pass
- `cargo test --test search` — search integration tests pass

## Dependencies
- Depends on: Task 1 — Add search indexes (B-tree indexes on severity and date columns)

[sdlc-workflow] Description digest: sha256:eb2a1563de2b48095485f3f432e1859c92ccd87c69b0bfecae7ce1a396c0e525
