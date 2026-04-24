# Task 4 — Extend search endpoint response with relevance score and metadata

## Repository
trustify-backend

## Description
Update the search endpoint response model to include relevance score per result and
enhanced metadata (entity type discriminator, total count per entity type). This provides
the API consumers with the information needed to display search results meaningfully —
showing why a result matched (relevance score) and what kind of entity it is (type
discriminator). The response must remain compatible with the existing `PaginatedResults<T>`
wrapper.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Update the endpoint handler to serialize the
  new response structure including relevance scores and entity type metadata
- `modules/search/src/service/mod.rs` — Ensure the service returns relevance scores and
  entity type information alongside results

## Files to Create
- `modules/search/src/model/mod.rs` — Define `SearchResultItem` struct with fields:
  - `entity_type` (string: "sbom", "advisory", "package")
  - `entity_id` (string/uuid: the entity's primary key)
  - `title` (string: display name of the entity)
  - `snippet` (string: text excerpt showing matched context)
  - `relevance_score` (f64: the `ts_rank` score)
  - `created_at` (datetime: entity creation timestamp)

## API Changes
- `GET /api/v2/search` — MODIFY: Response body changes from generic results to structured
  `PaginatedResults<SearchResultItem>` with:
  - Each item includes `entity_type`, `entity_id`, `title`, `snippet`, `relevance_score`, `created_at`
  - Response metadata includes `total` count

## Implementation Notes
- Follow the model pattern used in other modules: `modules/fundamental/src/sbom/model/summary.rs`
  and `modules/fundamental/src/advisory/model/summary.rs` use dedicated struct files under
  a `model/` directory. Create `modules/search/src/model/mod.rs` following this pattern.
- The `SearchResultItem` struct should derive `Serialize`, `Deserialize`, `Debug`, `Clone`
  to match the patterns in existing model structs.
- Use `ts_headline()` PostgreSQL function to generate the `snippet` field — this highlights
  matching terms in the text excerpt. The `SearchService` query should select
  `ts_headline('english', <text_column>, query)` alongside the result rows.
- Wrap results in `PaginatedResults<SearchResultItem>` from `common/src/model/paginated.rs`
  to maintain consistency with all other list endpoints.
- The `entity_type` discriminator should be a string enum, set based on which table the
  result originated from.
- Per constraints §5.3: follow the patterns referenced in Implementation Notes.
- Per constraints §5.8: compare against sibling model implementations for parity on
  serialization, derive macros, and field conventions.

## Reuse Candidates
- `common/src/model/paginated.rs` — `PaginatedResults<T>` wrapper. Reuse directly for
  the search response.
- `modules/fundamental/src/sbom/model/summary.rs` — `SbomSummary` struct as a reference
  for model struct patterns (derives, field types, serialization).
- `modules/fundamental/src/advisory/model/summary.rs` — `AdvisorySummary` struct as
  another reference for model conventions.

## Acceptance Criteria
- [ ] `SearchResultItem` struct is defined with all required fields
- [ ] Search endpoint returns `PaginatedResults<SearchResultItem>`
- [ ] Each result item includes a `relevance_score` field with a non-zero value for matching results
- [ ] Each result item includes an `entity_type` discriminator
- [ ] Each result item includes a `snippet` with highlighted matching terms
- [ ] Response is valid JSON and can be deserialized by API consumers
- [ ] Existing API consumers that depend on the search endpoint response shape are considered (document breaking changes if any)

## Test Requirements
- [ ] Integration test: search results include `relevance_score` field with values > 0.0
- [ ] Integration test: search results include correct `entity_type` for each result
- [ ] Integration test: search results include `snippet` field with non-empty text
- [ ] Integration test: response deserializes correctly into `PaginatedResults<SearchResultItem>`
- [ ] Integration test: results are ordered by `relevance_score` descending

## Documentation Updates
- `README.md` — Document the updated search endpoint response schema with the new
  `SearchResultItem` fields

## Dependencies
- Depends on: Task 2 — Refactor SearchService to use full-text search with relevance ranking
