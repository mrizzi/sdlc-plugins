## Repository
trustify-backend

## Description
Improve search result relevance by implementing weighted field scoring in the `SearchService`. The feature requirement states users complain about "irrelevant results" but provides no definition of relevance, no example queries, and no expected result ordering (see Ambiguity A2 in impact-map.md). This task implements a weighted scoring model that boosts matches in high-signal fields (e.g., name, title) over low-signal fields (e.g., description, body text).

**Assumption (pending clarification):** "More relevant" means results where the search term appears in the entity name/title should rank higher than results where it appears only in description or metadata. This assumption should be validated with product by providing example queries and reviewing the resulting order. More advanced relevance approaches (ML ranking, click-through signals) are out of scope for MVP.

## Files to Modify
- `modules/search/src/service/mod.rs` — Implement weighted scoring: assign higher weights to name/title columns and lower weights to description/body columns when constructing full-text search queries; order results by relevance score descending
- `common/src/model/paginated.rs` — Optionally extend `PaginatedResults<T>` to include a relevance score field in search results, or add a `SearchResults<T>` wrapper that includes score metadata

## Implementation Notes
- The `SearchService` in `modules/search/src/service/mod.rs` currently performs full-text search across entities. Modify the query construction to use PostgreSQL `ts_rank` or `ts_rank_cd` functions with field-specific weights.
- PostgreSQL full-text search supports weight categories (A, B, C, D). Map entity fields to weights:
  - Weight A (highest): entity name/title fields (e.g., SBOM name, advisory title, package name from `entity/src/sbom.rs`, `entity/src/advisory.rs`, `entity/src/package.rs`)
  - Weight B: identifiers and keys (e.g., CVE IDs in advisories)
  - Weight C: description/summary fields
  - Weight D (lowest): other indexed text
- The `PaginatedResults<T>` wrapper in `common/src/model/paginated.rs` is used by all list endpoints. If adding a score field, consider whether to add it to `PaginatedResults` (affects all endpoints) or create a search-specific response type. The search-specific type is preferred to avoid impacting other endpoints.
- Ensure the relevance scoring is consistent across entity types (SBOMs, advisories, packages) so that cross-entity search results are meaningfully ordered.
- The indexes created in Task 1 should support `ts_rank` queries efficiently. Coordinate with Task 1 to ensure the index type (GIN with tsvector) is compatible with ranking.

## Reuse Candidates
- `common/src/model/paginated.rs::PaginatedResults` — Existing response wrapper; use as the base for a search-specific response type
- `common/src/db/query.rs::apply_sorting` — Existing sorting helper; extend to support score-based ordering for search queries
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService::search` — Existing search method on AdvisoryService that may contain patterns to align with

## Acceptance Criteria
- [ ] Search results are ordered by relevance score (highest relevance first)
- [ ] Matches in name/title fields rank higher than matches in description fields for the same query
- [ ] The `GET /api/v2/search` response includes relevance score metadata for each result
- [ ] Cross-entity results (SBOMs, advisories, packages) are ordered by a unified scoring model
- [ ] Existing API response structure is preserved (new fields are additive, not breaking)

## Test Requirements
- [ ] Integration test: a query matching an entity by name ranks that entity above one matching only by description
- [ ] Integration test: search results include score metadata in the response
- [ ] Existing search integration tests in `tests/api/search.rs` continue to pass

## Dependencies
- Depends on: Task 1 — Optimize search query performance (indexes must support ranking queries)
