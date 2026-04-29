# implement-task: TC-9202 -- Validation Result

## Step 0 -- Validate Project Configuration

Project Configuration in CLAUDE.md verified:
- **Repository Registry** -- present, contains `trustify-backend` with Serena instance `serena_backend`
- **Jira Configuration** -- present, contains Project key (`TC`), Cloud ID, Feature issue type ID
- **Code Intelligence** -- present, tool naming convention documented (`mcp__<serena-instance>__<tool>`)

Project Configuration is valid. Proceeding to Step 1.

## Step 1 -- Fetch and Parse Jira Task

Parsing the structured description for TC-9202 against the required template sections:

| Required Section        | Status      | Notes                                                        |
|-------------------------|-------------|--------------------------------------------------------------|
| Repository              | Present     | `trustify-backend`                                           |
| Description             | Present     | "Add search capabilities to the package module..."           |
| Files to Modify         | Present     | 1 file listed                                                |
| Files to Create         | Present     | 1 file listed                                                |
| API Changes             | **MISSING** | No API Changes section -- endpoint path, HTTP method, request/response shapes are undefined |
| Implementation Notes    | **MISSING** | No Implementation Notes section -- no patterns, code references, or reusable code identified |
| Acceptance Criteria     | **VAGUE**   | Criteria are not specific or measurable (see details below)  |
| Test Requirements       | **VAGUE**   | Requirements do not define what "correctly" means (see details below) |
| Dependencies            | Not present | No dependencies listed (acceptable -- this section is optional when there are none) |

### Missing: Implementation Notes

The task description contains no **Implementation Notes** section. This section is required and should specify:
- Which existing patterns to follow (e.g., how the `advisory` module's search works, or how `common/src/db/query.rs` query helpers should be used)
- Code references for reusable utilities (e.g., `PaginatedResults<T>`, `AppError`, query builder helpers)
- How the search endpoint should integrate with the existing module structure (service layer, route registration)
- Whether to use the existing `modules/search/` full-text search infrastructure or implement module-local search

### Missing: API Changes

The task description contains no **API Changes** section. This section is required and should specify:
- The endpoint path (e.g., `GET /api/v2/package/search` or a query parameter on `GET /api/v2/package`)
- HTTP method
- Request parameters (query string, path parameters, request body)
- Response shape (fields, pagination, status codes)

### Vague: Acceptance Criteria

The listed acceptance criteria are not specific or measurable:

1. **"Users can search for packages"** -- Does not specify:
   - Which fields are searchable (package name? version? license? description? pURL?)
   - What the search input looks like (free-text query string? structured filters? both?)
   - Whether partial matching, prefix matching, or exact matching is expected

2. **"Search results are relevant"** -- Does not define:
   - What "relevant" means in this context
   - Whether there is a relevance ranking algorithm (e.g., TF-IDF, Levenshtein distance, simple `ILIKE`)
   - How results should be ordered (by relevance score? alphabetically? by creation date?)

3. **"Performance is acceptable"** -- Does not define:
   - A concrete performance threshold (e.g., "p95 latency under 200ms for 10,000 packages")
   - The expected dataset size
   - Whether database indexing is required

### Vague: Test Requirements

The single test requirement -- **"Test that search works correctly"** -- is not actionable:
- It does not define what "correctly" means
- It does not specify test scenarios (empty query, no results, partial match, exact match, special characters, pagination)
- It does not specify whether integration tests, unit tests, or both are required
- It does not follow the testing patterns established in the repository (e.g., `tests/api/` integration tests with status code assertions)

---

## Execution Stopped -- Clarification Required

Per the skill instructions: "If any required section is missing or the description doesn't follow the template, list the gaps, ask the user for clarification, and **stop execution immediately**."

The task description is missing required sections and contains vague criteria that would force me to guess at implementation details. I will not proceed with branching, code analysis, or implementation until the following questions are answered.

### Clarifying Questions

1. **Which package fields should be searchable?** The `PackageSummary` struct in `modules/fundamental/src/package/model/summary.rs` likely contains fields such as name, version, and license. Which of these fields should the search query match against? Should it support searching by pURL (Package URL)? Should search match against related SBOM data?

2. **What does "relevant" mean for search result ranking?** Should results be ranked by a relevance score (e.g., exact match first, then prefix match, then substring match)? Or is a simple SQL `ILIKE` filter with no ranking sufficient? If ranking is needed, what algorithm or approach should be used?

3. **What is the concrete performance threshold?** "Performance is acceptable" is not measurable. What is the maximum acceptable response time (e.g., p95 < 200ms)? What is the expected dataset size (hundreds, thousands, millions of packages)? Does the search require a database index, or is a sequential scan acceptable?

4. **What is the API contract for the search endpoint?** Should this be a new dedicated endpoint (e.g., `GET /api/v2/package/search?q=...`) or a query parameter added to the existing list endpoint (`GET /api/v2/package?q=...`)? What should the response shape look like -- should it reuse `PaginatedResults<PackageSummary>` like the existing list endpoint?

5. **What patterns should the implementation follow?** The repository has an existing `modules/search/` module with a `SearchService` for full-text search across entities. Should the package search integrate with this existing search infrastructure, or should it be a module-local search implementation similar to how `advisory` search works (via `AdvisoryService`)? What query builder helpers from `common/src/db/query.rs` should be used?

6. **What specific test scenarios are required?** "Test that search works correctly" needs to be broken down. At minimum, should the tests cover: (a) search with results, (b) search with no results, (c) search with empty/missing query parameter, (d) pagination of search results, (e) search with special characters? Should these be integration tests in `tests/api/` following the existing pattern?

Please provide the missing **Implementation Notes** and **API Changes** sections, refine the **Acceptance Criteria** with measurable thresholds, and specify concrete **Test Requirements** so I can proceed with the implementation.
