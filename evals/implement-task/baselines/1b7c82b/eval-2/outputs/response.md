# implement-task: TC-9202 — Analysis and Clarification Request

## Step 0 — Validate Project Configuration

The project's CLAUDE.md (claude-md-mock.md) contains the required sections:

1. **Repository Registry** — present, with `trustify-backend` mapped to Serena instance `serena_backend`.
2. **Jira Configuration** — present, with Project key (`TC`), Cloud ID, Feature issue type ID, and custom fields.
3. **Code Intelligence** — present, with `serena_backend` using `rust-analyzer`.

Project configuration is valid. Proceeding to Step 1.

## Step 1 — Fetch and Parse Jira Task

Parsing the structured description of TC-9202 against the expected template sections:

| Section | Status | Assessment |
|---|---|---|
| **Repository** | Present | `trustify-backend` — valid, matches Repository Registry. |
| **Target Branch** | Present | `main` — valid. |
| **Description** | Present but **vague** | "Add search capabilities to the package module so users can find packages more easily." — does not specify *what* search capabilities (full-text? filter-based? field-specific?), does not describe how it integrates with the existing `modules/search/` module, and does not explain the expected behavior. |
| **Files to Modify** | Present but **incomplete** | Lists only `modules/fundamental/src/package/endpoints/mod.rs` for adding a search route. Missing: service layer file (`modules/fundamental/src/package/service/mod.rs`), server route mounting (`server/src/main.rs` if needed), and potentially model files if a new response type is required. |
| **Files to Create** | Present but **incomplete** | Lists only `modules/fundamental/src/package/endpoints/search.rs`. Missing: any service-layer search logic file, potential query builder additions, and test files. |
| **API Changes** | **Missing** | No API Changes section. A search endpoint requires specifying the HTTP method, URL path, query parameters (search term, pagination, filters), and response shape. |
| **Implementation Notes** | **Missing** | No Implementation Notes section. This is critical — the task does not reference any existing code patterns, reusable utilities (e.g., `common/src/db/query.rs` for query building, `common/src/model/paginated.rs` for response wrapping, the existing `modules/search/` module's `SearchService`), or the specific symbols and functions to follow. |
| **Acceptance Criteria** | Present but **vague** | All three criteria are non-specific and not verifiable: "Users can search for packages" (how? what fields?), "Search results are relevant" (by what measure?), "Performance is acceptable" (what threshold?). These do not meet the standard of testable acceptance criteria. |
| **Test Requirements** | Present but **vague** | "Test that search works correctly" — does not specify what test scenarios to cover (e.g., search by name, search with no results, pagination, empty query, special characters, performance). Does not specify whether to create a new test file or extend existing ones. |
| **Dependencies** | Not present | Not required if there are no dependencies, but should be confirmed. |
| **Reuse Candidates** | **Missing** | The repository has potentially reusable code: `common/src/db/query.rs` (shared query builder with filtering, pagination, sorting), `common/src/model/paginated.rs` (`PaginatedResults<T>`), and `modules/search/src/service/mod.rs` (`SearchService` with full-text search). None of these are referenced. |

## Identified Gaps

The following gaps prevent implementation from proceeding:

### 1. Missing: API Changes section
The task creates a search endpoint but does not specify:
- The HTTP method and URL path (e.g., `GET /api/v2/package/search?q=...` or `GET /api/v2/package?q=...` as a query parameter on the existing list endpoint)
- Query parameters (search term, pagination parameters, filter fields)
- Response shape (does it return `PaginatedResults<PackageSummary>` like the existing list endpoint, or a different structure?)

### 2. Missing: Implementation Notes section
The task does not explain:
- Whether to use the existing `SearchService` from `modules/search/` or implement search logic directly in the package module's service layer
- What search mechanism to use (SQL `LIKE`/`ILIKE`, PostgreSQL full-text search with `tsvector`/`tsquery`, or integration with an external search service)
- Which fields of `PackageSummary` should be searchable (name only? name + license? all fields?)
- What patterns to follow from existing code (e.g., should this follow the pattern in `modules/fundamental/src/advisory/service/advisory.rs` which already has a `search` capability per the repo structure?)
- How the new `search.rs` endpoint integrates with the existing `endpoints/mod.rs` route registration

### 3. Vague: Acceptance Criteria
The current criteria are not testable:
- "Users can search for packages" — needs specifics: search by what field(s)? What is the expected endpoint?
- "Search results are relevant" — needs a definition of relevance (e.g., exact match ranked higher than partial match, results sorted by relevance score)
- "Performance is acceptable" — needs a measurable threshold (e.g., < 200ms for 10,000 packages)

### 4. Vague: Test Requirements
"Test that search works correctly" needs to be broken down into specific test cases, such as:
- Search by exact package name returns the matching package
- Search by partial name returns matching packages
- Search with no matches returns an empty result set
- Search results are paginated correctly
- Search with special characters is handled safely
- Whether to create `tests/api/package_search.rs` or add to an existing test file

### 5. Missing: Service layer files
The Files to Modify/Create sections only cover the endpoint layer. If search logic goes in the service layer (which is the established pattern in this codebase — see `advisory/service/advisory.rs` which has search), then `modules/fundamental/src/package/service/mod.rs` should appear in Files to Modify and possibly a new service file should be in Files to Create.

## Decision: Stop Execution

Per the implement-task skill's rules:

> "If any required section is missing or the description doesn't follow the template, list the gaps, ask the user for clarification, and **stop execution immediately** — do not proceed with any subsequent steps (branching, implementation planning, code changes) until the user provides the missing information."

And:

> "If the structured description is incomplete, ask the user for clarification and **stop execution**. Do not draft an implementation plan, create branches, or proceed with any subsequent steps until the user provides the missing information."

**I am stopping execution and requesting clarification on TC-9202.**

## Clarification Needed

Please provide the following information to complete the task description before implementation can proceed:

1. **API Changes**: What is the exact endpoint specification? (HTTP method, path, query parameters, response shape)
2. **Implementation Notes**: Should this use the existing `SearchService` from `modules/search/`, or implement search directly in the package service? What search mechanism (SQL pattern matching, PostgreSQL full-text search, etc.)? Which `PackageSummary` fields should be searchable?
3. **Acceptance Criteria**: Please provide specific, testable criteria with measurable outcomes.
4. **Test Requirements**: Please list the specific test scenarios to implement and the target test file(s).
5. **Files to Modify/Create**: Should the service layer (`modules/fundamental/src/package/service/mod.rs`) also be modified? Are test files needed in `tests/api/`?

No branches have been created. No code changes have been made. No Jira transitions have been performed.
