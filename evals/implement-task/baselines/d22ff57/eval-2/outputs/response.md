# implement-task TC-9202 -- Incomplete Task Description, Clarification Required

## Step 0 -- Validate Project Configuration

I have validated the project's CLAUDE.md and confirmed all required sections are present:

1. **Repository Registry** -- contains `trustify-backend` with Serena instance `serena_backend` at path `./`.
2. **Jira Configuration** -- contains Project key (`TC`), Cloud ID, Feature issue type ID, Git Pull Request custom field (`customfield_10875`), and GitHub Issue custom field (`customfield_10747`).
3. **Code Intelligence** -- present with tool naming convention `mcp__<serena-instance>__<tool>` and configured instance `serena_backend` using `rust-analyzer`.

Project configuration is complete. Proceeding to Step 1.

## Step 1 -- Fetch and Parse Jira Task

I fetched TC-9202 ("Add package search functionality") and parsed its structured description. The task contains the following sections:

| Section | Status |
|---|---|
| Repository | Present: `trustify-backend` |
| Description | Present but vague |
| Files to Modify | Present: 1 file |
| Files to Create | Present: 1 file |
| API Changes | **MISSING** |
| Implementation Notes | **MISSING** |
| Acceptance Criteria | Present but vague (3 items) |
| Test Requirements | Present but vague (1 item) |
| Target PR | Not present (default flow) |
| Review Context | Not present |
| Dependencies | Not present |

**The structured description is incomplete.** Two required sections are entirely absent, and three others lack the specificity needed to implement against. Per the skill's rules, I must list the gaps, ask the user for clarification, and **stop execution immediately** -- I will not proceed with any subsequent steps (branching, implementation planning, code changes) until the missing information is provided.

---

## Gaps Identified

### 1. Missing "API Changes" Section

The task asks to "add search capabilities" and lists a new endpoint file to create (`search.rs`), but does not define the API contract. The following are undefined:

- **HTTP method and path**: Is this `GET /api/v2/package/search`, `GET /api/v2/package?q=<term>` (a query parameter on the existing list endpoint), or something else entirely?
- **Query parameters or request body**: What parameters does the search accept? A free-text query string (`q`)? Structured field-level filters? Pagination parameters?
- **Response shape**: Should the response use the existing `PaginatedResults<PackageSummary>` wrapper consistent with other list endpoints (e.g., `GET /api/v2/sbom`, `GET /api/v2/advisory`), or does it need a different structure (e.g., with relevance scores)?
- **Error responses**: What status codes and error shapes should be returned for invalid input, empty queries, or other error conditions?

Without an API contract, I cannot implement the endpoint handler or write meaningful integration tests.

### 2. Missing "Implementation Notes" Section

The Implementation Notes section is required to provide concrete guidance on patterns to follow, existing code to reuse, and specific file paths and symbol names discovered during planning. Without it, I cannot determine:

- **Which search mechanism to use**: The repository already has a `modules/search/` module with a `SearchService` providing full-text search across entities at `GET /api/v2/search`. Should the package search reuse this existing infrastructure, extend it, or should it be an independent filtered query within the package module?
- **Which existing patterns to follow**: The `advisory` module has an `AdvisoryService` with what appears to be a `search` method (`service/advisory.rs`). Should the package search follow this pattern? Or should it use a different approach via `common/src/db/query.rs` shared filtering helpers?
- **Which query builder approach to use**: Should the search use PostgreSQL full-text search (`tsvector`/`tsquery`), `ILIKE` pattern matching, trigram similarity (`pg_trgm`), or simple `WHERE` clause filtering via SeaORM?
- **Which fields on `PackageSummary` or the `package` entity to search against**: The `PackageSummary` struct in `model/summary.rs` contains a `license` field, but the full set of searchable fields (name, version, PURL, namespace, ecosystem, description) is unknown.

### 3. Vague Acceptance Criteria

All three acceptance criteria lack the specificity required for implementation and verification:

- **"Users can search for packages"** -- This restates the task summary without adding detail. Search by what fields? Using what mechanism (free-text, structured filters, autocomplete)? Through what interface (a dedicated endpoint, a query parameter on the list endpoint)?

- **"Search results are relevant"** -- "Relevant" is undefined and unmeasurable. To implement and verify this criterion, I need to know:
  - Which fields determine relevance (name only? name + description? name + license + PURL?).
  - What type of matching is expected (exact, prefix, substring/contains, full-text with stemming).
  - Whether results should be ranked (e.g., exact matches first, then prefix matches, then substring matches) or returned in an unspecified order.
  - Whether matching should be case-insensitive.

- **"Performance is acceptable"** -- "Acceptable" has no quantitative definition. There is no:
  - Latency target (e.g., p95 < 200ms).
  - Dataset size assumption (e.g., "with 100,000 packages in the database").
  - Indexing requirement (e.g., "must use a GIN index on the name column").
  - Pass/fail threshold that could be verified during Step 8 (Verify Acceptance Criteria).

Without measurable criteria, I cannot objectively verify the implementation satisfies requirements.

### 4. Vague Test Requirements

The single test requirement -- **"Test that search works correctly"** -- does not define what "correctly" means. It does not specify:

- Which test scenarios to cover (e.g., exact name match, partial match, no results, empty query, special characters, pagination).
- Which response fields to assert on beyond HTTP status code (e.g., result count, matched package names, field values, ordering).
- Whether error cases need coverage (e.g., missing query parameter, malformed input, invalid pagination values).
- Whether the tests should follow the existing integration test pattern in `tests/api/` (hitting a real PostgreSQL test database with `assert_eq!(resp.status(), StatusCode::OK)` assertions).

The implement-task skill requires concrete test scenarios to drive test implementation and verify each acceptance criterion.

### 5. Incomplete File Scope

The task lists only:
- **Files to Modify**: `modules/fundamental/src/package/endpoints/mod.rs` (add search route)
- **Files to Create**: `modules/fundamental/src/package/endpoints/search.rs` (search endpoint handler)

Based on the repository's established module pattern (`model/ + service/ + endpoints/`), the following additional files would likely need modification or creation depending on the implementation approach:

- `modules/fundamental/src/package/service/mod.rs` -- a service method containing the search query logic (following the pattern where `sbom/service/sbom.rs` contains `SbomService` methods and `advisory/service/advisory.rs` contains `AdvisoryService` methods including search).
- A test file in `tests/api/` (e.g., `tests/api/package_search.rs`) -- the Test Requirements section says to test search but no test file is listed in Files to Create.
- Potentially `migration/` -- if a database index is needed for search performance (e.g., a GIN trigram index on the package name column).

These scope gaps cannot be resolved without clarifying the implementation approach first.

---

## Clarifying Questions

Before I can proceed with implementation, I need the following information:

**Q1 -- What is the API contract for the search endpoint?**

What HTTP method and path should the endpoint use? What query parameters or request body does it accept? What does the response look like? Should it follow the same `PaginatedResults<PackageSummary>` format used by the existing `GET /api/v2/package` list endpoint? Specifically:
- Is this a new route (e.g., `GET /api/v2/package/search?q=<term>`) or a query-parameter extension on the existing list endpoint (e.g., `GET /api/v2/package?q=<term>`)?
- What parameters are required vs. optional?

**Q2 -- Which fields should the search match against?**

Should the search match on package name only, or also on other fields such as version, license, PURL, namespace/ecosystem, or description? Should matching be exact, prefix (starts-with), substring (contains), or full-text? Should it be case-insensitive?

**Q3 -- What does "relevant" mean for result ranking?**

Should results be ranked in a specific order (e.g., exact matches above partial matches, then alphabetical)? Or is any matching result set in default database order acceptable? If ranking is required, what is the ranking algorithm or priority scheme?

**Q4 -- Should the search reuse the existing `modules/search/` infrastructure or be a standalone query?**

The repository has `modules/search/src/service/mod.rs` providing `SearchService` for full-text search across entities at `GET /api/v2/search`. Should the package search:
- (a) Add a query parameter filter to the existing `GET /api/v2/package` list endpoint using `common/src/db/query.rs` helpers.
- (b) Create a dedicated `GET /api/v2/package/search` route with its own handler in `search.rs`.
- (c) Extend the existing `SearchService` in `modules/search/` to support package-specific search.

This decision directly affects file scope, service layer changes, and the API contract.

**Q5 -- What is the measurable performance threshold?**

Is there a latency target (e.g., p95 under 200ms for N packages)? Is a database index required, and if so, does one already exist on the relevant columns in the `package` entity, or does a migration need to be created? Or does "acceptable" simply mean the endpoint must not perform an unbounded full table scan?

**Q6 -- What specific test scenarios are required?**

Please specify which of the following should be covered by integration tests:
- A query that matches one or more packages by name
- A query that returns zero results
- Pagination of search results (using `PaginatedResults<T>`)
- Case-insensitive matching behavior
- Partial match vs. exact match behavior
- An error response for a missing or empty query parameter
- Handling of special characters in the query string

---

## Next Steps

Once these questions are answered and the task description is updated with the missing **API Changes** and **Implementation Notes** sections, refined **Acceptance Criteria**, and concrete **Test Requirements**, I will:

1. Inspect the existing code (advisory search pattern, package service, query helpers, search module) using the `serena_backend` Serena instance.
2. Perform convention conformance analysis on sibling files in the package and advisory modules.
3. Produce a scoped implementation plan with concrete file changes.
4. Proceed through the remaining implement-task steps (branch creation, implementation, testing, verification, commit, PR, Jira update).

**Stopping execution.** No branch has been created, no code has been written, and no implementation plan has been drafted. I will not proceed until the ambiguities above are resolved.
