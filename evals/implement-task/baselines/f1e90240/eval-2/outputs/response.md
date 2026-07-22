# implement-task: TC-9202 — Validation Failed

## Step 0 — Validate Project Configuration

The project's CLAUDE.md contains all required sections:

1. **Repository Registry** — present with `trustify-backend` entry
2. **Jira Configuration** — present with Project key (TC), Cloud ID, and Feature issue type ID
3. **Code Intelligence** — present with `serena_backend` instance and tool naming convention

Project configuration is valid. Proceeding to Step 1.

## Step 1 — Fetch and Parse Jira Task

Parsing the task description for TC-9202 reveals the following sections:

| Section | Status | Content |
|---|---|---|
| Repository | Present | trustify-backend |
| Target Branch | Present | main |
| Description | Present but vague | "Add search capabilities to the package module so users can find packages more easily." |
| Files to Modify | Present but likely incomplete | 1 file listed |
| Files to Create | Present but likely incomplete | 1 file listed |
| API Changes | **MISSING** | — |
| Implementation Notes | **MISSING** | — |
| Acceptance Criteria | Present but vague | 3 items, all non-verifiable |
| Test Requirements | Present but vague | 1 item, not actionable |
| Dependencies | Not present | — |

### Gaps Identified

**Execution is stopped.** The task description is missing required sections and contains vague content that is insufficient for implementation. The specific gaps are listed below.

---

### 1. API Changes section is missing (required)

There is no API Changes section at all. Without it, the following are unknown:

- What is the endpoint path? (e.g., `GET /api/v2/package/search` vs. `GET /api/v2/package?q=...` as a query parameter on the existing list endpoint)
- What HTTP method does it use?
- What query parameters or request body does it accept? (e.g., `q`, `field`, `limit`, `offset`)
- What is the response shape? (e.g., does it return `PaginatedResults<PackageSummary>` like the existing list endpoint, or a different search-specific result type?)
- What status codes should it return for empty results, invalid queries, etc.?

### 2. Implementation Notes section is missing (required)

There is no Implementation Notes section. This section is critical because it provides the patterns and code references that guide implementation. Without it, the following decisions are ambiguous:

- **Search mechanism**: Should this use the existing `SearchService` in `modules/search/` (full-text search across entities), or build a package-specific search using SQL `LIKE`/`ILIKE` queries via the `common/src/db/query.rs` query builder helpers?
- **Service layer pattern**: The existing `PackageService` in `modules/fundamental/src/package/service/mod.rs` has `fetch` and `list` methods. Should a `search` method be added there, or should a separate search service be created?
- **Query builder usage**: The repo has shared query builder helpers in `common/src/db/query.rs` for filtering, pagination, and sorting. Should the search endpoint reuse these helpers (similar to how the advisory module's `AdvisoryService` implements search)?
- **Route registration**: How should the new search route be registered in `endpoints/mod.rs`? Should it follow the same pattern as `list.rs` (separate handler file with route registration in `mod.rs`)?
- **Integration with existing search module**: The repository already has a `modules/search/` module with a `SearchService` providing "full-text search across entities." The relationship between this existing module and the new package-specific search is not specified.

### 3. Description is vague and underspecified

The description states only: "Add search capabilities to the package module so users can find packages more easily." This does not specify:

- **Searchable fields**: Which fields of a package should be searchable? The `PackageSummary` struct includes at least a `license` field (per the repo structure). Are users searching by package name, version, PURL, license, or some combination?
- **Search type**: Is this a substring match, prefix match, full-text search with ranking, or exact match with filters?
- **Result ordering**: How should search results be sorted? By relevance score, alphabetically, by creation date?
- **Pagination**: Should search results be paginated using the existing `PaginatedResults<T>` wrapper from `common/src/model/paginated.rs`?

### 4. Acceptance Criteria are non-verifiable

The three acceptance criteria are too vague to verify programmatically or even manually:

- "Users can search for packages" — By what mechanism? Through what API? With what parameters? This criterion cannot be verified without knowing the API contract.
- "Search results are relevant" — What defines relevance? Is there a ranking algorithm? What constitutes a relevant vs. irrelevant result? Without a definition, this criterion is subjective and unverifiable.
- "Performance is acceptable" — What is the performance target? Is there a maximum response time (e.g., < 200ms for 95th percentile)? A maximum result set size? Without a threshold, this criterion is unmeasurable.

### 5. Test Requirements are not actionable

The single test requirement — "Test that search works correctly" — provides no guidance on:

- What test scenarios to cover (e.g., search with results, search with no results, search with special characters, search with pagination)
- What assertions to make (e.g., expected status codes, expected result counts, expected field values)
- Whether to add integration tests in `tests/api/` (following the pattern of `sbom.rs`, `advisory.rs`, and `search.rs`) or unit tests within the module
- Whether to test edge cases (e.g., empty search query, very long query, SQL injection attempts)

### 6. Files to Modify is likely incomplete

Only `modules/fundamental/src/package/endpoints/mod.rs` is listed for modification. Based on the repository's module pattern (`model/ + service/ + endpoints/`), the following files likely also need modification or creation but are not listed:

- `modules/fundamental/src/package/service/mod.rs` — the `PackageService` would need a new `search` method
- `server/src/main.rs` — if the search route requires separate mounting (depends on how routes are organized)
- Potentially a new model file if a search-specific request or response type is needed

---

## Clarifying Questions

Before proceeding with implementation, I need answers to the following:

1. **API design**: What should the search endpoint look like? Specifically:
   - What is the endpoint path and HTTP method?
   - What query parameters does it accept (search term, filters, pagination)?
   - What is the response shape (reuse `PaginatedResults<PackageSummary>` or a new type)?

2. **Search mechanism**: Should this use the existing `SearchService` from `modules/search/` for full-text search, or implement package-specific search using SQL queries via the shared query builder in `common/src/db/query.rs`?

3. **Searchable fields**: Which package fields should be searchable (name, version, PURL, license, or all)?

4. **Service layer changes**: Should a `search` method be added to the existing `PackageService` in `service/mod.rs`? If so, that file should be listed in Files to Modify.

5. **Acceptance criteria thresholds**: What defines "relevant" results and "acceptable" performance? Are there specific latency targets or relevance ranking requirements?

6. **Test scenarios**: What specific scenarios should tests cover? At minimum, should there be tests for: successful search with results, search with no matches, search with pagination, and search with invalid input?

Please provide the missing sections (API Changes, Implementation Notes) and clarify the vague sections (Description, Acceptance Criteria, Test Requirements) so I can proceed with implementation.
