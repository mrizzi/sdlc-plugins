# implement-task TC-9202 -- Execution Halted: Incomplete Task Description

## Step 0 -- Validate Project Configuration

Verified the project's CLAUDE.md contains all required sections under `# Project Configuration`:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena instance `serena_backend` and path `./`
2. **Jira Configuration** -- present, contains Project key (`TC`), Cloud ID (`2b9e35e3-6bd3-4cec-b838-f4249ee02432`), and Feature issue type ID (`10142`)
3. **Code Intelligence** -- present, documents tool naming convention (`mcp__<serena-instance>__<tool>`) and configured instance `serena_backend` with `rust-analyzer`

Project Configuration is valid. Proceeding to Step 1.

## Step 1 -- Fetch and Parse Jira Task

Fetched issue TC-9202. Parsing the structured description against the required template sections:

| Section | Status | Detail |
|---|---|---|
| Repository | Present | `trustify-backend` |
| Target Branch | Present | `main` |
| Description | **Incomplete** | Too vague to implement -- "Add search capabilities to the package module so users can find packages more easily" does not specify what kind of search (full-text, filtered query, pURL lookup), which fields are searchable, what the search API contract looks like, or how the search is executed (database query, existing SearchService integration, new index). |
| Files to Modify | Present but insufficient | Lists only `modules/fundamental/src/package/endpoints/mod.rs` -- no service-layer file is listed, yet a search feature would require service-layer logic (e.g., `modules/fundamental/src/package/service/mod.rs` for a `search` method on `PackageService`). |
| Files to Create | Present but insufficient | Lists only `modules/fundamental/src/package/endpoints/search.rs` -- no test file is listed despite the Test Requirements section existing. |
| API Changes | **Missing** | No API Changes section. A search endpoint requires specifying the route path (e.g., `GET /api/v2/package/search`), query parameters (search term, pagination, filters), and response shape. |
| Implementation Notes | **Missing** | No Implementation Notes section. There is no guidance on which patterns to follow, whether to integrate with the existing `modules/search/` SearchService or build a standalone query, what query builder helpers from `common/src/db/query.rs` to use, or how sibling search implementations (e.g., `AdvisoryService` which already has a `search` method) should be referenced. |
| Acceptance Criteria | **Incomplete** | The criteria are too vague to verify: "Users can search for packages" (by what mechanism?), "Search results are relevant" (what defines relevance?), "Performance is acceptable" (what threshold?). These are not testable or verifiable as written. |
| Test Requirements | **Incomplete** | "Test that search works correctly" is a single vague line with no specifics. It does not specify which test file to create or modify, what scenarios to cover (empty results, partial match, exact match, pagination, invalid input), or what assertions to make. |
| Dependencies | Not listed | No dependencies section (acceptable -- this is optional). |

## Execution Stopped -- Clarification Required

The structured description for TC-9202 is incomplete. The following gaps must be resolved before implementation can proceed. I will not draft an implementation plan, create branches, or proceed with any subsequent steps until you provide the missing information.

### Missing sections that must be added:

1. **API Changes** -- Please specify:
   - The endpoint route (e.g., `GET /api/v2/package/search` or `GET /api/v2/package?q=...`)
   - Query parameters (search term, pagination parameters, filters)
   - Response shape (e.g., `PaginatedResults<PackageSummary>` or a new response type)
   - HTTP method

2. **Implementation Notes** -- Please specify:
   - Which search approach to use: integrate with the existing `modules/search/` SearchService (full-text search across entities), or add a query-based search directly in `PackageService` using the shared query builder from `common/src/db/query.rs`
   - Which sibling implementations to follow as patterns (e.g., `AdvisoryService` already has a `search` method in `modules/fundamental/src/advisory/service/advisory.rs`)
   - Which fields of `PackageSummary` (or the underlying `package` entity) should be searchable
   - How search results should be sorted (relevance, name, date)

### Sections that need more detail:

3. **Description** -- Please clarify:
   - What type of search is intended (full-text search, filtered listing, pURL-based lookup, or combined)
   - Whether this is a new standalone endpoint or an extension of the existing `GET /api/v2/package` list endpoint with query parameters

4. **Files to Modify** -- Likely incomplete. Should it also include:
   - `modules/fundamental/src/package/service/mod.rs` (to add a search method to `PackageService`)
   - `server/src/main.rs` (if a new route group needs mounting)

5. **Files to Create** -- Likely incomplete. Should it also include:
   - A test file (e.g., `tests/api/package_search.rs` or additions to an existing package test file)

6. **Acceptance Criteria** -- Please make these specific and verifiable, for example:
   - "Search by package name substring returns matching packages"
   - "Search with no matches returns an empty paginated result (200 OK, zero items)"
   - "Search supports pagination via `offset` and `limit` query parameters"
   - "Search response time is under 500ms for datasets up to 10,000 packages"

7. **Test Requirements** -- Please specify concrete test scenarios, for example:
   - "Test search with a known package name returns that package in results"
   - "Test search with a non-existent term returns empty results"
   - "Test search pagination returns correct subsets"
   - "Test search with empty query parameter returns 400 Bad Request"

Please update the task description in TC-9202 with the missing information and re-run `/implement-task TC-9202`.
