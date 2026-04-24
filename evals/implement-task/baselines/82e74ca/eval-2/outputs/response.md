# implement-task: TC-9202 — Execution Halted (Incomplete Task Description)

## Step 0 — Validate Project Configuration

Project Configuration in CLAUDE.md has been validated:

- **Repository Registry**: Present with `trustify-backend` mapped to Serena instance `serena_backend`.
- **Jira Configuration**: Present with Project key (`TC`), Cloud ID, and Feature issue type ID.
- **Code Intelligence**: Present with tool naming convention (`mcp__<serena-instance>__<tool>`) and configured instance `serena_backend` using `rust-analyzer`.

Project Configuration is complete. Proceeding to Step 1.

## Step 1 — Fetch and Parse Jira Task

Parsing the structured description for TC-9202 against the required template sections:

| Required Section       | Status      | Notes                                                                                                            |
|------------------------|-------------|------------------------------------------------------------------------------------------------------------------|
| Repository             | Present     | `trustify-backend`                                                                                               |
| Description            | Present     | "Add search capabilities to the package module so users can find packages more easily." — vague, lacks specifics |
| Files to Modify        | Present     | `modules/fundamental/src/package/endpoints/mod.rs`                                                               |
| Files to Create        | Present     | `modules/fundamental/src/package/endpoints/search.rs`                                                            |
| API Changes            | **MISSING** | No API Changes section. What endpoint path, HTTP method, query parameters, and response shape should be used?    |
| Implementation Notes   | **MISSING** | No Implementation Notes section. No patterns, code references, or reusable utilities are specified.              |
| Acceptance Criteria    | Present     | Criteria are vague and non-actionable (see details below).                                                       |
| Test Requirements      | Present     | Requirements are vague and non-actionable (see details below).                                                   |
| Dependencies           | Absent      | No Dependencies section. This may be acceptable if there are none, but should be confirmed.                      |

### Identified Gaps

**1. Missing: API Changes section**

The task asks to "add search functionality" but does not specify:
- The endpoint path (e.g., `GET /api/v2/package/search` or `GET /api/v2/package?q=...`)
- The HTTP method
- Query parameters (search term, filters, pagination)
- The response shape (what fields are returned, whether results use `PaginatedResults<T>`)

Without this information, I cannot implement the endpoint correctly.

**2. Missing: Implementation Notes section**

There are no implementation notes specifying:
- Which existing patterns to follow (e.g., how the `advisory` module implements its search — see `modules/fundamental/src/advisory/service/advisory.rs` which has `AdvisoryService: fetch, list, search`)
- Whether to use the existing `SearchService` in `modules/search/` or build module-local search logic
- Which query helpers from `common/src/db/query.rs` to use for filtering and pagination
- Whether to leverage full-text search capabilities or simple LIKE/ILIKE matching
- How search results should be ranked or sorted
- Whether the `PackageService` in `modules/fundamental/src/package/service/mod.rs` needs a new `search` method or if the existing `list` method should be extended

**3. Vague Acceptance Criteria**

The current acceptance criteria are not actionable:
- "Users can search for packages" — search by what? Name? Version? License? PURL? All fields?
- "Search results are relevant" — what defines relevance? Exact match? Substring? Full-text ranking?
- "Performance is acceptable" — what is the performance threshold? Response time target? Maximum result set size?

These criteria cannot be objectively verified during Step 8.

**4. Vague Test Requirements**

The test requirements state only "Test that search works correctly" without specifying:
- What test scenarios to cover (e.g., exact match, partial match, no results, special characters)
- Whether to test pagination of search results
- Whether to test filtering in combination with search
- Whether to test error cases (e.g., empty query, overly long query)
- What assertion patterns to use (the repository uses integration tests in `tests/api/` against a real PostgreSQL database)

**5. Missing service layer guidance**

The Files to Modify and Files to Create sections only reference the `endpoints/` directory. There is no mention of whether a service-layer method needs to be added to `modules/fundamental/src/package/service/mod.rs` (which currently only has `fetch` and `list`). A search endpoint would typically require a corresponding service method — this omission suggests the task description is incomplete.

## Decision: Stop Execution

Per the implement-task skill specification:

> "If any required section is missing or the description doesn't follow the template, list the gaps, ask the user for clarification, and stop execution immediately."

**Execution is halted.** I will not proceed with branching, implementation planning, code changes, or any subsequent steps.

## Clarification Needed

Please provide the following information before I can proceed with implementation:

1. **API Changes**: What is the endpoint specification?
   - Endpoint path and HTTP method (e.g., `GET /api/v2/package/search?q=<term>`)
   - Query parameters (search term, optional filters, pagination parameters)
   - Response shape (fields returned, use of `PaginatedResults<PackageSummary>`?)

2. **Implementation Notes**: What patterns should be followed?
   - Should the search reuse the existing `SearchService` from `modules/search/`, or implement module-local search in `PackageService`?
   - Which query helpers from `common/src/db/query.rs` should be used?
   - What search strategy should be used (SQL LIKE, PostgreSQL full-text search, trigram matching)?
   - Are there specific sibling implementations to follow (e.g., `AdvisoryService.search`)?

3. **Service layer changes**: Does `modules/fundamental/src/package/service/mod.rs` need a new `search` method? If so, it should be listed in Files to Modify.

4. **Acceptance Criteria**: Please provide specific, verifiable criteria:
   - What fields are searchable?
   - What constitutes a "relevant" result?
   - What is the performance target?

5. **Test Requirements**: Please provide specific test scenarios:
   - Which search cases should be tested (exact match, partial, no results, edge cases)?
   - Should pagination and filtering be tested in combination with search?
   - What error cases should be covered?

6. **Dependencies**: Are there any prerequisite tasks that must be completed first? Please confirm or add a Dependencies section.

Once the task description is updated with the missing sections, please re-run `/implement-task TC-9202` and I will proceed with the full implementation workflow.
