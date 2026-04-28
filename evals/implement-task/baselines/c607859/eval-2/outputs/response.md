# implement-task: TC-9202 — Add package search functionality

## Step 0 — Validate Project Configuration

The project's CLAUDE.md (claude-md-mock.md) contains all required sections:

1. **Repository Registry** — present, lists `trustify-backend` with Serena instance `serena_backend`.
2. **Jira Configuration** — present, includes Project key (`TC`), Cloud ID, Feature issue type ID, and custom fields.
3. **Code Intelligence** — present, with tool naming convention (`mcp__<serena-instance>__<tool>`) and configured instance `serena_backend` using `rust-analyzer`.

Project Configuration is valid. Proceeding.

## Step 1 — Fetch and Parse Jira Task

Parsed the task description for TC-9202. Evaluating the structured sections against the expected template:

| Section | Status | Content |
|---|---|---|
| Repository | Present | `trustify-backend` |
| Description | Present but vague | "Add search capabilities to the package module so users can find packages more easily." |
| Files to Modify | Present but incomplete | Lists only `modules/fundamental/src/package/endpoints/mod.rs` |
| Files to Create | Present but incomplete | Lists only `modules/fundamental/src/package/endpoints/search.rs` |
| API Changes | **MISSING** | No endpoint specification (path, method, query parameters, response shape) |
| Implementation Notes | **MISSING** | No patterns, code references, or reuse guidance provided |
| Acceptance Criteria | Present but vague | All three criteria are subjective and non-verifiable ("relevant", "acceptable") |
| Test Requirements | Present but vague | Single item: "Test that search works correctly" — no specific scenarios |
| Target PR | Not present (optional) | N/A |
| Review Context | Not present (optional) | N/A |
| Dependencies | Not present | N/A |

## Identified Gaps — Execution Halted

Per SKILL.md section "Important Rules" (constraint on incomplete descriptions):

> "If the structured description is incomplete, ask the user for clarification and **stop execution immediately**. Do not draft an implementation plan, create branches, or proceed with any subsequent steps until the user provides the missing information."

The task description for TC-9202 is incomplete. The following gaps must be resolved before implementation can proceed:

### Gap 1: Missing API Changes section

The task says "add search route" and "search endpoint handler" but does not specify:

- **Endpoint path**: What is the URL? (e.g., `GET /api/v2/package/search` or `GET /api/v2/package?q=...`)
- **HTTP method**: GET with query parameters? POST with a request body?
- **Query/request parameters**: What fields can be searched? (package name, version, license, pURL?) What filtering, pagination, and sorting parameters are supported?
- **Response shape**: What does the response look like? Does it return `PaginatedResults<PackageSummary>` consistent with the existing list endpoint, or a different structure?

### Gap 2: Missing Implementation Notes section

No guidance is provided on:

- **Which search mechanism to use**: The repository has a dedicated `modules/search/` module with a `SearchService` for full-text search across entities. Should the package search integrate with this existing `SearchService`, or should it implement its own search logic at the database query level using the `common/src/db/query.rs` helpers?
- **Search strategy**: Full-text search (PostgreSQL `tsvector`/`tsquery`)? Simple `LIKE`/`ILIKE` filtering? Integration with an external search index?
- **Code patterns to follow**: Which existing implementations to reference? The `advisory` module has a `search` method in its `AdvisoryService` — should the package search follow that pattern?
- **Service layer changes**: The task lists only endpoint files, but `modules/fundamental/src/package/service/mod.rs` (`PackageService`) likely needs a new `search` method. This file is not listed in Files to Modify.
- **Reusable code**: No mention of existing utilities to leverage (e.g., `common/src/db/query.rs` for query building, `common/src/model/paginated.rs` for response wrapping).

### Gap 3: Vague Acceptance Criteria

The current acceptance criteria are not verifiable:

- "Users can search for packages" — by what fields? What constitutes a "search"?
- "Search results are relevant" — what relevance criteria? Exact match? Partial match? Ranked?
- "Performance is acceptable" — what threshold? Response time target? Maximum result set size?

These need to be rewritten as concrete, testable statements. For example:
- "Users can search packages by name using a `q` query parameter"
- "Search returns packages whose name contains the query string (case-insensitive)"
- "Search results are paginated using `PaginatedResults<PackageSummary>`"
- "Search endpoint responds within 500ms for queries against 10,000 packages"

### Gap 4: Vague Test Requirements

"Test that search works correctly" does not specify:

- What test scenarios are needed (empty query, partial match, no results, pagination, special characters)?
- Where test files should be created (presumably `tests/api/package.rs` or a new `tests/api/package_search.rs`, following the pattern in `tests/api/search.rs`)?
- What assertions to make on response status codes and body structure?

### Gap 5: Incomplete Files to Modify

The task lists only the endpoint registration file (`endpoints/mod.rs`) but the service layer (`service/mod.rs`) almost certainly needs modification to add a search method to `PackageService`. If the `modules/search/` module is involved, its files may also need modification.

## Questions for the User

Before proceeding, please provide clarification on the following:

1. **API specification**: What is the exact endpoint path, HTTP method, and query parameter schema for the package search? What response shape should it return?

2. **Search mechanism**: Should this integrate with the existing `SearchService` in `modules/search/`, or implement search at the `PackageService` level using database query helpers from `common/src/db/query.rs`?

3. **Searchable fields**: Which package fields should be searchable? (e.g., name, version, license, pURL, description)

4. **Service layer scope**: Should `modules/fundamental/src/package/service/mod.rs` be added to Files to Modify for adding a `search` method to `PackageService`?

5. **Concrete acceptance criteria**: Can you provide measurable acceptance criteria with specific behavior expectations and performance thresholds?

6. **Test scenarios**: What specific test cases should be covered? (e.g., search with results, search with no results, search with pagination, search with invalid input)

Please provide the missing information so I can resume implementation from Step 2.
