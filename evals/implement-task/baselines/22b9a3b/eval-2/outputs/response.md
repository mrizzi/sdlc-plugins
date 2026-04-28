# TC-9202: Add package search functionality

## Status: Blocked -- Clarification Required

I cannot proceed with implementation because the task description for TC-9202 is incomplete. Per workflow constraints, I must ask for clarification rather than improvise when required details are missing.

---

## Missing Information

### 1. Acceptance Criteria Are Too Vague

The current acceptance criteria are not actionable:

- **"Users can search for packages"** -- What fields should be searchable? Package name only, or also version, namespace, description, license, associated SBOM data? What query parameters should the endpoint accept (e.g., `q`, `name`, `license`)?
- **"Search results are relevant"** -- What defines relevance? Is this prefix matching, substring matching, full-text search with ranking, or exact match? Should results be ordered by relevance score?
- **"Performance is acceptable"** -- What is the performance target? Is there a maximum response time (e.g., < 200ms for 95th percentile)? What dataset size should this be tested against?

### 2. No API Contract Specified

The task does not define the search endpoint contract:

- What is the route? Presumably `GET /api/v2/package/search` or a query parameter on `GET /api/v2/package`, but this is not stated.
- What are the request query parameters (search term, filters, pagination, sorting)?
- What is the response shape? Should it return `PaginatedResults<PackageSummary>` consistent with the existing list endpoint, or a different response type with relevance scores?

### 3. No Implementation Notes

There is no guidance on the implementation approach:

- Should this integrate with the existing `modules/search/` module and its `SearchService` (full-text search across entities), or should it be a standalone query within the `package` module?
- Should this use PostgreSQL full-text search (`tsvector`/`tsquery`), SQL `LIKE`/`ILIKE` patterns, or something else?
- Is a database migration required to add search indexes (e.g., GIN index on package name)?
- Should the search endpoint use the shared query builder helpers from `common/src/db/query.rs` for filtering and pagination?

### 4. Test Requirements Are Too Vague

The single test requirement "Test that search works correctly" does not provide enough detail:

- What specific scenarios should be tested (exact match, partial match, no results, special characters, empty query)?
- Should there be performance/load tests?
- What test data setup is needed?
- Should the tests follow the existing integration test pattern in `tests/api/` against a real PostgreSQL test database?

### 5. Service Layer Not Addressed

The task lists files to modify and create only in the `endpoints/` directory. It does not mention:

- Whether `PackageService` in `modules/fundamental/src/package/service/mod.rs` needs a new `search` method (analogous to `AdvisoryService` which already has `fetch, list, search`).
- Whether new model types are needed for search results.

---

## Questions for the Task Author

Before implementation can begin, please clarify the following:

1. **Search fields**: Which package fields should be searchable (name, namespace, version, license, description)?
2. **Search mechanism**: Should this use the existing `SearchService` from `modules/search/`, or implement search directly in the package service layer using SQL queries?
3. **API contract**: What is the exact endpoint path, accepted query parameters, and response format?
4. **Matching strategy**: Should search use exact matching, substring/ILIKE, or PostgreSQL full-text search?
5. **Pagination**: Should search results be paginated using `PaginatedResults<PackageSummary>` like other list endpoints?
6. **Performance target**: What is the acceptable response time, and for what data volume?
7. **Test scenarios**: What specific search scenarios and edge cases should be covered in tests?
8. **Service layer changes**: Does `PackageService` need a new `search` method, and if so, what is its signature?

---

## What I Would Do Once Clarified

Once the above questions are answered, I would proceed with:

1. **Create a feature branch** `TC-9202/add-package-search` from `main`.
2. **Add the service method** in `modules/fundamental/src/package/service/mod.rs` implementing the search logic per the clarified approach.
3. **Create the search endpoint** at `modules/fundamental/src/package/endpoints/search.rs` following the existing endpoint patterns (returning `Result<Json<PaginatedResults<PackageSummary>>, AppError>`).
4. **Register the route** in `modules/fundamental/src/package/endpoints/mod.rs`.
5. **Add a migration** if database indexes are needed for search performance.
6. **Write integration tests** in `tests/api/` covering the clarified test scenarios.
7. **Run the full test suite** to verify no regressions.
8. **Transition the Jira ticket** from "To Do" to "In Progress" and then to "In Review" upon completion.
