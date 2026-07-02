# implement-task: TC-9202

## Step 0 -- Validate Project Configuration

Reading the project's CLAUDE.md to verify required sections under `# Project Configuration`:

1. **Repository Registry** -- Present. Contains one entry: `trustify-backend` with Serena instance `serena_backend` at path `./`.
2. **Jira Configuration** -- Present. Contains Project key (`TC`), Cloud ID, Feature issue type ID, Git Pull Request custom field, and GitHub Issue custom field.
3. **Code Intelligence** -- Present. Documents the tool naming convention (`mcp__<serena-instance>__<tool>`) and lists the `serena_backend` instance with `rust-analyzer`.

All required Project Configuration sections are present. Proceeding to Step 1.

## Step 1 -- Fetch and Parse Jira Task

Fetching task TC-9202. Parsing the structured description against the expected template sections:

| Section | Status | Details |
|---|---|---|
| Repository | Present | `trustify-backend` |
| Target Branch | Present | `main` |
| Description | Present but vague | "Add search capabilities to the package module so users can find packages more easily." -- does not specify search type (full-text, filter-based, fuzzy), which fields are searchable, or how the search integrates with existing infrastructure. |
| Files to Modify | Present | 1 file listed (`modules/fundamental/src/package/endpoints/mod.rs`) |
| Files to Create | Present | 1 file listed (`modules/fundamental/src/package/endpoints/search.rs`) |
| API Changes | **MISSING** | For a new search endpoint, this section should specify the HTTP method, URL path, query parameters, request/response shapes, and pagination behavior. |
| Implementation Notes | **MISSING** | This section is required to reference existing code patterns, reusable utilities, and concrete examples from the codebase. Without it, the implementer has no guidance on which patterns to follow (e.g., how `AdvisoryService` implements its existing search, how `common/src/db/query.rs` query helpers should be used, whether to integrate with the `modules/search/` full-text search service). |
| Acceptance Criteria | Present but vague | All three criteria are non-measurable (see details below). |
| Test Requirements | Present but vague | Single criterion with no specific test scenarios (see details below). |
| Dependencies | Not present | (Optional section -- not a gap.) |

### Specific gaps identified

**1. Missing Implementation Notes (required)**

The task provides no guidance on:
- Which existing search patterns to follow. The repository has an `AdvisoryService` with a `search` method in `modules/fundamental/src/advisory/service/advisory.rs` and a dedicated `modules/search/` module with `SearchService` for full-text search. Should the package search reuse one of these patterns?
- How to use the shared query helpers in `common/src/db/query.rs` for filtering, pagination, and sorting.
- Whether to use SeaORM query builder patterns or raw SQL for the search logic.
- What the `PackageService` in `modules/fundamental/src/package/service/mod.rs` currently provides and how the search method should integrate with it.

**2. Missing API Changes (required for endpoint tasks)**

The task creates a new search endpoint but does not specify:
- The HTTP method and URL path (e.g., `GET /api/v2/package/search?q=...` or `GET /api/v2/package?search=...`).
- Query parameters (search term, filters, pagination parameters, sort options).
- Response shape (should it return `PaginatedResults<PackageSummary>` consistent with the list endpoint, or a different structure?).

**3. Vague Acceptance Criteria**

The three acceptance criteria are not measurable:

- "Users can search for packages" -- What constitutes a search? Full-text search across all fields? Filtering by specific fields (name, version, license)? Partial matching? Exact matching? What query parameters does the user provide?
- "Search results are relevant" -- How is relevance defined? Is there ranking? What makes a result relevant vs. irrelevant? Is this full-text relevance scoring, or simply "results match the query"?
- "Performance is acceptable" -- What is acceptable? Is there a latency target (e.g., < 200ms for typical queries)? A result set size limit? Should the endpoint support pagination?

**4. Vague Test Requirements**

- "Test that search works correctly" -- This provides no actionable test scenarios. Should tests cover: successful search with results, search with no results, search with special characters, pagination of search results, search by specific fields, case sensitivity, SQL injection prevention, performance under load?

## Execution Stopped -- Clarification Required

Per the implement-task skill process (Step 1) and constraint 1.6, I am stopping execution because the task description is incomplete. I will not draft an implementation plan, create branches, or proceed with any subsequent steps until the missing information is provided.

### Questions for clarification

1. **Search mechanism**: Should this use the existing `SearchService` in `modules/search/` (full-text search across entities), or should it be a query-parameter-based filter on the package list endpoint (similar to how `AdvisoryService` implements search)? Or is this a new dedicated search within the package module only?

2. **API design**: What is the endpoint specification?
   - HTTP method and path (e.g., `GET /api/v2/package/search?q=<term>` or query parameters on the existing list endpoint)?
   - Which fields are searchable (package name, version, license, purl)?
   - Should results be paginated using `PaginatedResults<PackageSummary>`?
   - Are there filter or sort parameters beyond the search term?

3. **Implementation patterns**: Which existing code should serve as the reference pattern?
   - The `AdvisoryService::search` method in `modules/fundamental/src/advisory/service/advisory.rs`?
   - The shared query helpers in `common/src/db/query.rs`?
   - The `SearchService` in `modules/search/src/service/mod.rs`?

4. **Acceptance Criteria specifics**:
   - What fields should be searched when the user provides a query term?
   - Is there a performance target (e.g., response time, maximum result set)?
   - Should relevance ranking be implemented, or is this a simple contains/prefix match?

5. **Test Requirements specifics**:
   - What specific test scenarios should be covered (e.g., search with results, empty results, special characters, pagination, field-specific search)?
   - Should integration tests follow the pattern in `tests/api/search.rs` or `tests/api/advisory.rs`?

Please provide the missing Implementation Notes, API Changes, measurable Acceptance Criteria, and specific Test Requirements so I can proceed with the implementation.
