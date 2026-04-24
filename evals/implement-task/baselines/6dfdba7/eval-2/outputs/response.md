# implement-task TC-9202 -- Clarification Required

I have fetched and reviewed Jira task TC-9202 ("Add package search functionality") and validated the project configuration against the CLAUDE.md Project Configuration section. The target repository is `trustify-backend` with Serena instance `serena_backend`.

Before proceeding with implementation, I must stop and request clarification. The task description has several gaps and ambiguities that prevent me from producing a reliable implementation plan. Per constraint 1.6, I must not improvise implementation details or draft a plan when the structured description is incomplete.

---

## Gaps Identified

### 1. Missing Implementation Notes Section

The task description does not contain an **Implementation Notes** section. This section is expected in well-formed tasks produced by `plan-feature` and is essential for guiding implementation. Without it, I cannot determine:

- Which search mechanism to use -- the repository already has a `modules/search/` module with `SearchService` (full-text search across entities at `GET /api/v2/search`). Should the package search reuse this infrastructure, or should it be a filtered query added to the existing package list endpoint?
- Which existing patterns or utilities from `common/src/db/query.rs` (shared filtering, pagination, sorting helpers) should be applied.
- Whether the search endpoint should be a new route (`GET /api/v2/package/search`) or a query-parameter extension on the existing `GET /api/v2/package` list endpoint (e.g., `?q=<term>`).
- What SeaORM query patterns to follow -- the advisory module appears to have a `search` method in `AdvisoryService` that could serve as a reference, but the task does not point to it.

### 2. Vague Acceptance Criteria

Two of the three acceptance criteria are not specific enough to implement or verify:

- **"Search results are relevant"** -- The word "relevant" is undefined. It does not specify:
  - Which fields are searched (package name? version? license? PURL?).
  - What type of matching is expected (exact, prefix/starts-with, substring/contains, or full-text with stemming).
  - Whether or how results should be ranked (exact matches first? alphabetical? insertion order?).
  - Whether matching should be case-insensitive.

- **"Performance is acceptable"** -- "Acceptable" has no measurable definition. There is no:
  - Latency target (e.g., p95 < 200ms).
  - Dataset size assumption (e.g., "with 10,000 packages in the database").
  - Indexing requirement (e.g., "must use a database index on the package name column").
  - Pass/fail threshold that could be verified in Step 8 (Verify Acceptance Criteria).

Without concrete, measurable acceptance criteria, I cannot objectively verify the implementation.

### 3. Vague Test Requirements

The single test requirement -- **"Test that search works correctly"** -- does not define what "correctly" means. It does not specify:

- Which test scenarios to cover: basic name match, no-results case, partial match, case sensitivity behavior, empty query handling, special characters in query, pagination of search results.
- Which response fields to assert on beyond HTTP status code (e.g., result count, matched package names, ordering).
- Whether error cases need coverage (invalid query parameter, missing required parameter, malformed input).
- Whether the test should use the existing integration test pattern from `tests/api/` (hitting a real PostgreSQL test database), which is the convention observed in the repository.

The implement-task skill requires test requirements specific enough to drive test file creation and to verify each acceptance criterion through tests.

### 4. Incomplete File Scope

The task lists only one file to modify (`modules/fundamental/src/package/endpoints/mod.rs`) and one file to create (`modules/fundamental/src/package/endpoints/search.rs`). However, depending on the answers to the clarifying questions below, additional files may be needed:

- A service method in `modules/fundamental/src/package/service/mod.rs` to contain the search query logic (following the module pattern of model/service/endpoints observed in sibling modules like `sbom` and `advisory`).
- An integration test file in `tests/api/` (e.g., `tests/api/package.rs` or `tests/api/package_search.rs`).
- Potentially a database migration in `migration/` if an index is required.

These gaps in file scope cannot be resolved without first clarifying the implementation approach.

---

## Clarifying Questions

I need answers to the following questions before I can proceed:

**Q1 -- Which fields should the search query match against?**

Should the search match on package name only, or also on other fields such as version, license, and PURL? Should matching be exact, prefix (starts-with), substring (contains), or full-text? Should it be case-insensitive?

**Q2 -- What does "relevant" mean for result ranking?**

Should results be returned in a specific order (e.g., exact matches ranked above partial matches, then alphabetical)? Or is relevance ranking not required -- any matching result set in an unspecified order is acceptable? If ranking is required, what is the ranking algorithm?

**Q3 -- What is the measurable performance threshold?**

Is there a latency target (e.g., p95 under 200ms for a dataset of N packages)? Should the search use a database index, and if so, does one already exist on the relevant columns in the `package` entity, or does a migration need to be created? Or does "acceptable" simply mean the endpoint must not perform an unbounded full table scan?

**Q4 -- Should the search reuse the existing `modules/search/` infrastructure or be a filtered query on the package endpoint?**

The repository has `modules/search/src/service/mod.rs` providing `SearchService` for full-text search across entities, exposed at `GET /api/v2/search`. Should package search be:
- (a) A query parameter filter on the existing `GET /api/v2/package` list endpoint (e.g., `?q=<term>`), following the pattern used by list endpoints with `common/src/db/query.rs` helpers.
- (b) A dedicated `GET /api/v2/package/search` route with its own handler.
- (c) An extension to the existing `SearchService` in `modules/search/`.

This decision affects file scope, service layer changes, and the API contract.

**Q5 -- What specific test scenarios are required?**

Please confirm which of the following should be covered by integration tests:
- A query that matches one or more packages by name.
- A query that returns zero results.
- Pagination of search results (using `PaginatedResults<T>`).
- An error response for a missing or empty query parameter.
- Case-insensitive matching behavior.
- Partial match vs. exact match behavior.

---

## Next Steps

Once these questions are answered, I will:
1. Inspect the existing code (advisory search pattern, package service, query helpers) using Serena/Read tools.
2. Produce a scoped implementation plan with concrete file changes.
3. Proceed through the remaining implement-task steps (branch creation, implementation, testing, commit, PR).

I will not proceed until the ambiguities above are resolved.
