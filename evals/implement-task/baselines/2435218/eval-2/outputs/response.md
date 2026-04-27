# implement-task TC-9202 -- Execution Halted: Incomplete Task Description

## Step 0 -- Validate Project Configuration

Verified the project's CLAUDE.md contains:

1. **Repository Registry** -- present, lists `trustify-backend` with Serena instance `serena_backend`
2. **Jira Configuration** -- present, includes Project key (`TC`), Cloud ID, Feature issue type ID
3. **Code Intelligence** -- present, with tool naming convention `mcp__<serena-instance>__<tool>` and configured instance `serena_backend`

Project configuration is valid. Proceeding to Step 1.

## Step 1 -- Fetch and Parse Jira Task

Fetched TC-9202. Parsing the structured description against the required template sections:

| Section | Status | Detail |
|---|---|---|
| Repository | present | `trustify-backend` |
| Description | present (vague) | "Add search capabilities to the package module so users can find packages more easily." -- lacks specifics on search behavior |
| Files to Modify | present | 1 file listed |
| Files to Create | present | 1 file listed |
| API Changes | **MISSING** | No API Changes section. The task implies a new endpoint but does not specify the HTTP method, path, query parameters, request/response shapes, or pagination behavior. |
| Implementation Notes | **MISSING** | No Implementation Notes section. There are no references to existing code patterns, reusable utilities, or architectural guidance for how to implement the search. |
| Acceptance Criteria | present (vague) | All three criteria are subjective and unmeasurable -- see details below. |
| Test Requirements | present (vague) | Single item "Test that search works correctly" provides no actionable test specification -- see details below. |
| Dependencies | not present | No dependencies listed (acceptable -- task may have none). |

### Identified Gaps

#### 1. Missing: API Changes section

The task says to "add search route" and create a "search endpoint handler" but does not specify:

- What is the endpoint path? (e.g., `GET /api/v2/package/search` vs. `GET /api/v2/package?q=...` vs. something else)
- What HTTP method is used?
- What query parameters does the search accept? (e.g., `q`, `filter`, `sort`, `page`, `limit`)
- What is the response shape? Does it return `PaginatedResults<PackageSummary>`, or a different structure with relevance scores?

#### 2. Missing: Implementation Notes section

There is no guidance on:

- **Which fields to search**: Should the search match against package name only? Name and description? License? Version? PURL? Some combination?
- **Search mechanism**: Should this use the existing `SearchService` in `modules/search/`? Should it use PostgreSQL full-text search (`tsvector`/`tsquery`)? SQL `ILIKE`? Should it integrate with the existing `common/src/db/query.rs` query builder filtering, or implement a separate search path?
- **Existing patterns to follow**: The repository already has a `modules/search/` module with a `SearchService` for full-text search across entities and a `GET /api/v2/search` endpoint. Should the package search reuse this service, extend it, or implement a separate module-local search? No guidance is provided.
- **Code references**: No references to sibling implementations (e.g., the `advisory` module's `AdvisoryService` which already has a `search` method in `modules/fundamental/src/advisory/service/advisory.rs`).

#### 3. Vague Acceptance Criteria

The three acceptance criteria are not actionable:

- **"Users can search for packages"** -- By what mechanism? What inputs are accepted? What constitutes a successful search?
- **"Search results are relevant"** -- What does "relevant" mean? Is there a ranking algorithm expected? Should exact matches rank higher than partial matches? Is fuzzy matching required? What is the expected behavior for zero results?
- **"Performance is acceptable"** -- What is the performance threshold? Is there a maximum response time target (e.g., < 200ms for 95th percentile)? A maximum result set size? Does the search need an index? What is the expected data volume?

#### 4. Vague Test Requirements

The single test requirement "Test that search works correctly" does not specify:

- What search scenarios to test (exact match, partial match, no results, special characters, empty query)
- Whether to test pagination of search results
- Whether to test performance/load characteristics
- Whether to test edge cases (very long queries, SQL injection prevention, Unicode handling)
- What assertions define "correctly" (status codes, response shape, result ordering, result count)

---

## Execution Stopped

Per the implement-task skill rules: "If any required section is missing or the description doesn't follow the template, list the gaps, ask the user for clarification, and stop execution immediately."

The task description is missing the **API Changes** and **Implementation Notes** sections entirely, and the **Acceptance Criteria** and **Test Requirements** sections are too vague to implement against. I will not proceed with branching, implementation planning, code changes, or any subsequent steps until the following questions are answered.

## Clarifying Questions

Please provide answers to the following before I can proceed:

### Search Behavior

1. **Which fields should be searchable?** Should the search match against package name only, or also against description, license, version, PURL, or other fields on `PackageSummary`?
2. **What search mechanism should be used?** Options include:
   - Reusing the existing `SearchService` in `modules/search/` (full-text search across entities)
   - Extending `PackageService` with a SQL-level search (e.g., PostgreSQL `ILIKE` or `tsvector`/`tsquery`)
   - Adding a filter parameter to the existing `GET /api/v2/package` list endpoint via `common/src/db/query.rs`
3. **What does "relevant" mean for ranking?** Should results be ranked by relevance score (e.g., full-text search rank), or is alphabetical/default ordering sufficient? Should exact matches appear before partial matches?

### API Design

4. **What is the endpoint path and method?** For example: `GET /api/v2/package/search?q=<term>`, or should search be a query parameter on the existing list endpoint `GET /api/v2/package?q=<term>`?
5. **What query parameters are supported?** At minimum: the search term parameter name, plus pagination (`offset`/`limit`), sorting, and any filters.
6. **What is the response shape?** Should it return `PaginatedResults<PackageSummary>` (consistent with other list endpoints), or a custom shape with relevance scores?

### Performance

7. **What performance threshold is "acceptable"?** Is there a target response time (e.g., < 200ms at p95)? What is the expected data volume (number of packages in the database)?
8. **Is a database index required?** If full-text search is used, should a GIN index or similar be created via a migration?

### Testing

9. **What search scenarios should be tested?** For example: exact name match, partial match, case-insensitive match, no results, empty query, special characters.
10. **Should integration tests hit the database?** The existing test suite in `tests/api/` uses a real PostgreSQL test database -- should the search tests follow the same pattern?
11. **What assertions define correctness?** For example: status code 200, response contains matching packages, response is paginated, specific fields are present in results.

Once these questions are answered, I will resume execution from Step 2.
