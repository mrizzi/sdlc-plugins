# implement-task: TC-9202 — Add package search functionality

## Project Configuration Validation

Project Configuration in CLAUDE.md is valid:
- Repository Registry contains `trustify-backend` with Serena instance `serena_backend`.
- Jira Configuration is present with project key `TC`, Cloud ID, and required custom field IDs.
- Code Intelligence section lists `serena_backend` with `rust-analyzer`.

The task's Repository field (`trustify-backend`) matches a configured repository. Validation passes.

## Task Description Analysis

I parsed the Jira task TC-9202 and checked it against the required template sections. The expected sections are: **Repository**, **Description**, **Files to Modify**, **Files to Create**, **API Changes**, **Implementation Notes**, **Acceptance Criteria**, **Test Requirements**.

### Sections Present

| Section | Status | Assessment |
|---|---|---|
| Repository | Present | `trustify-backend` -- matches Project Configuration |
| Description | Present | Very brief, but present |
| Files to Modify | Present | Lists one file |
| Files to Create | Present | Lists one file |
| Acceptance Criteria | Present | Three items listed, but problematically vague (see below) |
| Test Requirements | Present | One item listed, but problematically vague (see below) |

### Sections Missing Entirely

| Section | Status |
|---|---|
| **API Changes** | **MISSING** |
| **Implementation Notes** | **MISSING** |

## STOP: Gaps and Clarification Needed

**Execution is halted.** The task description does not follow the required template. Two sections are entirely missing and several present sections are too vague to implement without improvisation. Per constraint section 1.6 ("Ask vs improvise"), I must ask for clarification rather than proceed.

### 1. Missing: API Changes

The task adds a search endpoint but does not specify:
- What is the HTTP method and route path? (e.g., `GET /api/v2/package/search` or a query parameter on the existing `GET /api/v2/package`?)
- What query parameters does the search accept? (e.g., `q`, `name`, `license`, `page`, `limit`?)
- What is the response shape? (e.g., `PaginatedResults<PackageSummary>` or a new search-specific DTO?)
- What HTTP status codes should be returned for success, empty results, and errors?

### 2. Missing: Implementation Notes

There is no guidance on:
- Which search mechanism to use. The repository has a `modules/search/` module with a `SearchService` for full-text search. Should the package search integrate with this existing `SearchService`, or should it implement its own query-based filtering via `common/src/db/query.rs`?
- Whether a database migration is needed (e.g., adding a full-text search index on the `package` table).
- Whether the `PackageService` in `modules/fundamental/src/package/service/mod.rs` needs a new method, or whether the endpoint handler should call `SearchService` directly.
- Any caching requirements for the new search endpoint.

### 3. Vague: Acceptance Criteria

The three listed acceptance criteria are not actionable:
- **"Users can search for packages"** -- Search by what fields? Name only? Name and license? PURL? What constitutes a match (exact, prefix, substring, full-text)?
- **"Search results are relevant"** -- How is relevance defined? Is ranking required? What ordering should results use?
- **"Performance is acceptable"** -- What is the performance target? A specific latency threshold (e.g., p95 < 200ms)? A minimum dataset size the search must handle?

Each of these would require me to make arbitrary design decisions, which violates the ask-vs-improvise constraint.

### 4. Vague: Test Requirements

- **"Test that search works correctly"** -- This is a tautology, not a test requirement. Specific scenarios are needed, for example: test search with matching results, test search with no matches, test search with pagination, test search with special characters, test search with empty query string.

### 5. Incomplete: Files to Modify / Files to Create

Given the repository structure, the listed files may be incomplete:
- If a service-layer method is needed, `modules/fundamental/src/package/service/mod.rs` should likely appear in Files to Modify.
- If the search integrates with `SearchService`, files in `modules/search/` may need modification.
- No integration test file is mentioned (the repo has `tests/api/` for integration tests; a `tests/api/package.rs` or addition to an existing test file would be expected).
- If the route is mounted at the server level, `server/src/main.rs` may need modification.

---

## Questions for the User

Before I can proceed with branching, planning, or implementation, please provide the following:

1. **API Changes section**: What is the exact HTTP method, route path, query parameters, response type, and status codes for the new search endpoint?

2. **Implementation Notes section**: Should this integrate with the existing `SearchService` in `modules/search/`, or use direct database queries via the shared query helpers in `common/src/db/query.rs`? Is a database migration needed?

3. **Acceptance Criteria**: Please replace the vague criteria with specific, testable ones. What fields are searchable? What matching semantics apply (substring, prefix, full-text)? Is there a performance target?

4. **Test Requirements**: Please list specific test scenarios (e.g., search returns matching packages, search with no results returns empty paginated response, search handles pagination parameters).

5. **Files to Modify/Create**: Should the list be expanded to include the service layer, integration tests, and potentially the search module or server main?

I will resume implementation once these gaps are addressed.
