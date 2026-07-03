## Repository
trustify-backend

## Target Branch
main

## Description
Add filter query parameters to the `GET /api/v2/search` endpoint so that users can narrow search results by entity type and other criteria. This task addresses the "add filters" requirement from TC-9002. The endpoint currently accepts only a search query; after this change, it will also accept optional filter parameters to scope results.

**Assumption pending clarification:** The feature description specifies "some kind of filtering capability" without defining which fields to filter on, what filter types (exact match, range, multi-select), or how filters combine. This task assumes the following filter parameters based on the existing entity model: `entity_type` (enum: sbom, advisory, package) to filter by entity kind, and `severity` (enum: critical, high, medium, low) to filter advisory results by severity level. Additional filter fields should be specified by the product owner.

additional_fields: { "labels": ["ai-generated-jira"], "priority": "Normal", "fixVersions": "RHTPA 1.6.0" }

## Files to Modify
- `modules/search/src/endpoints/mod.rs` -- add optional query parameters `entity_type` (enum: sbom, advisory, package) and `severity` (enum: critical, high, medium, low) to the search handler; pass filter values to the service layer
- `modules/search/src/service/mod.rs` -- modify the search method to accept filter parameters and apply them as WHERE clause conditions on the search query; use existing query builder helpers for filter composition

## API Changes
- `GET /api/v2/search?q=term&entity_type=sbom` -- MODIFY: accepts optional `entity_type` query parameter to filter results by entity kind (sbom, advisory, package)
- `GET /api/v2/search?q=term&severity=critical` -- MODIFY: accepts optional `severity` query parameter to filter advisory results by severity level (critical, high, medium, low)
- Both parameters are optional; when omitted, behavior is unchanged from the current endpoint (backwards-compatible)

## Implementation Notes
Add filter query parameters to the search endpoint handler in `modules/search/src/endpoints/mod.rs` using `axum::extract::Query` with a filter struct:

```
struct SearchFilters {
    entity_type: Option<EntityTypeFilter>,
    severity: Option<SeverityFilter>,
}
```

Define `EntityTypeFilter` as an enum with variants `Sbom`, `Advisory`, `Package` and `SeverityFilter` as an enum with variants `Critical`, `High`, `Medium`, `Low`. Use `#[serde(rename_all = "lowercase")]` for URL-friendly parameter values.

In the service layer (`modules/search/src/service/mod.rs`), apply filters as additional WHERE conditions on the search query:
- `entity_type` filter: restrict the search to only the specified entity table(s)
- `severity` filter: when entity_type is advisory (or when searching across all types), add a condition on the advisory severity field from `entity/src/advisory.rs`

Leverage the existing shared filtering helpers in `common/src/db/query.rs` for composing filter conditions with the existing pagination and sorting logic. The filter conditions should be combined with AND semantics (all filters must match).

Per CONVENTIONS.md: all handlers return `Result<T, AppError>` with `.context()` wrapping.
Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` module scope.

Per CONVENTIONS.md: shared filtering, pagination, and sorting via `common/src/db/query.rs`.
Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's `.rs` module scope.

## Reuse Candidates
- `common/src/db/query.rs` -- shared query builder helpers for filtering, pagination, and sorting; reuse for composing filter WHERE conditions
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` -- contains the severity field definition; reference for severity enum values and naming
- `modules/search/src/service/mod.rs::SearchService` -- existing search service; extend with filter support rather than creating a new service
- `modules/search/src/endpoints/mod.rs` -- existing search endpoint handler; extend with additional query parameters

## Acceptance Criteria
- [ ] `GET /api/v2/search?q=term&entity_type=sbom` returns only SBOM results
- [ ] `GET /api/v2/search?q=term&entity_type=advisory` returns only advisory results
- [ ] `GET /api/v2/search?q=term&entity_type=package` returns only package results
- [ ] `GET /api/v2/search?q=term&severity=critical` returns only advisories with critical severity
- [ ] `GET /api/v2/search?q=term` (no filters) returns all entity types as before (backwards-compatible)
- [ ] Multiple filters combine with AND semantics
- [ ] Invalid filter values return a 400 Bad Request error with a descriptive message

## Test Requirements
- [ ] Integration test: search with `entity_type=sbom` returns only SBOM entities
- [ ] Integration test: search with `entity_type=advisory&severity=high` returns only high-severity advisories
- [ ] Integration test: search without filters returns results from all entity types (backwards compatibility)
- [ ] Integration test: invalid `entity_type` value returns 400 Bad Request
- [ ] Integration test: `severity` filter is ignored when `entity_type` is not advisory (or returns empty if applied)

## Verification Commands
- `cargo build -p trustify-search` -- compiles without errors
- `cargo test --test search` -- integration tests pass
- `curl -s "http://localhost:8080/api/v2/search?q=test&entity_type=sbom" | jq .` -- returns only SBOM results

## Dependencies
- Depends on: Task 2 -- Implement relevance scoring in search service
