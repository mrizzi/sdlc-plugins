# implement-task TC-9202 — Clarification Required

I have fetched and parsed Jira task TC-9202 ("Add package search functionality") and validated the project configuration. Before proceeding with implementation, I need to stop and flag several gaps in the task description.

## Gaps Found in TC-9202

### 1. Missing Section: Implementation Notes

The task description does not include an **Implementation Notes** section. This section is required by the implement-task skill — it specifies which code patterns, utilities, and existing helpers to follow during implementation.

Without Implementation Notes, I cannot determine:
- Which search mechanism to use (the existing `modules/search/` full-text search module, raw SQL `ILIKE` queries, SeaORM filter expressions, or something else)
- Whether to reuse `SearchService` from `modules/search/src/service/mod.rs` or implement search logic directly in the package service
- Which query builder helpers from `common/src/db/query.rs` are applicable
- Whether the endpoint should live at `/api/v2/package/search` or be a query parameter on the existing `GET /api/v2/package` list endpoint

### 2. Vague Acceptance Criteria

The two criteria below are not testable as written:

- **"Search results are relevant"** — "relevant" is undefined. It does not say which fields are searched (package name, version, license, PURL?), whether matching is exact, prefix, substring, or full-text, or how results should be ranked when multiple packages match.
- **"Performance is acceptable"** — "acceptable" has no measurable definition. No latency target (e.g., p95 < 200 ms), no dataset size assumption, and no threshold for test pass/fail is specified.

Without concrete, measurable criteria, Step 8 (Verify Acceptance Criteria) cannot be completed objectively.

### 3. Vague Test Requirements

The single test requirement — **"Test that search works correctly"** — does not define what "correctly" means. It does not specify:
- Which scenarios to cover (basic name match, no-results case, partial match, case sensitivity, empty query, pagination of search results)
- Which fields the test should assert on beyond status code
- Whether error cases (invalid query, missing parameter) need test coverage

The implement-task skill requires Test Requirements specific enough to drive test implementation and verify acceptance criteria through tests.

---

## Clarifying Questions

Please answer the following before I proceed:

**Q1 — Which fields should the search query match against?**

For example: package name only, or also version, license, and PURL? Should the match be exact, prefix (starts-with), substring (contains), or full-text? Should it be case-insensitive?

**Q2 — What does "relevant" mean for result ranking?**

Should results be returned in a fixed order (e.g., alphabetical by name, or insertion order)? Should exact matches rank above partial matches? Or is relevance ranking not required and any matching result set in an unspecified order is acceptable?

**Q3 — What is the performance threshold for "acceptable"?**

Is there a latency target (e.g., p95 under 200 ms for a dataset of N packages)? Should the search endpoint use a database index, and if so, is there an existing index on the relevant columns in the `package` entity? Or does "performance is acceptable" simply mean the endpoint should not do a full table scan without a `LIMIT`?

**Q4 — Should search reuse the existing `modules/search/` full-text search infrastructure, or be implemented as a filtered query on the package list endpoint?**

The repository already has `modules/search/src/service/mod.rs` (a cross-entity full-text search service) and `GET /api/v2/search`. Should package search be a thin filter on `GET /api/v2/package?q=<term>`, a dedicated `GET /api/v2/package/search` route, or routed through the existing search module? This affects both the file scope and the API contract.

**Q5 — What specific test scenarios should be covered?**

At minimum, please confirm which of the following are required:
- A query that matches one or more packages by name
- A query that returns zero results
- Pagination of search results (if the endpoint is paginated)
- An error response for a missing or empty query parameter (if the parameter is required)

---

Once these questions are answered, I can proceed with Step 4 (code inspection) and produce a complete implementation plan with no ambiguity.
