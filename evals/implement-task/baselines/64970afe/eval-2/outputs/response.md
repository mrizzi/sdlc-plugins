# TC-9202: Task Description Gaps -- Clarification Required

## Step 0 -- Validate Project Configuration

Project Configuration verified in CLAUDE.md:
- **Repository Registry**: Present with `trustify-backend` entry, Serena instance `serena_backend`, path `./`
- **Jira Configuration**: Present with Project key `TC`, Cloud ID, Feature issue type ID, Git Pull Request custom field, GitHub Issue custom field
- **Code Intelligence**: Present with tool naming convention, configured instances, and limitations

All required sections are present. Proceeding to Step 1.

## Step 1 -- Fetch and Parse Jira Task

Parsing the structured description for TC-9202 against the expected template sections:

| Section | Status | Notes |
|---|---|---|
| Repository | Present | `trustify-backend` |
| Target Branch | Present | `main` |
| Description | Present | "Add search capabilities to the package module so users can find packages more easily." |
| Files to Modify | Present | `modules/fundamental/src/package/endpoints/mod.rs` |
| Files to Create | Present | `modules/fundamental/src/package/endpoints/search.rs` |
| API Changes | **MISSING** | No API contract specified -- no endpoint path, HTTP method, request parameters, or response shape defined |
| Implementation Notes | **MISSING** | No patterns, code references, or guidance on how to implement the search |
| Acceptance Criteria | Present but **VAGUE** | See detailed analysis below |
| Test Requirements | Present but **VAGUE** | See detailed analysis below |
| Dependencies | Not present | Optional section, acceptable to omit |

### Missing: API Changes

The task asks to "add search route" and create a "search endpoint handler" but provides no API contract:
- What is the endpoint path? (e.g., `GET /api/v2/package/search` vs. query parameter on existing `GET /api/v2/package`?)
- What HTTP method should be used?
- What request parameters does the endpoint accept (query string, path params, request body)?
- What is the response shape? Should it return `PaginatedResults<PackageSummary>` consistent with the existing list endpoint, or a different shape?

### Missing: Implementation Notes

The Implementation Notes section is entirely absent. This section is critical because it provides:
- Patterns and code references to follow
- Pointers to reusable code (e.g., the existing `SearchService` in `modules/search/`, the shared query helpers in `common/src/db/query.rs`)
- Guidance on whether this should use the existing full-text search infrastructure in `modules/search/` or implement a new search mechanism within the package module
- References to sibling implementations (e.g., `AdvisoryService` already has a `search` method -- should this follow the same pattern?)

### Vague: Acceptance Criteria

Each acceptance criterion lacks the specificity needed for implementation and verification:

1. **"Users can search for packages"** -- Does not specify:
   - Which fields are searchable (package name only? version? license? description? all fields?)
   - What type of search is expected (exact match, prefix, substring, full-text/fuzzy?)
   - Whether filtering and pagination are required alongside search

2. **"Search results are relevant"** -- Does not define:
   - What "relevant" means in measurable terms
   - Whether relevance ranking is required (and if so, what ranking algorithm or scoring)
   - Whether results should be ordered by relevance score, or alphabetically, or by some other criterion
   - Whether partial matches should be included or only exact matches

3. **"Performance is acceptable"** -- Does not define:
   - What response time threshold constitutes "acceptable" (e.g., p95 < 200ms? < 500ms?)
   - Whether there is a dataset size assumption (e.g., 10K packages? 1M packages?)
   - Whether database indexing is required and, if so, whether a migration should be included in Files to Create

### Vague: Test Requirements

1. **"Test that search works correctly"** -- Does not specify:
   - What test scenarios to cover (search by name? by license? empty results? special characters?)
   - What assertions to make on the response (status code, result count, specific field values, ordering?)
   - Whether error cases should be tested (invalid query parameters, empty search term, excessively long queries)
   - Whether performance/load tests are in scope
   - Where the test file should live (presumably `tests/api/package.rs` or a new `tests/api/package_search.rs`, but this is not stated in Files to Create)

---

## Execution Halted -- Clarification Required

Per the implement-task skill rules, the structured description is incomplete. Multiple required sections are missing and several present sections are too vague to implement without guessing. **Execution is stopped.** I will not proceed with branching, implementation planning, or code changes until the following questions are answered.

### Clarifying Questions

**1. Which package fields should be searchable, and what type of search is expected?**

The `PackageSummary` struct (in `modules/fundamental/src/package/model/summary.rs`) presumably has fields like name, version, and license. Which of these fields should the search query match against? Should the search use exact matching, substring/LIKE matching, or full-text search with stemming and ranking? Should the existing `SearchService` in `modules/search/` be reused, or should this be a new query-parameter-based filter on the package list endpoint?

**2. What does "search results are relevant" mean concretely -- is relevance ranking required, and if so, what determines the ranking?**

"Relevant" is not a testable criterion as stated. Does this mean:
- Results must match the search query (basic correctness)?
- Results must be ranked by a relevance score (e.g., exact name match ranks higher than partial match)?
- Results should use PostgreSQL full-text search with `ts_rank` scoring?
- Or is this simply a restatement of "search returns correct matches" with no ranking requirement?

**3. What performance threshold is required, and does the implementation need a database migration for search indexing?**

"Performance is acceptable" needs a concrete definition. Is there a target response time (e.g., p95 < 200ms)? Is there an expected dataset size to design for? If full-text search is required, a GIN or GiST index on the relevant columns would likely be needed, which means a new database migration file should be listed in Files to Create. Should a migration be included?

**4. What is the API contract for the search endpoint?**

The API Changes section is missing entirely. What endpoint path and HTTP method should be used? What query parameters does the endpoint accept? Should the response use `PaginatedResults<PackageSummary>` (consistent with the existing list endpoint pattern), or a different response type? Should this be a new `/api/v2/package/search` route, or should search be added as a query parameter (`?q=...`) to the existing `GET /api/v2/package` list endpoint?

**5. What patterns and existing code should be followed?**

The Implementation Notes section is missing. The repository has potentially relevant existing code:
- `modules/search/` contains a `SearchService` with full-text search across entities
- `AdvisoryService` already has a `search` method
- `common/src/db/query.rs` provides shared query builder helpers for filtering, pagination, and sorting

Should the implementation follow the `AdvisoryService` search pattern? Should it integrate with or extend the existing `SearchService`? Or should it use a simpler query-parameter filter approach via the shared query helpers?

**6. What specific test scenarios and assertions are required?**

"Test that search works correctly" is not actionable. What cases should the tests cover? For example:
- Search by exact name returns the matching package
- Search by partial name returns packages containing the substring
- Search with no matches returns an empty paginated result
- Search with special characters is handled safely (no SQL injection, proper escaping)
- Search results respect pagination parameters

Also, should a test file be added to Files to Create (e.g., `tests/api/package_search.rs`)?

---

Please provide answers to these questions so I can proceed with implementation.
