# TC-9202: Add package search functionality

## Status: Blocked -- Clarification Required

I have reviewed the structured task description for TC-9202 and identified several gaps that prevent me from proceeding with implementation planning. The task description is incomplete, and per workflow rules I must ask for clarification before drafting an implementation plan, creating branches, or taking any further action.

---

## Missing and Incomplete Sections

### 1. Implementation Notes section is missing entirely

The task description does not include an **Implementation Notes** section. This section is required and should provide technical guidance such as: which search mechanism to use (e.g., PostgreSQL full-text search via `tsvector`/`tsquery`, SQL `LIKE`/`ILIKE`, integration with the existing `modules/search/` service, or an external search engine), how to integrate with the existing codebase patterns, relevant database considerations, and any architectural constraints. Without this section, I cannot determine the intended technical approach and would be guessing at the implementation strategy.

### 2. Acceptance Criteria are vague and not implementation-ready

The current acceptance criteria lack the specificity needed to guide implementation or verify correctness:

- **"Search results are relevant"** -- This is insufficiently specific. What defines relevance? Which fields should be matched against the search query (package name only? version? description? license? pURL?)? Should results be ranked, and if so, by what criteria (exact match first, then partial match, then fuzzy)? Is there a minimum relevance threshold? Without a concrete definition of "relevant," there is no way to implement or verify this criterion.

- **"Performance is acceptable"** -- This is insufficiently specific. What is the performance threshold? Is there a maximum response time target (e.g., p95 < 200ms)? What is the expected dataset size (hundreds, thousands, millions of packages)? Should the search use database indexes, and if so, what kind? Without concrete performance requirements, I cannot make informed decisions about indexing strategy, query optimization, or whether caching (the project uses `tower-http` caching middleware) is needed.

- **"Users can search for packages"** -- This is functional but underspecified. What query parameters should the endpoint accept? Should it support filtering, pagination, and sorting like other list endpoints in this codebase (which use `PaginatedResults<T>` and `common/src/db/query.rs` helpers)?

### 3. Test Requirements are vague and untestable as stated

The sole test requirement -- **"Test that search works correctly"** -- does not define what "correctly" means. Effective test requirements should specify concrete scenarios: searching by exact name, partial match, no results found, empty query handling, pagination of results, special character handling, SQL injection prevention, etc. The existing test patterns in `tests/api/` (e.g., `sbom.rs`, `advisory.rs`, `search.rs`) use integration tests against a real PostgreSQL test database, but the test cases themselves need to be defined based on the search behavior specification.

---

## Clarifying Questions

Before I can proceed with an implementation plan, I need answers to the following questions:

1. **Which package fields should be searchable?** Looking at the repository structure, `PackageSummary` in `modules/fundamental/src/package/model/summary.rs` includes at least a license field, and the `package` entity in `entity/src/package.rs` likely has fields like name, version, and pURL. Should the search match against all of these fields, or only specific ones (e.g., name and version)? Should the search also span related entities such as `package_license` or `sbom_package`?

2. **What does "relevant" mean for search result ranking?** Should results be ranked by relevance score (e.g., exact match > prefix match > substring match > fuzzy match), or is unranked filtering sufficient? If ranking is needed, should this use PostgreSQL full-text search with `ts_rank`, the existing `modules/search/` service (`SearchService` provides full-text search across entities), or a simpler `ILIKE` approach? The choice fundamentally changes the implementation.

3. **What is the concrete performance threshold?** What maximum response time is acceptable, and at what data scale? For example, "p95 latency under 200ms for a dataset of 100,000 packages" would be actionable. This determines whether a simple query suffices or whether I need to add database indexes, use the existing search infrastructure, or configure caching middleware.

4. **Should the search endpoint follow the same pagination, filtering, and sorting conventions as other list endpoints?** The codebase uses `PaginatedResults<T>` and shared query helpers in `common/src/db/query.rs` for all list endpoints. Should the new search endpoint return `PaginatedResults<PackageSummary>` and support the same query parameters, or does it have different response requirements?

5. **What should happen for edge cases?** How should the endpoint handle an empty search query, very short queries (single character), or queries with special characters? Should there be a minimum query length?

---

## Next Steps

Once these questions are answered, I will:

1. Draft a complete implementation plan covering the search endpoint, service layer, query logic, and tests
2. Create the feature branch `tc-9202/add-package-search`
3. Proceed with implementation following the plan

I will not proceed until the missing information is provided.
