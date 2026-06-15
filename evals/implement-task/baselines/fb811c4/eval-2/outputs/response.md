# implement-task: TC-9202 — Add package search functionality

## Step 0 — Validate Project Configuration

Checked the project's CLAUDE.md (claude-md-mock.md) for required sections:

1. **Repository Registry** — present, contains `trustify-backend` with Serena instance `serena_backend` and path `./`.
2. **Jira Configuration** — present, contains Project key (`TC`), Cloud ID, Feature issue type ID, Git Pull Request custom field (`customfield_10875`), and GitHub Issue custom field (`customfield_10747`).
3. **Code Intelligence** — present, with tool naming convention (`mcp__<serena-instance>__<tool>`) and configured instance `serena_backend` using `rust-analyzer`.

All required sections are present. Proceeding.

## Step 0.5 — JIRA Access Initialization

Would attempt MCP first for all JIRA operations. (Skipped per eval instructions — no external service calls.)

## Step 1 — Fetch and Parse Jira Task

Parsed the structured description for TC-9202. Results:

| Section | Status | Value |
|---|---|---|
| Repository | Present | `trustify-backend` |
| Target Branch | Present | `main` |
| Description | Present (vague) | "Add search capabilities to the package module so users can find packages more easily." |
| Files to Modify | Present | `modules/fundamental/src/package/endpoints/mod.rs` — add search route |
| Files to Create | Present | `modules/fundamental/src/package/endpoints/search.rs` — search endpoint handler |
| API Changes | **MISSING** | Not specified |
| Implementation Notes | **MISSING** | Not specified |
| Acceptance Criteria | Present but **VAGUE** | See details below |
| Test Requirements | Present but **VAGUE** | See details below |
| Target PR | Not present (optional) | — |
| Bookend Type | Not present (optional) | — |
| Dependencies | Not present | — |
| Review Context | Not present (optional) | — |

## STOP — Incomplete Task Description

The task description for TC-9202 is missing required sections and contains vague criteria that do not meet the structured description template. **Execution is halted.** The following gaps must be resolved before implementation can proceed.

### Gap 1: Missing "API Changes" section

The task creates a new search endpoint but does not specify:

- **HTTP method and route path** (e.g., `GET /api/v2/package/search` or `GET /api/v2/package?q=...`)
- **Query parameters** (e.g., `q` for search term, `offset`/`limit` for pagination, filter fields like `license`, `ecosystem`)
- **Response shape** (e.g., does it return `PaginatedResults<PackageSummary>` like the existing list endpoint, or a different search result type?)
- **Status codes** (e.g., 200 for success, 400 for invalid query, etc.)

The repository already has a `modules/search/` module with a `SearchService` for full-text search across entities. It is unclear whether this task should integrate with that existing search infrastructure or implement a standalone query-based search within the package module.

### Gap 2: Missing "Implementation Notes" section

There are no patterns or code references to follow. The skill requires Implementation Notes to guide the implementation. Specifically, we need to know:

- **Which search approach to use**: Should this use the existing `SearchService` from `modules/search/` (full-text search), or implement query-based filtering using `common/src/db/query.rs` helpers (like the existing list endpoints do), or something else entirely?
- **Which fields are searchable**: Should search match against package name only, or also version, license, description, ecosystem, or other fields?
- **Pattern references**: Which existing endpoint handler should be used as the template? The `advisory` module has a `search` method in its `AdvisoryService` — should the package search follow the same pattern?
- **Service layer changes**: The task only lists files in `endpoints/` but does not mention `service/mod.rs`. Does `PackageService` need a new `search` method, or should the endpoint call `SearchService` directly?
- **Integration with existing search module**: The repository has `modules/search/` with `SearchService: full-text search across entities` and `GET /api/v2/search`. How does this package-specific search relate to the global search?

### Gap 3: Vague Acceptance Criteria

The current Acceptance Criteria are not measurable or verifiable:

| Criterion | Problem |
|---|---|
| "Users can search for packages" | Does not specify what inputs trigger a search (name? license? version? pURL?), what "search" means technically (substring match? full-text? regex?), or what constitutes a valid result. |
| "Search results are relevant" | "Relevant" is subjective and unmeasurable. No ranking criteria, relevance scoring method, or minimum match quality is defined. |
| "Performance is acceptable" | "Acceptable" is undefined. No latency target (e.g., "responds within 500ms for 10k packages"), no load requirements, no pagination behavior specified. |

These need to be replaced with specific, testable criteria. For example:
- "GET /api/v2/package/search?q=openssl returns packages whose name contains 'openssl'"
- "Search results are paginated using PaginatedResults with default limit of 20"
- "Search with no results returns an empty PaginatedResults (200 OK, items: [], total: 0)"

### Gap 4: Vague Test Requirements

The single test requirement — "Test that search works correctly" — does not specify:

- **Which test file** to create or modify (the `tests/api/` directory has existing test files like `sbom.rs`, `advisory.rs`, `search.rs` — should a new `package_search.rs` be created, or should tests be added to an existing file?)
- **Which scenarios to test**: No specific test cases are enumerated. At minimum, a search endpoint typically requires:
  - Search with matching results
  - Search with no matching results (empty response)
  - Search with special characters or empty query
  - Pagination of search results
  - Invalid/missing query parameter (400 response)
- **Expected response assertions**: No field-level expectations are stated for validating correctness.

### Gap 5: Files to Modify may be incomplete

The task lists only `modules/fundamental/src/package/endpoints/mod.rs` for modification and `modules/fundamental/src/package/endpoints/search.rs` for creation. However:

- If a new `search` method is needed in the service layer, `modules/fundamental/src/package/service/mod.rs` should be listed in Files to Modify.
- If the search route needs to be mounted at the server level, `server/src/main.rs` may need modification (though likely not, since the package module's `endpoints/mod.rs` handles route registration within the module).
- If a new test file is needed, it should be listed in Files to Create (e.g., `tests/api/package_search.rs` or similar).

---

## Action Required

Please provide the missing information for TC-9202 before implementation can proceed:

1. **API Changes**: What is the HTTP method, route path, query parameters, and response shape for the search endpoint?
2. **Implementation Notes**: Which search approach should be used (existing `SearchService`, query-based filtering via `common/src/db/query.rs`, or other)? Which existing endpoint should be used as the pattern reference? Does `PackageService` need a new method?
3. **Acceptance Criteria**: Please replace the vague criteria with specific, measurable conditions (e.g., which fields are searchable, what match behavior is expected, what pagination defaults apply).
4. **Test Requirements**: Please specify the test file location, the test scenarios to cover, and the expected assertions for each scenario.
5. **Files to Modify/Create**: Confirm whether service layer files (`service/mod.rs`) and test files need to be listed.

I will not proceed with branching, implementation planning, code inspection, or any code changes until these gaps are resolved.
