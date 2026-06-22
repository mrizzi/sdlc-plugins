# implement-task: TC-9202 — Validation Result

## Step 0 — Validate Project Configuration

The project's CLAUDE.md (claude-md-mock.md) contains all required sections under `# Project Configuration`:

1. **Repository Registry** — present, contains `trustify-backend` with Serena instance `serena_backend` and path `./`.
2. **Jira Configuration** — present, contains Project key (`TC`), Cloud ID, Feature issue type ID, and custom fields.
3. **Code Intelligence** — present, lists the `serena_backend` instance with `rust-analyzer` and tool naming convention.

Project Configuration validation: **PASS**. Proceeding to Step 1.

## Step 1 — Fetch and Parse Jira Task

Parsing the structured description for TC-9202 against the required template sections:

| Section | Status | Detail |
|---|---|---|
| **Repository** | Present | `trustify-backend` |
| **Target Branch** | Present | `main` |
| **Description** | Present but vague | "Add search capabilities to the package module so users can find packages more easily." — no specifics on search behavior, fields, query syntax, or integration approach |
| **Files to Modify** | Present | `modules/fundamental/src/package/endpoints/mod.rs` |
| **Files to Create** | Present | `modules/fundamental/src/package/endpoints/search.rs` |
| **API Changes** | **MISSING** | No API Changes section — unclear what endpoint path, HTTP method, request parameters, or response shape to implement |
| **Implementation Notes** | **MISSING** | No Implementation Notes section — no patterns, code references, or guidance on how to implement the search (e.g., SQL LIKE queries vs. full-text search vs. the existing `modules/search/` module, which query helpers to use, how to integrate with `PackageService`) |
| **Acceptance Criteria** | Present but vague | All three criteria are non-specific and unmeasurable: "Users can search for packages" (by what fields? what query format?), "Search results are relevant" (what defines relevance?), "Performance is acceptable" (what threshold?) |
| **Test Requirements** | Present but vague | Single item "Test that search works correctly" — no specific test scenarios, edge cases, error cases, or expected behaviors defined |
| **Dependencies** | Not present | Optional — acceptable |
| **Target PR** | Not present | Optional — acceptable |
| **Bookend Type** | Not present | Optional — acceptable |

## Gaps Identified

The task description is **incomplete**. The following required information is missing or insufficient:

### Missing Sections

1. **API Changes** — This section is required to define the search endpoint contract. Specifically needed:
   - What is the endpoint path? (e.g., `GET /api/v2/package/search` or a query parameter on the existing `GET /api/v2/package`?)
   - What HTTP method does it use?
   - What request parameters does it accept? (query string, body, pagination?)
   - What is the response shape? (reuses `PaginatedResults<PackageSummary>` or a new type?)

2. **Implementation Notes** — This section is required to specify patterns and code references. Specifically needed:
   - Should this use the existing `modules/search/` module's `SearchService` (full-text search), or implement filtering directly in `PackageService` using `common/src/db/query.rs` helpers?
   - What fields should be searchable? (package name, version, license, purl?)
   - What query mechanism? (SQL `LIKE`/`ILIKE`, PostgreSQL full-text search `tsvector`, or integration with an external search service?)
   - What existing patterns to follow? (e.g., the `advisory` module has a `search` method in `AdvisoryService` — should the package search follow the same pattern?)
   - How should the new `search.rs` endpoint be registered in `endpoints/mod.rs`?

### Vague Sections

3. **Acceptance Criteria** — The current criteria are not measurable or verifiable:
   - "Users can search for packages" — by what fields? What constitutes a valid search query?
   - "Search results are relevant" — what ranking or matching algorithm defines relevance? Is partial matching expected?
   - "Performance is acceptable" — what is the performance target? (e.g., < 200ms for 10k packages?)

4. **Test Requirements** — The current requirement "Test that search works correctly" does not specify:
   - What test scenarios to cover (e.g., exact match, partial match, no results, empty query, special characters)
   - What error cases to test (e.g., invalid query parameters, 400 response)
   - Whether integration tests are needed in `tests/api/` following the existing pattern (e.g., `tests/api/search.rs` already exists for the search module)
   - Whether service-level unit tests are needed

## Decision: Stop Execution

Per the implement-task skill rules:

> "If the structured description is incomplete, ask the user for clarification and **stop execution**. Do not draft an implementation plan, create branches, or proceed with any subsequent steps until the user provides the missing information."

**Execution stopped.** The task description for TC-9202 is missing the **API Changes** and **Implementation Notes** sections entirely, and the **Acceptance Criteria** and **Test Requirements** sections are too vague to implement against without guessing.

## Clarification Needed

Before proceeding with implementation, please provide the following:

1. **API Changes**: What is the exact endpoint path, HTTP method, request parameters (search query, filters, pagination), and response shape for the package search?

2. **Implementation Notes**: Should this search use the existing `SearchService` in `modules/search/`, or implement direct database querying via `PackageService` using the shared query helpers in `common/src/db/query.rs`? What fields should be searchable? What matching strategy (exact, prefix, full-text)? Please reference the specific patterns and existing code to follow (e.g., the `AdvisoryService::search` method pattern).

3. **Acceptance Criteria**: Please provide measurable criteria — for example: "Search by package name returns matching packages using case-insensitive substring matching", "Search with no results returns an empty `PaginatedResults` with `total_count: 0`", "Search endpoint responds within 500ms for datasets up to 50k packages".

4. **Test Requirements**: Please specify concrete test scenarios — for example: "Test search by exact package name returns matching result", "Test search with no matches returns empty results", "Test search with pagination parameters", "Test search with invalid query returns 400".

Please update the task description in Jira with the missing sections, or provide the information here so I can proceed.
