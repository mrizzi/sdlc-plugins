# TC-9202: Add package search functionality -- Clarification Required

## Step 0 -- Validate Project Configuration

The project's CLAUDE.md contains all required sections:

1. **Repository Registry** -- present, lists `trustify-backend` with Serena instance `serena_backend`
2. **Jira Configuration** -- present, includes Project key (TC), Cloud ID, Feature issue type ID, and custom fields
3. **Code Intelligence** -- present, documents `serena_backend` instance with `rust-analyzer`

Configuration is valid. Proceeding to task analysis.

## Step 1 -- Fetch and Parse Jira Task

I would fetch the task using `jira.get_issue(TC-9202)` and parse its structured description. Based on the task description provided, here is the parsed content:

| Section | Status |
|---|---|
| Repository | Present: `trustify-backend` |
| Description | Present: "Add search capabilities to the package module so users can find packages more easily." |
| Files to Modify | Present: `modules/fundamental/src/package/endpoints/mod.rs` |
| Files to Create | Present: `modules/fundamental/src/package/endpoints/search.rs` |
| API Changes | **MISSING** |
| Implementation Notes | **MISSING** |
| Acceptance Criteria | Present but **vague** (see below) |
| Test Requirements | Present but **vague** (see below) |
| Dependencies | Not listed (assumed none) |

### Missing Implementation Notes

The task description does not include an **Implementation Notes** section. This section is critical for a search feature because it specifies the technical approach the implementation should follow. Without it, fundamental architectural decisions are undefined:

- Should this use PostgreSQL full-text search (`tsvector`/`tsquery`), SQL `LIKE`/`ILIKE` queries, or integrate with the existing `modules/search/` service (`SearchService`) that already provides full-text search across entities?
- What query builder patterns from `common/src/db/query.rs` should be used for filtering and pagination?
- Which `PackageSummary` fields should be indexed or searchable?
- Should the search endpoint follow the same patterns as the existing `list.rs` endpoint or the global `modules/search/endpoints/mod.rs` endpoint?

Without this guidance, I would be guessing at the intended architecture, which violates the skill's constraint: "If the structured description is incomplete, ask the user for clarification and stop execution immediately."

### Missing API Changes

The task does not include an **API Changes** section. For a new search endpoint, this section should specify:

- The endpoint path (e.g., `GET /api/v2/package/search` vs. adding to `GET /api/v2/search`)
- The HTTP method
- Query parameters (search term, filters, pagination, sorting)
- The response shape (presumably `PaginatedResults<PackageSummary>` following the existing pattern)

### Vague Acceptance Criteria

The acceptance criteria are too imprecise to implement against:

- **"Users can search for packages"** -- This is minimally actionable but does not specify what constitutes a "search." Is it a keyword search against the package name? A full-text search across multiple fields? A filtered list query?
- **"Search results are relevant"** -- This is not actionable. "Relevant" is undefined. Does this mean exact match on package name? Substring match? Full-text search with ranking? Should results be sorted by relevance score (e.g., using PostgreSQL `ts_rank`), or by name, or by recency?
- **"Performance is acceptable"** -- This provides no measurable threshold. "Acceptable" could mean under 100ms, under 1 second, or under 5 seconds. Without a concrete target, there is no way to verify this criterion or choose an appropriate implementation strategy (e.g., whether a database index is needed, whether to use the existing `tower-http` caching middleware).

### Vague Test Requirements

The test requirements state only "Test that search works correctly." This does not define what "correctly" means. There are no specifications for:

- Edge cases: empty query string, no matching results, special characters in search term
- Expected result ordering or ranking
- Pagination behavior (page size, total count)
- Error handling scenarios (invalid query parameters, database errors)
- Performance testing or load expectations
- Which test patterns to follow from `tests/api/` (the existing `sbom.rs`, `advisory.rs`, and `search.rs` integration tests)

## Execution Halted -- Clarifying Questions

Per the skill's rules, I am stopping execution immediately because the structured description is incomplete. I am not proceeding with branching, implementation planning, or code changes.

I need answers to the following questions before I can proceed:

1. **What should the Implementation Notes contain?** Specifically:
   - Should this search integrate with the existing `modules/search/` service (`SearchService` at `GET /api/v2/search`), or should it be a standalone endpoint under the package module (`GET /api/v2/package/search`) as the Files to Create section implies?
   - What search mechanism should be used? Options include PostgreSQL full-text search (`tsvector`/`tsquery`), SQL `ILIKE` queries, or delegating to the existing `SearchService`.
   - Which existing code patterns should be followed? The repository has both `list.rs` endpoints (simple filtered lists) and the `modules/search/` module (full-text search). The approach differs significantly depending on which pattern to follow.

2. **Which fields should be searchable?** The `PackageSummary` struct exists in `modules/fundamental/src/package/model/summary.rs` and includes a `license` field. Should search cover only the package name, or also other fields such as version, license, or description? Should the search match against related entities (e.g., SBOMs linked to a package via `entity/src/sbom_package.rs`)?

3. **What are the API Changes?** What is the exact endpoint path, HTTP method, query parameter schema (search term parameter name, filter parameters, pagination parameters), and response format? Should the response use `PaginatedResults<PackageSummary>` from `common/src/model/paginated.rs` following the existing list endpoint pattern?

4. **What does "relevant" mean for search result ranking?** Should results be ranked by a relevance score (e.g., using PostgreSQL `ts_rank`), or is a simple filtered list sufficient? Should exact matches appear before partial matches? Is there a relevance model in the existing `modules/search/` service that should be reused?

5. **What is the concrete performance requirement?** What is the maximum acceptable response time for a search query? What is the expected dataset size (number of packages) this needs to perform well against? This determines whether a database index, caching via `tower-http` middleware, or other optimization strategy is needed.

6. **What are the specific test scenarios?** Should tests cover:
   - Empty search queries returning all or no results?
   - Queries with no matching results?
   - Queries with special characters?
   - Pagination of search results?
   - Relevance ordering verification?
   - Performance benchmarks?
   What fixtures or test data should be used, and should the tests follow the integration test pattern in `tests/api/search.rs`?

Please provide clarification on these points so I can proceed with a correct and complete implementation.
