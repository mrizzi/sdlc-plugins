# TC-9202: Add package search functionality -- Clarification Required

## Task Analysis

I reviewed the task description for TC-9202 and the target repository structure. Before proceeding with implementation, I need to flag several gaps in the task description that prevent me from implementing this correctly.

### Missing Implementation Notes

The task description does not include an **Implementation Notes** section. For a search feature, implementation notes are critical because they specify the technical approach -- for example, whether to use PostgreSQL full-text search (`tsvector`/`tsquery`), SQL `LIKE`/`ILIKE` queries, or integrate with the existing `modules/search/` service that already provides full-text search across entities. Without this guidance, I would be guessing at the intended architecture.

### Vague Acceptance Criteria

The acceptance criteria are too imprecise to implement against:

- **"Search results are relevant"** -- This is not actionable. "Relevant" is undefined. Does this mean exact match on package name? Substring match? Full-text search with ranking? Should results be sorted by relevance score, or by name, or by recency?
- **"Performance is acceptable"** -- This provides no measurable threshold. Acceptable could mean under 100ms, under 1 second, or under 5 seconds. Without a concrete target, there is no way to verify this criterion or choose an appropriate implementation strategy (e.g., whether an index is needed).

### Vague Test Requirements

The test requirements state only "test that search works correctly." This does not define what "correctly" means. There are no specifications for edge cases (empty query, no results, special characters), expected result ordering, pagination behavior, or error handling scenarios.

## Clarifying Questions

I need answers to the following before I can proceed:

1. **Which fields should be searchable?** The `PackageSummary` struct exists in `modules/fundamental/src/package/model/summary.rs`. Should search cover only the package name, or also other fields such as version, license, or description? Should the search match against related entities (e.g., SBOMs linked to a package)?

2. **What does "relevant" mean for search result ranking?** Should results be ranked by a relevance score (e.g., using PostgreSQL `ts_rank`), or is a simple filtered list sufficient? Should exact matches appear before partial matches? Is there an existing relevance model in the `modules/search/` service that should be reused?

3. **What is the concrete performance requirement?** What is the maximum acceptable response time for a search query? What is the expected dataset size (number of packages) this needs to perform well against? This determines whether a database index, caching, or the existing `tower-http` caching middleware is needed.

4. **Should this integrate with the existing search module?** The repository already has `modules/search/` with a `SearchService` providing full-text search across entities at `GET /api/v2/search`. Should the package search be added there, or should it be a separate endpoint under `GET /api/v2/package/search` as the task's file list implies? If separate, should both endpoints exist?

5. **What query parameters should the search endpoint accept?** Beyond a search term (`q`), should the endpoint support filtering (e.g., by license), pagination (using the existing `PaginatedResults<T>` pattern), and sorting? What is the default page size?

6. **What are the expected test scenarios?** Specifically: should tests cover empty search queries, queries with no matching results, queries with special characters, pagination of search results, and performance under load? What fixtures or test data should be used?

Please provide clarification on these points so I can proceed with a correct and complete implementation.
