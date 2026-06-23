# implement-task: TC-9202 — Add package search functionality

## Step 0 — Validate Project Configuration

Project Configuration in CLAUDE.md has been verified:

1. **Repository Registry** — present, contains `trustify-backend` with Serena instance `serena_backend` at path `./`.
2. **Jira Configuration** — present with Project key (`TC`), Cloud ID, and Feature issue type ID.
3. **Code Intelligence** — present with tool naming convention (`mcp__<serena-instance>__<tool>`) and configured instance `serena_backend` using `rust-analyzer`.

Project Configuration is complete. Proceeding to Step 1.

## Step 1 — Fetch and Parse Jira Task

Parsing the structured description of TC-9202:

| Section | Status | Content |
|---|---|---|
| **Repository** | Present | `trustify-backend` |
| **Target Branch** | Present | `main` |
| **Description** | Present but vague | "Add search capabilities to the package module so users can find packages more easily." |
| **Files to Modify** | Present but incomplete | Only lists `modules/fundamental/src/package/endpoints/mod.rs` |
| **Files to Create** | Present but incomplete | Only lists `modules/fundamental/src/package/endpoints/search.rs` |
| **API Changes** | **MISSING** | No endpoint specification (path, method, query parameters, response shape) |
| **Implementation Notes** | **MISSING** | No patterns, code references, or guidance on how to implement |
| **Acceptance Criteria** | Present but vague | Criteria are not measurable or verifiable (see below) |
| **Test Requirements** | Present but vague | Single item with no specific test cases (see below) |
| **Bookend Type** | Not present (optional) | N/A |
| **Target PR** | Not present (optional) | N/A |
| **Dependencies** | Not present | Not listed |

### Identified Gaps

Per constraint 1.6, the following gaps in the structured description prevent implementation from proceeding:

**1. Missing: API Changes section**

The task adds a search endpoint but provides no API contract. The following details are unspecified:

- What is the endpoint path? (e.g., `GET /api/v2/package/search` or a query parameter on the existing `GET /api/v2/package`?)
- What query parameters does the search accept? (e.g., `q`, `name`, `purl`, `license`?)
- What is the response shape? (e.g., `PaginatedResults<PackageSummary>` consistent with the existing list endpoint?)
- What HTTP method is used?

**2. Missing: Implementation Notes section**

There is no guidance on how to implement the search. Key questions:

- Should this use the existing `modules/search/` full-text search infrastructure (which already has a `SearchService` at `modules/search/src/service/mod.rs`), or should it implement search directly in the package module?
- What search mechanism should be used? PostgreSQL full-text search (`tsvector`/`tsquery`), SQL `ILIKE`, or integration with the existing `SearchService`?
- Should the search leverage the shared query builder helpers in `common/src/db/query.rs` for filtering and pagination?
- What fields should be searchable? (package name, PURL, license, version?)
- Are there existing patterns in sibling modules to follow? (e.g., the `advisory` module has `search` in its `AdvisoryService` — should the package search follow the same pattern?)

**3. Incomplete: Files to Modify / Files to Create**

The task only lists endpoint-level files but likely requires changes to:

- `modules/fundamental/src/package/service/mod.rs` — to add a `search` method to `PackageService`
- `modules/fundamental/src/package/model/` — potentially a search-specific model or query parameters struct
- `server/src/main.rs` — if route mounting needs updating
- `tests/api/` — a test file for the package search endpoint (not listed in Files to Create)
- Possibly `entity/src/package.rs` — if database-level search requires query changes

**4. Vague: Acceptance Criteria**

The acceptance criteria are not measurable:

- "Users can search for packages" — search by what? Name? PURL? License? All fields?
- "Search results are relevant" — what defines relevance? Exact match? Substring? Fuzzy? Ranked?
- "Performance is acceptable" — what is the performance threshold? Response time target? Maximum result set size?

**5. Vague: Test Requirements**

The single test requirement "Test that search works correctly" provides no specifics:

- What test cases should be covered? (empty query, exact match, partial match, no results, special characters?)
- Should error cases be tested? (invalid parameters, unauthorized access?)
- What is the expected assertion pattern? (status code checks, response body validation, result count verification?)
- Should performance/load tests be included given the "Performance is acceptable" acceptance criterion?

## Decision: STOP — Clarification Required

Per the implement-task skill's Step 1 rules and constraint 1.6:

> "If any required section is missing or the description doesn't follow the template, list the gaps, ask the user for clarification, and **stop execution immediately** — do not proceed with any subsequent steps (branching, implementation planning, code changes) until the user provides the missing information."

**I am stopping execution and requesting clarification on the following before proceeding:**

1. **API Changes**: What is the full endpoint specification? (path, method, query parameters, response shape)
2. **Implementation Notes**: Should this integrate with the existing `modules/search/` SearchService or implement search directly in the package service? What search mechanism (full-text, ILIKE, etc.)? What fields are searchable?
3. **Files to Modify / Files to Create**: The list appears incomplete — the service layer, potential model changes, test files, and possibly entity changes are not accounted for. Please provide the complete file list.
4. **Acceptance Criteria**: Please provide measurable criteria — what fields are searchable, what constitutes a "relevant" result, and what performance thresholds apply.
5. **Test Requirements**: Please specify concrete test cases — at minimum: search with results, search with no results, search with invalid input, and any edge cases.

No branches have been created. No implementation planning has been performed. No code changes have been made. Execution is halted pending user response.
