# implement-task TC-9202 -- Analysis and Clarification Required

## Step 0 -- Validate Project Configuration

Project Configuration in CLAUDE.md has been validated:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena instance `serena_backend`.
2. **Jira Configuration** -- present, contains Project key (`TC`), Cloud ID, and Feature issue type ID.
3. **Code Intelligence** -- present, with tool naming convention (`mcp__<serena-instance>__<tool>`) and configured instance `serena_backend` using `rust-analyzer`.

Validation: PASS. Proceeding to Step 1.

---

## Step 1 -- Fetch and Parse Jira Task

Parsing the structured description of TC-9202 against the required task template sections:

| Section | Status | Content |
|---|---|---|
| Repository | Present | `trustify-backend` |
| Target Branch | Present | `main` |
| Description | Present but vague | "Add search capabilities to the package module so users can find packages more easily." |
| Files to Modify | Present but incomplete | Only lists `modules/fundamental/src/package/endpoints/mod.rs` |
| Files to Create | Present but incomplete | Only lists `modules/fundamental/src/package/endpoints/search.rs` |
| API Changes | **MISSING** | No endpoint specification (path, method, query parameters, response shape) |
| Implementation Notes | **MISSING** | No patterns, code references, or reuse candidates referenced |
| Acceptance Criteria | Present but **vague and non-verifiable** | All three criteria are subjective, not pass/fail |
| Test Requirements | Present but **vague and non-verifiable** | Single item "Test that search works correctly" is not actionable |
| Verification Commands | Absent (optional) | -- |
| Target PR | Absent (optional) | -- |
| Review Context | Absent (optional) | -- |
| Bookend Type | Absent (optional) | -- |
| Dependencies | Absent (optional) | -- |

### Identified Gaps

**The structured description is incomplete. Execution must stop here per constraint 1.6: "implement-task MUST ask the user for clarification and stop execution when the structured description is incomplete -- it MUST NOT draft an implementation plan or proceed with any subsequent steps until the user responds."**

The following gaps must be resolved before implementation can proceed:

---

### Gap 1: Missing API Changes section

The task says "add search functionality" but does not specify the API contract. The following details are needed:

- **Endpoint path**: What is the route? Based on existing patterns (`/api/v2/package`), should it be `GET /api/v2/package/search` or a query parameter on the existing `GET /api/v2/package` endpoint (e.g., `?q=<search-term>`)?
- **HTTP method**: GET (most likely for search), but needs confirmation.
- **Query parameters**: What search parameters are supported? Full-text search (`q`), field-specific filters (e.g., `name`, `license`, `version`), pagination parameters (`offset`, `limit`)?
- **Response shape**: Should it return `PaginatedResults<PackageSummary>` (following the existing pattern in `common/src/model/paginated.rs`)? Or a different response type?
- **Search scope**: Which fields on the `Package` entity are searchable? Name only? Name and license? All fields?

### Gap 2: Missing Implementation Notes section

The task provides no guidance on how to implement the search. Critical questions:

- **Search mechanism**: Should this use the existing `SearchService` in `modules/search/` (which provides "full-text search across entities")? Or should this be a separate database-level query (e.g., SQL `LIKE`/`ILIKE` or PostgreSQL full-text search via `tsvector`/`tsquery`)? The repository already has a dedicated `modules/search/` module -- should the package search integrate with it or be independent?
- **Query builder integration**: Should the search use the shared query helpers in `common/src/db/query.rs` for filtering, pagination, and sorting? The existing `list.rs` endpoint likely uses these helpers already.
- **Existing patterns to follow**: The task should reference how `AdvisoryService` implements its `search` method (noted in `modules/fundamental/src/advisory/service/advisory.rs` which lists "fetch, list, search") as a sibling pattern. The `PackageService` currently only supports "fetch, list" -- does this task add a `search` method to `PackageService`, or does it integrate with the existing `SearchService`?
- **Reuse candidates**: The existing `modules/search/` module and `common/src/db/query.rs` helpers are likely reuse candidates but are not mentioned.

### Gap 3: Vague Acceptance Criteria (not pass/fail verifiable)

The current acceptance criteria are subjective and cannot be verified:

- "Users can search for packages" -- search by what? What constitutes a successful search? What input, what expected output?
- "Search results are relevant" -- what defines relevance? Exact match? Partial match? Ranking?
- "Performance is acceptable" -- what is acceptable? Response time threshold? Maximum result set size?

**Suggested replacement criteria (for user review):**

- [ ] `GET /api/v2/package/search?q=<term>` returns packages whose name contains the search term (or whatever the agreed endpoint and search field are)
- [ ] Search results are returned as `PaginatedResults<PackageSummary>` with pagination support (offset/limit)
- [ ] Empty search term returns a 400 Bad Request (or returns all packages -- needs specification)
- [ ] Search with no matching results returns an empty paginated result (not a 404)
- [ ] The search endpoint is registered in the package module's route configuration
- [ ] The search handler follows the existing error handling pattern (`Result<T, AppError>` with `.context()`)

### Gap 4: Vague Test Requirements (not actionable)

The current test requirement "Test that search works correctly" provides no guidance on what test cases to write.

**Suggested replacement (for user review):**

- [ ] Integration test: search by exact package name returns the matching package
- [ ] Integration test: search by partial package name returns matching packages
- [ ] Integration test: search with no matches returns an empty paginated result
- [ ] Integration test: search results include pagination metadata (total count)
- [ ] Integration test: search with invalid/missing query parameter returns appropriate error
- [ ] Tests are placed in `tests/api/` following the existing test file pattern (e.g., `tests/api/package.rs` or `tests/api/package_search.rs`)

### Gap 5: Incomplete Files to Modify / Files to Create

The task only lists the endpoint files but does not account for:

- **Service layer**: `modules/fundamental/src/package/service/mod.rs` needs a `search` method added to `PackageService` (or a new service file). This file is not listed in Files to Modify.
- **Route registration**: `modules/fundamental/src/package/endpoints/mod.rs` is listed (to add the search route), but the server mount point in `server/src/main.rs` may also need changes if the search endpoint requires separate registration.
- **Test files**: No test file is listed in Files to Create. Based on the repo structure, a test file like `tests/api/package_search.rs` (or additions to an existing package test file) would be needed, plus updating `tests/` module declarations.
- **Entity/query**: If search requires new database queries, `common/src/db/query.rs` or entity files might need modifications.

---

## Questions for the User

Before I can proceed with implementation, I need the following clarifications:

1. **API Design**: What should the search endpoint look like? Specifically: the route path, HTTP method, query parameters, and response format.

2. **Search Mechanism**: Should this integrate with the existing `modules/search/` module (`SearchService`), follow the pattern from `AdvisoryService` which already has search capability, or use a different approach (e.g., direct SQL query)?

3. **Search Scope**: Which `Package` entity fields should be searchable (name, license, version, etc.)?

4. **Service Layer**: Should a `search` method be added to the existing `PackageService` in `modules/fundamental/src/package/service/mod.rs`? This file is not listed in Files to Modify but is almost certainly impacted.

5. **Acceptance Criteria**: Can you provide specific, verifiable acceptance criteria? The current ones ("relevant", "acceptable performance") are subjective and cannot be programmatically verified.

6. **Test Requirements**: Can you specify the concrete test scenarios expected? At minimum: what inputs, what expected outputs, what error cases?

7. **Files to Modify**: Should the task include the service file (`service/mod.rs`) and test files in the file scope?

**I am stopping execution here and will not proceed with branching, implementation planning, or code changes until these gaps are resolved.**
