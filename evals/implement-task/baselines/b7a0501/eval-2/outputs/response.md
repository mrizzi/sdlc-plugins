# implement-task: TC-9202 -- Evaluation Response

## Step 0 -- Validate Project Configuration

The project's CLAUDE.md contains the required sections:

- **Repository Registry** -- present with `trustify-backend` entry mapped to Serena instance `serena_backend`.
- **Jira Configuration** -- present with Project key (`TC`), Cloud ID, and Feature issue type ID.
- **Code Intelligence** -- present with tool naming convention and `serena_backend` instance configured for `rust-analyzer`.

Project Configuration is valid. Proceeding to Step 1.

## Step 1 -- Fetch and Parse Jira Task

Parsing the structured description for TC-9202 against the expected template sections:

| Section | Status | Detail |
|---|---|---|
| Repository | Present | `trustify-backend` |
| Description | Present | "Add search capabilities to the package module so users can find packages more easily." |
| Files to Modify | Present | `modules/fundamental/src/package/endpoints/mod.rs` |
| Files to Create | Present | `modules/fundamental/src/package/endpoints/search.rs` |
| **API Changes** | **MISSING** | No API Changes section is provided. The task involves adding a search endpoint, so the HTTP method, path, query parameters, request/response shapes, and status codes must be specified. |
| **Implementation Notes** | **MISSING** | No Implementation Notes section is provided. This section is critical -- it should reference existing code patterns, reusable utilities, and specific guidance on how to implement the search (e.g., which query builder helpers from `common/src/db/query.rs` to use, whether to use the existing `modules/search/` infrastructure or build a module-local search, what filtering/pagination patterns to follow, how to integrate with `PackageService`). |
| Acceptance Criteria | Present but **VAGUE** | See analysis below. |
| Test Requirements | Present but **VAGUE** | See analysis below. |
| Target PR | Absent (optional) | Not applicable -- this is not a review feedback fix. |
| Review Context | Absent (optional) | Not applicable. |
| Dependencies | Absent | No dependencies listed -- acceptable if there are none. |

### Detailed Issues

#### 1. Missing: API Changes

The task adds a search endpoint but does not specify:

- What is the endpoint path? (e.g., `GET /api/v2/package/search` or `GET /api/v2/package?q=...`)
- What HTTP method is used?
- What query parameters does the search accept? (e.g., `q`, `filter`, `limit`, `offset`)
- What is the response shape? (e.g., `PaginatedResults<PackageSummary>` or a different search-specific response type?)
- What status codes should be returned for success, empty results, and invalid queries?

#### 2. Missing: Implementation Notes

The task provides no guidance on how to implement the search. Key unknowns include:

- **Search strategy**: Should this use the existing `modules/search/` module (which provides `SearchService` for full-text search across entities), or should it be a module-local search using SQL `LIKE`/`ILIKE` queries, or full-text search via PostgreSQL `tsvector`?
- **Reusable code**: The repository has `common/src/db/query.rs` with shared query builder helpers for filtering, pagination, and sorting. Should the search endpoint use these? Are there other utilities to reuse?
- **Service layer**: Should a new method be added to `PackageService` (in `modules/fundamental/src/package/service/mod.rs`), or should the search endpoint call `SearchService` directly?
- **Searchable fields**: Which fields of a package are searchable? (e.g., name, version, license, purl)
- **Pattern reference**: No sibling endpoint or existing search implementation is referenced as a pattern to follow. The `advisory` module has a `search` method in `AdvisoryService` -- should this be used as a reference pattern?

#### 3. Vague: Acceptance Criteria

The acceptance criteria are too vague to verify:

- "Users can search for packages" -- by what mechanism? What constitutes a valid search query? What fields are searched?
- "Search results are relevant" -- what defines relevance? Is there ranking? Is partial matching required? Is fuzzy matching expected?
- "Performance is acceptable" -- what is the performance threshold? Is there a maximum response time (e.g., < 200ms for 95th percentile)? Is there a maximum dataset size to consider?

Each criterion should be specific and objectively verifiable.

#### 4. Vague: Test Requirements

The test requirements consist of a single item: "Test that search works correctly." This is insufficient:

- No specific test scenarios are described (e.g., search with results, search with no results, search with special characters, search with pagination).
- No error cases are specified (e.g., empty query string, excessively long query).
- No performance or edge-case tests are mentioned.
- The test file location is not specified (e.g., should it be added to `tests/api/search.rs` or a new `tests/api/package_search.rs`?).

## Decision: STOP -- Clarification Required

The structured description for TC-9202 is **incomplete**. Per the skill's rules, I am stopping execution and will not draft an implementation plan, create branches, or proceed with any subsequent steps.

### Questions for the user

Before I can proceed with implementation, please provide the following information:

1. **API Changes**: What is the endpoint specification for package search?
   - HTTP method and path (e.g., `GET /api/v2/package/search?q={query}`)
   - Query parameters (search term, filters, pagination)
   - Response shape and status codes

2. **Implementation Notes**: How should the search be implemented?
   - Should it use the existing `SearchService` from `modules/search/`, or implement a module-local search in `PackageService`?
   - What search strategy should be used (SQL LIKE, PostgreSQL full-text search, etc.)?
   - Which package fields should be searchable?
   - What existing code patterns or sibling implementations should be followed?

3. **Acceptance Criteria**: Can you make these specific and verifiable?
   - What fields are included in the search? (e.g., package name, version, purl, license)
   - What matching behavior is expected? (exact, prefix, substring, fuzzy)
   - What is the concrete performance target? (e.g., "responds within 500ms for up to 10,000 packages")

4. **Test Requirements**: What specific test scenarios should be covered?
   - Example: search returns matching packages, search returns empty results for non-matching query, search with pagination, search with invalid input
   - Where should the test file be located?

Please update the task description with this information, and I will proceed with implementation.
