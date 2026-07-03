# implement-task: TC-9202 — Add package search functionality

## Step 0 — Validate Project Configuration

Verified the project's CLAUDE.md contains all required sections under `# Project Configuration`:

1. **Repository Registry** — present, contains `trustify-backend` with Serena Instance `serena_backend` and Path `./`.
2. **Jira Configuration** — present with Project key (`TC`), Cloud ID (`2b9e35e3-6bd3-4cec-b838-f4249ee02432`), Feature issue type ID (`10142`), Git Pull Request custom field (`customfield_10875`), and GitHub Issue custom field (`customfield_10747`).
3. **Code Intelligence** — present with tool naming convention (`mcp__<serena-instance>__<tool>`) and configured instance `serena_backend` using `rust-analyzer`.

Project Configuration validation: **PASSED**.

## Step 0.5 — JIRA Access Initialization

Would attempt MCP tool `jira.get_issue(TC-9202)` first. If MCP fails, would prompt user for REST API fallback per the JIRA Access Initialization protocol.

*(Skipped per eval instructions — no external service calls.)*

## Step 1 — Fetch and Parse Jira Task

Parsed the task description for TC-9202. Results:

| Section | Status | Content |
|---|---|---|
| Repository | Present | `trustify-backend` |
| Target Branch | Present | `main` |
| Description | Present (vague) | "Add search capabilities to the package module so users can find packages more easily." |
| Files to Modify | Present | `modules/fundamental/src/package/endpoints/mod.rs` — add search route |
| Files to Create | Present | `modules/fundamental/src/package/endpoints/search.rs` — search endpoint handler |
| API Changes | **MISSING** | — |
| Implementation Notes | **MISSING** | — |
| Acceptance Criteria | Present (non-actionable) | 3 items, all vague |
| Test Requirements | Present (non-actionable) | 1 item, vague |
| Target PR | Not present | (optional — OK) |
| Bookend Type | Not present | (optional — OK) |
| Dependencies | Not present | (optional — OK) |
| Review Context | Not present | (optional — OK) |

### Extracted metadata

- **Jira issue web URL**: would be captured from the API response's `webUrl` field (e.g., `https://redhat.atlassian.net/browse/TC-9202`).
- **Target Branch**: `main`
- **Target PR**: none
- **Bookend Type**: none
- **GitHub Issue custom field**: `customfield_10747` — would check the issue's fields for this custom field value. Not present in task description.
- **Parent feature**: TC-9001 (linked via "is incorporated by TC-9001")

## STOP — Incomplete Task Description

The task description does not follow the structured template expected by plan-feature. Multiple required sections are missing or insufficiently specified. Per the skill's rules, execution stops here until the user provides the missing information.

### Missing sections

1. **API Changes** — This section is entirely absent. The task says "add search route" and "search endpoint handler" but does not specify:
   - The HTTP method (GET, POST?)
   - The endpoint path (e.g., `GET /api/v2/package/search` or `GET /api/v2/package?q=...`)
   - Query parameters (search term field, pagination, filtering options)
   - Request body shape (if POST)
   - Response body shape (what fields are returned, what wrapper type is used)

2. **Implementation Notes** — This section is entirely absent. No code references, patterns, or reuse guidance is provided. For a search feature in this codebase, implementation notes should specify:
   - Whether to use the existing `SearchService` from `modules/search/` or build a module-local search
   - Which query helpers from `common/src/db/query.rs` to use for filtering and pagination
   - Whether to return `PaginatedResults<PackageSummary>` (following the existing list endpoint pattern)
   - How to integrate with the existing route registration pattern in `endpoints/mod.rs`
   - Whether full-text search (PostgreSQL `tsvector`/`tsquery`) or simple `LIKE`/`ILIKE` filtering is expected
   - Which `PackageSummary` fields should be searchable (name? version? license? all?)

### Insufficiently specified sections

3. **Acceptance Criteria** — All three criteria are too vague to verify:
   - "Users can search for packages" — search by what? Name? Version? License? PURL? What constitutes a "search" vs. the existing list endpoint's filtering?
   - "Search results are relevant" — what ranking or relevance algorithm is expected? Is this full-text search relevance or exact/prefix matching?
   - "Performance is acceptable" — what is the target? Sub-second for N packages? Is there an index requirement?

4. **Test Requirements** — The single requirement ("Test that search works correctly") provides no specifics:
   - What test scenarios are needed? (empty query, exact match, partial match, no results, special characters)
   - Should tests verify pagination of search results?
   - Should tests verify search across specific fields?
   - What is the expected test file location? (presumably `tests/api/package.rs` or a new `tests/api/package_search.rs`, following the pattern in `tests/api/search.rs`)

### Questions for the user

Before proceeding with any implementation, the following information is needed:

1. **API design**: What is the endpoint specification? Specifically:
   - Is this a new `GET /api/v2/package/search?q=<term>` endpoint, or should search be added as a query parameter to the existing `GET /api/v2/package` list endpoint?
   - What query parameters should it accept (search term, pagination, sort order)?
   - Should it return `PaginatedResults<PackageSummary>` like the existing list endpoint?

2. **Search scope**: Which fields on `PackageSummary` should be searchable (name, license, version, all)?

3. **Search mechanism**: Should this use PostgreSQL full-text search (`tsvector`/`tsquery`), simple `ILIKE` pattern matching, or the existing `SearchService` in `modules/search/`?

4. **Implementation patterns**: Should the implementation follow the existing `advisory/service/advisory.rs` pattern (which already has a `search` method on `AdvisoryService`), extending `PackageService` with a similar `search` method?

5. **Test specifics**: What test cases are required? At minimum, I would expect: search with results, search with no results, search with pagination, search with empty query. Are there additional scenarios?

6. **Performance requirements**: Are there specific latency or result-count targets? Should a database index be added as part of this task?

**Execution halted. Awaiting user clarification on the above gaps before proceeding to Step 1.5 or any subsequent steps (branching, code inspection, implementation, testing).**
