# implement-task TC-9202

## Step 0 -- Validate Project Configuration

Checked the project's CLAUDE.md for required sections under `# Project Configuration`:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena instance `serena_backend`.
2. **Jira Configuration** -- present with Project key (TC), Cloud ID, and Feature issue type ID.
3. **Code Intelligence** -- present with tool naming convention (`mcp__<serena-instance>__<tool>`) and configured instance `serena_backend` using `rust-analyzer`.

Project Configuration is valid. Proceeding to Step 1.

## Step 1 -- Fetch and Parse Jira Task

Parsed the task description for TC-9202. The following sections were found:

| Section | Status |
|---|---|
| Repository | Present: `trustify-backend` |
| Target Branch | Present: `main` |
| Description | Present but vague |
| Files to Modify | Present: 1 file |
| Files to Create | Present: 1 file |
| API Changes | **MISSING** |
| Implementation Notes | **MISSING** |
| Acceptance Criteria | Present but vague and unmeasurable |
| Test Requirements | Present but vague and insufficient |
| Target PR | Not present (optional) |
| Bookend Type | Not present (optional) |
| Dependencies | Not present (optional) |

## Identified Gaps

The task description for TC-9202 has critical gaps that prevent implementation. The following sections are missing or do not follow the expected template:

### 1. Missing: API Changes

The task asks to "add search functionality" but does not specify the API contract:

- What is the endpoint path? (e.g., `GET /api/v2/package/search` or a query parameter on the existing `GET /api/v2/package`?)
- What HTTP method should be used?
- What query parameters does the search accept? (e.g., `q`, `name`, `purl`, `license`, `offset`, `limit`)
- What is the response shape? Should it return `PaginatedResults<PackageSummary>` consistent with the existing list endpoint, or a different structure?

### 2. Missing: Implementation Notes

There are no Implementation Notes providing patterns or code references for the implementation. The repository has existing patterns that could be referenced but the task does not specify which to follow:

- The `modules/search/` module already provides a `SearchService` with full-text search across entities -- should this service be reused or extended, or should a separate search be implemented within the `package` module?
- The `advisory` module has an `AdvisoryService` with a `search` method -- should the package search follow the same pattern?
- The `common/src/db/query.rs` module provides shared query builder helpers for filtering, pagination, and sorting -- should these be used for the search?
- What search strategy should be used? (SQL `LIKE`/`ILIKE`, PostgreSQL full-text search with `tsvector`/`tsquery`, or integration with the existing `SearchService`?)
- Should the search endpoint be registered alongside the existing `/api/v2/package` routes, or under a different path?

### 3. Vague: Acceptance Criteria

All three acceptance criteria are subjective and unmeasurable:

- **"Users can search for packages"** -- Search by what fields? Package name only? PURL? License? Version? Some combination? What input format is expected?
- **"Search results are relevant"** -- What defines "relevant"? Exact match only? Substring/prefix matching? Ranked full-text search? Should results be ordered by relevance score or by name?
- **"Performance is acceptable"** -- What is the performance threshold? Is there a maximum response time (e.g., < 200ms)? A maximum result set size? Should pagination be required? Are there expected data volumes to design for?

### 4. Vague: Test Requirements

The single test requirement ("Test that search works correctly") is insufficient to guide test implementation. It does not specify:

- What search scenarios to test (exact match, partial match, no results, special characters)
- Whether error cases should be covered (invalid query parameters, empty search term, excessively long input)
- Whether pagination of search results should be tested
- Whether performance/load testing is expected
- What assertions to make on search results (field presence, ordering, result count)
- Where the test file should be created (the existing `tests/api/` directory has `search.rs` for the global search -- should package search tests go in a new `tests/api/package_search.rs` or be added to the existing `tests/api/search.rs`?)

### 5. Vague: Description

The description ("Add search capabilities to the package module so users can find packages more easily") does not specify the search mechanism, searchable fields, matching behavior, or how this relates to the existing global search module at `modules/search/`.

---

## Clarifying Questions

Before proceeding with implementation, please provide the following information:

1. **API contract**: What should the search endpoint look like? Specifically: what is the endpoint path and HTTP method, what query parameters does it accept (and which fields are searchable -- name, PURL, license, version?), and what response shape should it return? Should it use `PaginatedResults<PackageSummary>` like the existing list endpoint?

2. **Search strategy and architecture**: Should this search reuse or extend the existing `SearchService` in `modules/search/`, follow the pattern of `AdvisoryService.search` in the advisory module, or implement an independent search within the package module using `common/src/db/query.rs` helpers? What search mechanism should be used (SQL `LIKE`/`ILIKE`, PostgreSQL full-text search, or something else)?

3. **Acceptance criteria specifics**: What measurable thresholds define success? For example: which fields must be searchable, what matching behavior is expected (exact, substring, fuzzy), should results be ranked by relevance, and is there a performance target (e.g., response time under a certain threshold for a given data volume)?

4. **Test scenarios**: What specific test cases should be covered? At minimum, should the tests include: search with results, search with no results, search with special characters, pagination of results, and error cases (e.g., missing query parameter)? Where should the test file be located?

5. **Implementation Notes**: Can you provide code references and patterns to follow? For example, which existing service method or endpoint handler should serve as the template for this implementation?

**Stopping execution.** I will not proceed with branching, code inspection, implementation planning, or any subsequent steps until these gaps are resolved. Please update the task description with the missing sections or provide the information above so I can continue.
