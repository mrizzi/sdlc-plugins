# implement-task: TC-9202 -- Execution Halted (Incomplete Description)

## Step 0 -- Validate Project Configuration

Verified the project's CLAUDE.md contains the required Project Configuration sections:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena instance `serena_backend` at path `./`
2. **Jira Configuration** -- present, contains Project key (`TC`), Cloud ID, and Feature issue type ID
3. **Code Intelligence** -- present, with tool naming convention `mcp__<serena-instance>__<tool>` and configured instance `serena_backend` using `rust-analyzer`

Project Configuration is valid. Proceeding to Step 1.

## Step 1 -- Fetch and Parse Jira Task

Fetched TC-9202. Parsing the structured description against the required template sections:

| Section | Status | Notes |
|---|---|---|
| Repository | Present | `trustify-backend` |
| Target Branch | Present | `main` |
| Description | Present but vague | "Add search capabilities to the package module so users can find packages more easily." -- does not specify search type, searchable fields, query parameters, or relationship to the existing `modules/search/` module. |
| Files to Modify | Present | 1 file listed (`modules/fundamental/src/package/endpoints/mod.rs`) |
| Files to Create | Present | 1 file listed (`modules/fundamental/src/package/endpoints/search.rs`) |
| API Changes | **MISSING** | No endpoint path, HTTP method, query parameters, request/response shapes, or pagination details specified. |
| Implementation Notes | **MISSING** | No patterns, code references, reusable utilities, or architectural guidance provided. |
| Acceptance Criteria | Present but non-specific | All three criteria are vague and unmeasurable (see details below). |
| Test Requirements | Present but non-specific | Single item with no concrete test cases (see details below). |
| Dependencies | Not present | May be intentionally absent (no prerequisites), but the section itself is missing from the template. |

### Identified Gaps

**1. Missing: API Changes section**

This task adds a search endpoint but provides no API contract details. The following are unknown:

- Endpoint path (e.g., `GET /api/v2/package/search` or a query parameter on the existing `GET /api/v2/package`?)
- HTTP method
- Query parameters (search term field name, filtering options, pagination parameters)
- Response shape (does it return `PaginatedResults<PackageSummary>` like sibling list endpoints, or a different structure?)
- Whether this integrates with the existing `modules/search/` module's `SearchService` or is an independent implementation within the package module

**2. Missing: Implementation Notes section**

No guidance is provided on:

- Which existing patterns to follow (the repo has sibling endpoints in `sbom/endpoints/` and `advisory/endpoints/` that could serve as references -- but the task should specify this)
- Whether to reuse `common/src/db/query.rs` shared query helpers for filtering and pagination
- Whether to use the existing `SearchService` in `modules/search/` or implement search logic directly in the package service
- How search should work at the database level (SQL `LIKE`/`ILIKE`, full-text search with `tsvector`, or another mechanism)
- Whether `PackageService` in `modules/fundamental/src/package/service/mod.rs` needs a new `search` method, or if the existing `list` method should be extended
- How the new `search.rs` endpoint handler should be registered in `endpoints/mod.rs`

**3. Vague Acceptance Criteria**

The three acceptance criteria are not measurable:

- "Users can search for packages" -- by what fields? Name, version, license, PURL, all of these?
- "Search results are relevant" -- what defines relevance? Exact match? Substring? Ranked results?
- "Performance is acceptable" -- what are the performance targets? Response time threshold? Maximum result set size?

**4. Vague Test Requirements**

The single test requirement ("Test that search works correctly") provides no concrete test cases. Sibling test files in `tests/api/` (e.g., `sbom.rs`, `advisory.rs`, `search.rs`) likely test specific scenarios such as:

- Search with valid query returns matching results
- Search with no matches returns empty result set
- Search with pagination parameters returns correct page
- Search with invalid/empty query returns appropriate response
- Search result fields contain expected values

None of these scenarios are specified in the task.

## Execution Halted

The task description is incomplete and does not follow the required template. Two required sections are entirely missing (**API Changes**, **Implementation Notes**), and two present sections (**Acceptance Criteria**, **Test Requirements**) lack the specificity needed to implement and verify the feature.

Per the implement-task skill rules: "If any required section is missing or the description doesn't follow the template, list the gaps, ask the user for clarification, and stop execution immediately."

No implementation plan has been drafted. No branches have been created. No code changes have been made.

### Clarifying Questions

Before this task can proceed, the following information is needed:

1. **API Changes**: What is the endpoint path, HTTP method, and query parameter design for the search? Should it return `PaginatedResults<PackageSummary>` consistent with the existing list endpoint pattern?

2. **Search mechanism**: Should search be implemented using the existing `SearchService` in `modules/search/`, or as a standalone query in the package module? What database search strategy should be used (SQL `ILIKE`, PostgreSQL full-text search, etc.)?

3. **Searchable fields**: Which fields of a package are searchable (name, version, license, PURL, description)?

4. **Implementation Notes**: What sibling patterns should be followed? Should the implementation mirror the `advisory` module's search endpoint (which already has a `search` method in `AdvisoryService`)?

5. **Acceptance Criteria**: What are the concrete, measurable criteria? For example: "Search by package name substring returns matching packages within 500ms for datasets up to 10,000 packages."

6. **Test Requirements**: What specific test scenarios should be covered? For example: exact match, partial match, no results, pagination, empty query handling.

Please provide the missing information or re-run plan-feature to generate a complete task description, then re-invoke `/implement-task TC-9202`.
