# implement-task TC-9202 -- Task Description Validation

## Step 0 -- Validate Project Configuration

The project's CLAUDE.md contains all required sections:

1. **Repository Registry** -- present, lists `trustify-backend` with Serena Instance `serena_backend` and Path `./`
2. **Jira Configuration** -- present, includes Project key (`TC`), Cloud ID, Feature issue type ID
3. **Code Intelligence** -- present, lists `serena_backend` instance with `rust-analyzer` language server and tool naming convention

Project Configuration is valid. Proceeding to Step 1.

## Step 1 -- Fetch and Parse Jira Task

Parsing the structured description for TC-9202 ("Add package search functionality").

### Parsed sections

| Section | Status | Content |
|---|---|---|
| Repository | Present | `trustify-backend` |
| Target Branch | Present | `main` |
| Description | Present (vague) | "Add search capabilities to the package module so users can find packages more easily." |
| Files to Modify | Present | `modules/fundamental/src/package/endpoints/mod.rs` |
| Files to Create | Present | `modules/fundamental/src/package/endpoints/search.rs` |
| API Changes | **MISSING** | Not provided |
| Implementation Notes | **MISSING** | Not provided |
| Acceptance Criteria | Present (vague) | See analysis below |
| Test Requirements | Present (vague) | See analysis below |
| Dependencies | Not present | (optional -- acceptable) |
| Target PR | Not present | (optional -- acceptable) |
| Bookend Type | Not present | (optional -- acceptable) |

### Identified Gaps

The task description has significant gaps that prevent implementation from proceeding.

#### 1. Missing Implementation Notes section (REQUIRED)

The **Implementation Notes** section is entirely absent. This section is critical because it provides:
- Patterns and code references to follow during implementation
- References to existing utilities, helpers, and shared modules to reuse
- Specific guidance on how the search should be integrated with existing code

Without this, there is no guidance on whether to use the existing `modules/search/` module's `SearchService` (which already provides full-text search across entities), or build a separate search mechanism within the package module. There is also no indication of which query builder patterns from `common/src/db/query.rs` to use.

#### 2. Missing API Changes section (REQUIRED for endpoint work)

The task involves adding a search route and endpoint handler, but there is no **API Changes** section specifying:
- The endpoint path (e.g., `GET /api/v2/package/search` vs. a query parameter on `GET /api/v2/package`)
- Request parameters (query string, path params, request body)
- Response shape and status codes

#### 3. Vague Acceptance Criteria

The acceptance criteria are not measurable:

- "Users can search for packages" -- does not specify which fields are searchable (name, version, license, purl, description, etc.) or what the search input format is (free text, structured query, filters).
- "Search results are relevant" -- does not define what "relevant" means. Is there a ranking algorithm? Should results be ordered by relevance score, alphabetically, or by recency? Is fuzzy matching required, or only exact/substring matching?
- "Performance is acceptable" -- does not define a performance threshold. What is the expected response time? What dataset size should it handle? Is there a target latency (e.g., < 200ms for 95th percentile)?

#### 4. Vague Test Requirements

The test requirements contain a single item -- "Test that search works correctly" -- which is insufficient to implement tests. There is no specification of:
- What constitutes a "correct" search result
- Which test scenarios to cover (empty query, no results, partial match, exact match, special characters, pagination)
- Whether integration tests against PostgreSQL are needed (the project convention per `repo-backend.md` uses real PostgreSQL test databases)
- Whether error cases should be tested (invalid input, database errors)

## Execution Halted -- Clarification Required

Per the implement-task skill specification: "If any required section is missing or the description doesn't follow the template, list the gaps, ask the user for clarification, and stop execution immediately."

**I am stopping execution and will not proceed with branching, implementation planning, code changes, or any subsequent steps until the following questions are answered.**

### Clarifying Questions

1. **Which fields should be searchable?** The `PackageSummary` struct in `modules/fundamental/src/package/model/summary.rs` includes at least a `license` field. Which package fields should the search query match against (e.g., package name, version, purl, license, description)? Should the search support filtering on specific fields, or is it a single free-text query across all fields?

2. **What does "relevant" mean for search results, and how should results be ranked?** Should results use PostgreSQL full-text search (`tsvector`/`tsquery`) with relevance scoring, simple `ILIKE`/substring matching, or integration with the existing `SearchService` in `modules/search/`? Should results be ranked by relevance score, or returned in a default order (e.g., alphabetical)? Is fuzzy matching (typo tolerance) required?

3. **What is the performance threshold?** What response time is considered "acceptable"? Is there a target latency (e.g., < 500ms at p95)? What is the expected dataset size (number of packages)? Should the endpoint support pagination via the existing `PaginatedResults<T>` pattern?

4. **What is the API contract?** What should the endpoint path be (e.g., `GET /api/v2/package/search?q=...` vs. adding a `q` parameter to the existing `GET /api/v2/package` list endpoint)? What query parameters should it accept? Should the response use the existing `PaginatedResults<PackageSummary>` wrapper, or a different shape?

5. **What test scenarios are required?** Should integration tests cover: successful search with results, search with no results, empty/missing query parameter, pagination of search results, special character handling? Should the tests follow the existing pattern in `tests/api/search.rs`?

6. **Should this reuse the existing search module?** The repository already has a `modules/search/` module with a `SearchService` providing full-text search across entities and a `GET /api/v2/search` endpoint. Should the package search integrate with this existing service, or be a standalone implementation within the package module?

Please provide the missing Implementation Notes, clarify the acceptance criteria and test requirements, and answer the questions above so I can proceed with implementation.
