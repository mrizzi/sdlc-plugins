# implement-task: TC-9202 -- Analysis and Clarification Request

## Step 0 -- Validate Project Configuration

The project's CLAUDE.md (claude-md-mock.md) contains the required sections:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena Instance `serena_backend` and Path `./`.
2. **Jira Configuration** -- present, contains Project key (`TC`), Cloud ID, Feature issue type ID, and custom fields.
3. **Code Intelligence** -- present, lists `serena_backend` with `rust-analyzer`.

Project Configuration is valid. Proceeding.

## Step 1 -- Fetch and Parse Jira Task

**Parsed sections from TC-9202:**

| Section | Status | Content |
|---|---|---|
| Repository | Present | `trustify-backend` |
| Target Branch | Present | `main` |
| Description | Present | "Add search capabilities to the package module so users can find packages more easily." |
| Files to Modify | Present | `modules/fundamental/src/package/endpoints/mod.rs` -- add search route |
| Files to Create | Present | `modules/fundamental/src/package/endpoints/search.rs` -- search endpoint handler |
| API Changes | **MISSING** | No API Changes section provided |
| Implementation Notes | **MISSING** | No Implementation Notes section provided |
| Acceptance Criteria | Present but **VAGUE** | See details below |
| Test Requirements | Present but **VAGUE** | See details below |
| Dependencies | Not present | (optional, acceptable) |
| Target PR | Not present | (optional, acceptable) |
| Bookend Type | Not present | (optional, acceptable) |

### Gaps Identified

#### 1. MISSING: Implementation Notes

The task description contains **no Implementation Notes section**. This is a critical gap. Implementation Notes are expected to reference real code patterns, existing utilities, structs, service methods, and sibling implementations that should be followed. Without them, there is no guidance on:

- Which existing service methods or query helpers to use or extend (e.g., does `PackageService` in `modules/fundamental/src/package/service/mod.rs` already have search-related methods, or must new ones be added?)
- Which patterns from sibling modules to follow (e.g., the advisory module has an `AdvisoryService` with a `search` method -- should the package search follow the same pattern?)
- How to integrate with the existing `SearchService` in `modules/search/` vs. building module-local search
- What request/response types to use or create
- How search queries should be constructed (SQL `LIKE`, PostgreSQL full-text search with `tsvector`/`tsquery`, or something else)

#### 2. MISSING: API Changes

There is no API Changes section specifying the endpoint path, HTTP method, query parameters, or response format for the new search capability.

#### 3. VAGUE: Acceptance Criteria

The acceptance criteria are insufficiently specific for implementation:

- **"Users can search for packages"** -- Does not specify which fields are searchable (package name? version? license? description? pURL?), what the search input format is (free-text query string? structured filters? both?), or what the API endpoint shape looks like.
- **"Search results are relevant"** -- "Relevant" is undefined. Does this mean exact match? Substring match? Full-text search with ranking? If ranking is expected, what relevance algorithm or scoring mechanism should be used? Is there a minimum relevance threshold? Should results be ordered by relevance score, and if so, what constitutes "relevant enough" to include?
- **"Performance is acceptable"** -- "Acceptable" is undefined. What is the target response time? (e.g., < 200ms for 95th percentile?) What is the expected dataset size? (100 packages? 100,000 packages?) Should the implementation use database indexes, and if so, on which columns? Is there a maximum result set size or pagination requirement?

#### 4. VAGUE: Test Requirements

- **"Test that search works correctly"** -- "Correctly" is not defined. Without knowing what fields are searchable, what relevance means, and what edge cases matter, it is impossible to write meaningful tests. This criterion does not specify:
  - What inputs to test with (exact matches, partial matches, case sensitivity, special characters, empty queries)
  - What outputs to assert on (result count, result ordering, specific field values, response shape)
  - What error cases to cover (empty results, invalid query parameters, oversized queries)
  - Whether integration tests against a real database are expected (the repo convention is integration tests in `tests/api/` against PostgreSQL)

---

## Execution Halted -- Clarification Required

Per the implement-task skill rules: "If the structured description is incomplete, ask the user for clarification and **stop execution immediately**. Do not draft an implementation plan, create branches, or proceed with any subsequent steps until the user provides the missing information."

The task description is missing required sections and contains vague criteria that would require guessing to implement. I am stopping execution and requesting the following clarifications before proceeding:

### Clarifying Questions

1. **Which fields should be searchable?**
   The `PackageSummary` struct is in `modules/fundamental/src/package/model/summary.rs`, and the `package` entity is in `entity/src/package.rs`. Which fields should the search cover -- package name only, or also version, license (via `package_license` entity), pURL, description, or other fields? Should the search support filtering on individual fields, or is it a single free-text query across multiple fields?

2. **What does "relevant" mean for search results, and how should results be ranked?**
   Should this be a simple SQL `LIKE`/`ILIKE` substring match, or a PostgreSQL full-text search using `tsvector`/`tsquery` with relevance ranking? If ranking is expected, what scoring model should be used? Should the existing `SearchService` in `modules/search/` be extended to cover packages, or should this be a standalone search within the package module? The advisory module appears to have its own search capability in `AdvisoryService` -- should the package search follow that same pattern?

3. **What is the specific performance threshold?**
   What response time is considered "acceptable"? What is the expected scale of the package table (number of rows)? Should database indexes be created as part of this task, and if so, should a new migration be added under `migration/`?

4. **What is the API endpoint contract?**
   What should the endpoint path be (e.g., `GET /api/v2/package/search?q=...` or `GET /api/v2/package?search=...` as a query parameter on the existing list endpoint)? What query parameters should it accept? Should the response use `PaginatedResults<PackageSummary>` from `common/src/model/paginated.rs` consistent with other list endpoints?

5. **What specific test scenarios define "works correctly"?**
   What are the concrete test cases? For example: exact name match returns the package, partial name match returns relevant results, search with no matches returns an empty paginated response, search with special characters is handled safely. Should tests follow the integration test pattern in `tests/api/` (hitting a real PostgreSQL test database), and should there be a new test file like `tests/api/package_search.rs`?

6. **Please provide Implementation Notes** referencing the specific patterns, structs, service methods, and sibling code to follow. For example, should this follow the pattern of `AdvisoryService::search` in `modules/fundamental/src/advisory/service/advisory.rs`, and should the query use helpers from `common/src/db/query.rs`?

---

I will not proceed with branching, implementation planning, code changes, or any subsequent steps until these questions are answered and the task description is updated with the missing Implementation Notes, clarified Acceptance Criteria, and specific Test Requirements.
