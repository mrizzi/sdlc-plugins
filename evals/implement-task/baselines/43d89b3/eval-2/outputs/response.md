## Step 0 -- Validate Project Configuration

Verified that the project's CLAUDE.md contains the required sections:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena instance `serena_backend` at path `./`.
2. **Jira Configuration** -- present, contains Project key (`TC`), Cloud ID, Feature issue type ID, Git Pull Request custom field (`customfield_10875`), and GitHub Issue custom field (`customfield_10747`).
3. **Code Intelligence** -- present, with tool naming convention `mcp__<serena-instance>__<tool>` and configured instance `serena_backend` using `rust-analyzer`.

Project Configuration is valid. Proceeding.

## Step 1 -- Fetch and Parse Jira Task

Parsed the structured description for TC-9202. Here is what was found:

| Section | Status |
|---|---|
| Repository | Present: `trustify-backend` |
| Target Branch | Present: `main` |
| Description | Present but vague: "Add search capabilities to the package module so users can find packages more easily." |
| Files to Modify | Present: `modules/fundamental/src/package/endpoints/mod.rs` |
| Files to Create | Present: `modules/fundamental/src/package/endpoints/search.rs` |
| API Changes | **MISSING** -- no API Changes section, despite the task adding a new search endpoint |
| Implementation Notes | **MISSING** -- no Implementation Notes section at all |
| Acceptance Criteria | Present but **vague** (see details below) |
| Test Requirements | Present but **vague** (see details below) |
| Target PR | Not present (not required) |
| Bookend Type | Not present (not required) |
| Dependencies | Not present (not required) |

### Identified gaps in the task description

**1. Missing Implementation Notes (required section)**

The task has no Implementation Notes section. This section is essential because it specifies which patterns and code references to follow during implementation. Without it, there is no guidance on:

- Which existing search patterns to follow (the repository has a `modules/search/` module with `SearchService` -- should the package search reuse or extend this, or implement a separate mechanism?)
- What query builder helpers from `common/src/db/query.rs` to use for filtering and pagination
- How to integrate with the existing `PackageService` in `modules/fundamental/src/package/service/mod.rs`
- What the search endpoint route should look like (e.g., `GET /api/v2/package/search?q=...` vs. adding a query parameter to the existing `GET /api/v2/package` list endpoint)

**2. Vague Acceptance Criteria**

- "Users can search for packages" -- does not specify which fields are searchable (package name only? version? license? description? purl?), what the search input mechanism is (query string parameter? request body?), or whether partial/fuzzy matching is required.
- "Search results are relevant" -- does not define what "relevant" means. There is no specification for relevance ranking, sorting, or scoring. Does this require full-text search with ranking, or simple substring matching?
- "Performance is acceptable" -- does not define a performance threshold. What response time is acceptable? Under what data volume? Is there a specific latency SLA (e.g., p95 < 200ms)?

**3. Vague Test Requirements**

- "Test that search works correctly" -- does not specify what test scenarios are needed. There is no guidance on: which search queries to test, expected result counts or values, edge cases (empty query, no results, special characters), performance benchmarks, or error cases (malformed queries).

**4. Missing API Changes section**

The task is adding a new search endpoint but does not specify the API contract: HTTP method, path, query parameters, request/response shapes, pagination behavior, or error responses.

---

## Execution stopped -- clarification required

Per the implement-task skill rules: "If the structured description is incomplete, ask the user for clarification and stop execution immediately -- do not proceed with any subsequent steps (branching, implementation planning, code changes) until the user provides the missing information."

The description for TC-9202 is missing the **Implementation Notes** section entirely, the **API Changes** section, and contains vague Acceptance Criteria and Test Requirements. I need the following clarifications before proceeding:

### Clarifying questions

1. **Which fields should be searchable, and what matching behavior is expected?**
   The package entity (defined in `entity/src/package.rs`) likely has multiple fields (name, version, purl, license, etc.). Which fields should the search query match against? Should this be exact matching, substring/LIKE matching, or full-text search with PostgreSQL `tsvector`/`tsquery`? Should the existing `SearchService` in `modules/search/` be reused or extended, or should this be a separate implementation within the package module?

2. **What does "relevant" mean for search results, and how should they be ranked?**
   The acceptance criterion "Search results are relevant" needs a concrete definition. Should results be ranked by relevance score (e.g., PostgreSQL `ts_rank`)? Should exact matches rank higher than partial matches? Is there a specific sort order required (relevance first, then alphabetical)? Should the response include a relevance score field? How should pagination interact with relevance ranking?

3. **What is the performance threshold, and what test scenarios are required?**
   "Performance is acceptable" needs a measurable definition -- what is the maximum acceptable response time (e.g., p95 < 200ms for 10,000 packages)? For test requirements, "test that search works correctly" needs specific scenarios: should tests cover exact match, partial match, no results, empty query, special characters, pagination of search results, and/or case sensitivity? Should the tests follow the integration test pattern in `tests/api/` hitting a real PostgreSQL test database?

4. **What is the API contract for the search endpoint?**
   The task lists files to create (`search.rs`) and modify (`mod.rs`) but does not specify the endpoint contract. What HTTP method and path should be used (e.g., `GET /api/v2/package/search?q=...`)? What query parameters are supported (search term, pagination, filters)? Should the response use `PaginatedResults<PackageSummary>` from `common/src/model/paginated.rs`? What error responses should be returned (e.g., 400 for missing query parameter)?

Please provide the missing Implementation Notes, clarify the Acceptance Criteria and Test Requirements, and specify the API Changes so that I can proceed with implementation.
