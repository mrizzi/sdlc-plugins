# Task 4 — Define SearchResultItem response model with enriched metadata

## Repository
trustify-backend

## Description
Create a structured response model for search results that includes a relevance score,
entity type discriminator, text snippet with highlighted matches, and entity metadata.
Update the search endpoint to return `PaginatedResults<SearchResultItem>` instead of the
current response shape. This gives API consumers the information they need to display
search results meaningfully — showing result relevance, entity kind, and contextual
match snippets.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Update the endpoint handler to serialize the
  new `SearchResultItem`-based response structure
- `modules/search/src/service/mod.rs` — Update the service to construct and return
  `SearchResultItem` instances with relevance score, entity type, and snippet data
- `modules/search/src/lib.rs` — Add `mod model` declaration and re-exports

## Files to Create
- `modules/search/src/model/mod.rs` — Define `SearchResultItem` struct with fields:
  - `entity_type` (String: "sbom", "advisory", or "package")
  - `entity_id` (String or UUID: the entity's primary key)
  - `title` (String: display name of the entity)
  - `snippet` (String: text excerpt with highlighted matching terms)
  - `relevance_score` (f64: the `ts_rank` computed score)
  - `created_at` (DateTime: entity creation timestamp)

## API Changes
- `GET /api/v2/search` — MODIFY: Response body changes to `PaginatedResults<SearchResultItem>` where each item includes `entity_type`, `entity_id`, `title`, `snippet`, `relevance_score`, and `created_at` fields. Total count metadata is provided by the `PaginatedResults` wrapper.

## Implementation Notes
- Follow the model directory pattern used by other modules:
  `modules/fundamental/src/sbom/model/summary.rs` and
  `modules/fundamental/src/advisory/model/summary.rs` each define model structs under a
  `model/` directory. Create `modules/search/src/model/mod.rs` following this convention.
- The `SearchResultItem` struct should derive `Serialize`, `Deserialize`, `Debug`, `Clone`
  to match existing model struct conventions (inspect `SbomSummary` and `AdvisorySummary`
  for the exact derive macro set).
- Use PostgreSQL `ts_headline('english', <text_column>, query)` to generate the `snippet`
  field — this automatically highlights matching terms in the text excerpt. The service
  query must select `ts_headline` alongside result rows.
- Wrap the result list in `PaginatedResults<SearchResultItem>` from
  `common/src/model/paginated.rs` to maintain consistency with all other list endpoints
  in the application.
- The `entity_type` discriminator should be set based on which table the result came from
  (sbom, advisory, or package). Use a string enum or const values.
- Consider backward compatibility: if existing consumers depend on the current response
  shape, document the breaking change. Since the feature is about improving search,
  a response shape change is expected and acceptable.
- Per constraints §5.3: follow the patterns referenced in these Implementation Notes.
- Per constraints §5.8: compare against sibling model implementations (`SbomSummary`,
  `AdvisorySummary`, `PackageSummary`) for parity on derive macros, serialization
  attributes, and field naming conventions.

## Reuse Candidates
- `common/src/model/paginated.rs` — `PaginatedResults<T>` wrapper for paginated list
  responses. Reuse directly for the search response.
- `modules/fundamental/src/sbom/model/summary.rs` — `SbomSummary` struct. Reference
  for model struct patterns (derives, field types, serde attributes).
- `modules/fundamental/src/advisory/model/summary.rs` — `AdvisorySummary` struct.
  Reference for model conventions and severity-related field patterns.
- `modules/fundamental/src/package/model/summary.rs` — `PackageSummary` struct.
  Another reference for consistent model struct conventions.

## Acceptance Criteria
- [ ] `SearchResultItem` struct is defined in `modules/search/src/model/mod.rs` with all required fields
- [ ] Search endpoint returns `PaginatedResults<SearchResultItem>`
- [ ] Each result item includes a `relevance_score` field with a positive value for matching results
- [ ] Each result item includes an `entity_type` discriminator ("sbom", "advisory", or "package")
- [ ] Each result item includes a `snippet` field with highlighted matching terms
- [ ] Each result item includes `entity_id`, `title`, and `created_at` metadata
- [ ] Response is valid JSON and correctly serialized by serde
- [ ] Breaking change to response shape is documented if the previous format differed

## Test Requirements
- [ ] Integration test: search results include `relevance_score` field with values > 0.0
- [ ] Integration test: search results include correct `entity_type` for each result
- [ ] Integration test: search results include `snippet` field with non-empty highlighted text
- [ ] Integration test: response deserializes correctly into `PaginatedResults<SearchResultItem>`
- [ ] Integration test: results are ordered by `relevance_score` descending

## Documentation Updates
- `README.md` — Document the updated `GET /api/v2/search` response schema with the new `SearchResultItem` fields and any breaking changes from the previous response format

## Dependencies
- Depends on: Task 2 — Refactor SearchService to use full-text search with relevance ranking
