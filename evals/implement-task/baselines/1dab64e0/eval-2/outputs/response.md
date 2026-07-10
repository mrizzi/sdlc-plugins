# implement-task TC-9202 — Execution Stopped: Incomplete Task Description

## Step 0 — Validate Project Configuration

Verified that the project's CLAUDE.md contains the required Project Configuration sections:

1. **Repository Registry** — present, contains `trustify-backend` with Serena instance `serena_backend` and path `./`.
2. **Jira Configuration** — present, contains Project key (`TC`), Cloud ID, and Feature issue type ID.
3. **Code Intelligence** — present, with tool naming convention `mcp__<serena-instance>__<tool>` and configured instance `serena_backend` using `rust-analyzer`.

Project Configuration is valid. Proceeding to Step 1.

## Step 1 — Fetch and Parse Jira Task

Fetched task TC-9202. Parsed the structured description and found the following:

### Sections present

| Section | Status | Content |
|---|---|---|
| Repository | Present | `trustify-backend` |
| Target Branch | Present | `main` |
| Description | Present but vague | "Add search capabilities to the package module so users can find packages more easily." |
| Files to Modify | Present but minimal | 1 file listed |
| Files to Create | Present but minimal | 1 file listed |
| Acceptance Criteria | Present but vague | 3 items, all subjective and unmeasurable |
| Test Requirements | Present but vague | 1 item, no specific scenarios |
| Target PR | Not present | (optional — acceptable) |
| Review Context | Not present | (optional — acceptable) |
| Bookend Type | Not present | (optional — acceptable) |

### Sections missing entirely

| Section | Required? | Notes |
|---|---|---|
| **API Changes** | Yes | No endpoint path, HTTP method, request parameters, query parameters, or response shape defined. The task adds a search endpoint but does not specify the API contract. |
| **Implementation Notes** | Yes | No patterns, code references, or guidance on how to implement the search. No reference to existing utilities like `common/src/db/query.rs` (shared query builder), `modules/search/` (existing search module), or the `PackageService` in `modules/fundamental/src/package/service/mod.rs`. |
| **Dependencies** | No (optional) | Not present — acceptable if there are no dependencies, but should be explicitly stated. |

### Vague or incomplete content in present sections

1. **Description** — "Add search capabilities to the package module so users can find packages more easily" is too vague to implement:
   - What fields should be searchable? (package name, version, license, PURL, ecosystem?)
   - What type of search? (full-text search via the existing `modules/search/` module? SQL LIKE/ILIKE queries? Filtered listing?)
   - Should search support pagination, sorting, or filtering? (The codebase uses `PaginatedResults<T>` and shared query helpers in `common/src/db/query.rs`)
   - Should this integrate with the existing `modules/search/` service, or is this a module-specific search endpoint?

2. **Acceptance Criteria** — All three criteria are subjective and unmeasurable:
   - "Users can search for packages" — via what endpoint? With what parameters? What constitutes a valid search?
   - "Search results are relevant" — what defines relevance? Exact match? Substring match? Fuzzy match? Ranked results?
   - "Performance is acceptable" — what is the latency target? What dataset size should it handle? Is there a response time SLA?

3. **Test Requirements** — "Test that search works correctly" specifies no concrete test scenarios:
   - No search-by-name test case
   - No empty-results test case
   - No pagination test case
   - No error handling test case (e.g., invalid query parameters)
   - No specification of whether tests should be integration tests in `tests/api/` (matching the existing pattern for `sbom.rs`, `advisory.rs`, `search.rs`) or unit tests

4. **Files to Modify / Files to Create** — The scope appears incomplete:
   - Only `endpoints/mod.rs` and `endpoints/search.rs` are listed, but adding search likely requires changes to the service layer (`modules/fundamental/src/package/service/mod.rs`) to add a search method to `PackageService`
   - No mention of whether `server/src/main.rs` needs updating for route mounting
   - No mention of model changes if search returns a different shape than `PackageSummary`

## Decision: Stop Execution

Per the implement-task skill's rules:

> "If any required section is missing or the description doesn't follow the template, list the gaps, ask the user for clarification, and stop execution immediately -- do not proceed with any subsequent steps (branching, implementation planning, code changes) until the user provides the missing information."

**Execution is stopped.** The task description is incomplete and cannot be implemented as-is.

## Clarification needed from user

Before proceeding, please provide the following information for TC-9202:

1. **API Changes**: What is the endpoint contract?
   - Endpoint path (e.g., `GET /api/v2/package/search?q={query}` or `GET /api/v2/package?search={query}`)
   - HTTP method
   - Query parameters (search term, filters, pagination params)
   - Response shape (reuse `PaginatedResults<PackageSummary>` or a new type?)

2. **Implementation Notes**: How should search be implemented?
   - Should this use the existing `SearchService` in `modules/search/`?
   - Or should it add filtering/search directly in `PackageService` using the shared query helpers in `common/src/db/query.rs`?
   - What existing patterns should be followed? (e.g., the advisory module's search implementation in `modules/fundamental/src/advisory/service/advisory.rs`)
   - Are there specific database columns or indexes to use?

3. **Acceptance Criteria**: What are measurable success conditions?
   - Which fields are searchable?
   - What matching behavior is expected (exact, substring, full-text)?
   - What is the performance target (e.g., < 200ms for 10k packages)?

4. **Test Requirements**: What specific scenarios should be tested?
   - Search with matching results
   - Search with no results (empty response)
   - Search with pagination
   - Search with invalid/empty query parameter
   - Should tests be integration tests in `tests/api/` following the existing pattern?

5. **Files to Modify / Files to Create**: Is the scope complete?
   - Does `PackageService` (`modules/fundamental/src/package/service/mod.rs`) need a new search method?
   - Does `server/src/main.rs` need route registration changes?
   - Are any model changes needed?

Please update the task description in Jira with the missing sections, or provide the information here so I can proceed with implementation.
