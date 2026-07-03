# implement-task: TC-9202 — Add package search functionality

## Step 0 — Validate Project Configuration

Verified the project's CLAUDE.md contains the required sections under `# Project Configuration`:

1. **Repository Registry** — present, contains `trustify-backend` with Serena instance `serena_backend` at path `./`
2. **Jira Configuration** — present with Project key (`TC`), Cloud ID, Feature issue type ID, Git Pull Request custom field (`customfield_10875`), and GitHub Issue custom field (`customfield_10747`)
3. **Code Intelligence** — present with tool naming convention (`mcp__<serena-instance>__<tool>`) and configured instance `serena_backend` using `rust-analyzer`

Configuration validation passed.

## Step 0.5 — JIRA Access Initialization

Would attempt MCP first for all Jira operations. If MCP fails, would prompt user with fallback options (REST API, skip, or retry).

## Step 1 — Fetch and Parse Jira Task

Fetched TC-9202. Parsed the structured description and identified the following:

| Section | Status | Content |
|---|---|---|
| Repository | Present | `trustify-backend` |
| Target Branch | Present | `main` |
| Description | **Incomplete** | "Add search capabilities to the package module so users can find packages more easily." — too vague; does not specify what search fields, what search mechanism (full-text, LIKE, filter), or how results should be shaped |
| Files to Modify | Present | `modules/fundamental/src/package/endpoints/mod.rs` — add search route |
| Files to Create | Present | `modules/fundamental/src/package/endpoints/search.rs` — search endpoint handler |
| API Changes | **Missing** | No API endpoint specification — for a new search endpoint, this section must define the HTTP method, path, query parameters, and response shape |
| Implementation Notes | **Missing** | No patterns, code references, or guidance on how to implement the search. This section is critical — it should reference existing patterns (e.g., how `advisory/service/advisory.rs` implements its `search` method), shared utilities to reuse (e.g., `common/src/db/query.rs` for filtering/pagination), and specific structs/functions to follow |
| Acceptance Criteria | **Vague** | All three criteria are non-actionable: "Users can search for packages" (by what field? name? purl? license?), "Search results are relevant" (what defines relevance?), "Performance is acceptable" (what threshold?) |
| Test Requirements | **Vague** | Single criterion "Test that search works correctly" — does not specify which scenarios to test, expected response codes, edge cases, or error cases |
| Dependencies | Not present | No dependencies listed — acceptable if there are none |

### Gaps Requiring Clarification

**STOP — Execution halted.** The task description does not follow the structured template and has critical gaps. The following clarifications are needed before implementation can proceed:

1. **API Changes section is missing.** For a new search endpoint, I need:
   - What is the endpoint path? (e.g., `GET /api/v2/package/search` or `GET /api/v2/package` with query parameters?)
   - What query parameters does it accept? (e.g., `q` for free-text, `name`, `purl`, `license`, `namespace`?)
   - What is the response shape? (e.g., `PaginatedResults<PackageSummary>` following the existing list pattern?)
   - Does it support pagination, sorting, and filtering like other list endpoints?

2. **Implementation Notes section is missing.** I need guidance on:
   - Which search mechanism to use — should this use the existing `SearchService` from `modules/search/` for full-text search, or implement filtering directly in `PackageService` using `common/src/db/query.rs` helpers?
   - What patterns to follow — the `advisory` module already has a `search` capability in `AdvisoryService` (`modules/fundamental/src/advisory/service/advisory.rs`). Should the package search follow the same approach?
   - How should the search handler integrate with existing service code — does `PackageService` (`modules/fundamental/src/package/service/mod.rs`) need a new `search` method, or should the existing `list` method be extended with filtering?
   - Are there reuse candidates in `common/src/db/query.rs` (shared query builder helpers for filtering, pagination, sorting) that should be leveraged?

3. **Acceptance Criteria are too vague to verify.** I need specific, testable criteria such as:
   - Which fields are searchable (package name, purl, license, namespace)?
   - What matching behavior is expected (exact match, prefix, substring, full-text)?
   - What constitutes "acceptable performance" (response time threshold, index requirements)?
   - Should results include pagination metadata (`total_count`, `offset`, `limit`)?

4. **Test Requirements are too vague to implement.** I need specific test scenarios such as:
   - Search by name returns matching packages
   - Search with no results returns empty paginated response
   - Search with special characters is handled safely
   - Pagination parameters work correctly with search
   - Invalid search parameters return appropriate error responses (400/422)

### What I Would Do Next

Once the user provides the missing information and the task description is updated to follow the structured template, I would proceed with:

- **Step 1.5**: Verify description integrity via the digest protocol
- **Step 2**: Verify dependencies (none listed, so skip)
- **Step 3**: Transition TC-9202 to In Progress and assign to current user
- **Step 4**: Understand the code using `mcp__serena_backend__get_symbols_overview` and `mcp__serena_backend__find_symbol` to inspect:
  - `modules/fundamental/src/package/endpoints/mod.rs` — current route registration pattern
  - `modules/fundamental/src/package/endpoints/list.rs` — existing list endpoint as sibling reference
  - `modules/fundamental/src/package/service/mod.rs` — PackageService capabilities
  - `modules/fundamental/src/package/model/summary.rs` — PackageSummary struct
  - `common/src/db/query.rs` — shared query helpers for filtering/pagination
  - `common/src/model/paginated.rs` — PaginatedResults wrapper
  - `modules/fundamental/src/advisory/service/advisory.rs` — AdvisoryService search as pattern reference
  - `modules/search/src/service/mod.rs` — SearchService for potential reuse
  - `CONVENTIONS.md` at repository root — project conventions and CI check commands
  - Sibling endpoints (`sbom/endpoints/`, `advisory/endpoints/`) for convention conformance analysis
  - Sibling test files (`tests/api/sbom.rs`, `tests/api/advisory.rs`, `tests/api/search.rs`) for test convention analysis
- **Step 5**: Create branch `TC-9202` from `main`
- **Step 6**: Implement the search endpoint in `search.rs`, register the route in `mod.rs`, following conventions discovered in Step 4
- **Step 7**: Write tests in `tests/api/` following test conventions from sibling analysis
- **Step 8**: Verify each acceptance criterion
- **Step 9**: Self-verification (scope containment, untracked file check, sensitive-pattern check, documentation currency, duplication check, CI checks, data-flow trace, contract and sibling parity)
- **Step 10**: Commit with conventional commit format (`feat(package): add search endpoint`) and create PR targeting `main` with `Implements [TC-9202](<webUrl>)` in the description
- **Step 11**: Update Jira — set `customfield_10875` with PR URL in ADF format, add comment with PR link and summary, transition to In Review
