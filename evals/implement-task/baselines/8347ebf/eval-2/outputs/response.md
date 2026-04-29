# implement-task TC-9202 -- Execution Halted: Incomplete Task Description

## Step 0 -- Validate Project Configuration

Project Configuration validated successfully:

- **Repository Registry**: present, contains `trustify-backend` with Serena instance `serena_backend`
- **Jira Configuration**: present, contains Project key (TC), Cloud ID, Feature issue type ID
- **Code Intelligence**: present, with tool naming convention and `serena_backend` instance configured

## Step 1 -- Fetch and Parse Jira Task

Parsing the structured description for TC-9202 ("Add package search functionality") against the required template sections:

| Section | Status | Details |
|---|---|---|
| Repository | Present | `trustify-backend` |
| Description | Present | "Add search capabilities to the package module so users can find packages more easily." |
| Files to Modify | Present | 1 file listed |
| Files to Create | Present | 1 file listed |
| API Changes | **MISSING** | No API Changes section. The task involves adding a search endpoint, but no endpoint path, HTTP method, request parameters, or response shape is specified. |
| Implementation Notes | **MISSING** | No Implementation Notes section. There is no guidance on which patterns to follow, which existing code to reference, or how the search should be implemented (e.g., SQL LIKE, full-text search via the existing `modules/search/` module, query builder filters). |
| Acceptance Criteria | **Present but vague** | The criteria lack specificity and are not verifiable as written (see details below). |
| Test Requirements | **Present but vague** | The requirements lack specificity and do not describe what scenarios to test (see details below). |
| Dependencies | Not present | Acceptable if there are no dependencies, but not explicitly stated. |

### Detailed Gaps

**1. Missing: API Changes section**

The task creates a new search endpoint but provides no API contract:
- What is the endpoint path? (e.g., `GET /api/v2/package/search` or a query parameter on `GET /api/v2/package`?)
- What query parameters does it accept? (e.g., `q`, `name`, `license`, `ecosystem`?)
- What is the response shape? (e.g., `PaginatedResults<PackageSummary>` following the existing list pattern?)
- Are there pagination, sorting, or filtering requirements?

**2. Missing: Implementation Notes section**

There is no guidance on how the search should be implemented:
- Should this use the existing `modules/search/` full-text search infrastructure (`SearchService`), or should it be a scoped search within the package module using query builder filters from `common/src/db/query.rs`?
- What fields should be searchable (package name, license, version, ecosystem)?
- Are there existing sibling search implementations (e.g., `AdvisoryService` has a `search` method in `modules/fundamental/src/advisory/service/advisory.rs`) that should serve as the pattern?
- Should the search endpoint be registered alongside the existing `GET /api/v2/package` route in `modules/fundamental/src/package/endpoints/mod.rs`, or as a separate sub-route?

**3. Vague Acceptance Criteria**

The current acceptance criteria are not objectively verifiable:
- "Users can search for packages" -- search by what? Name? License? Ecosystem? All fields?
- "Search results are relevant" -- what defines relevance? Exact match? Substring? Fuzzy? Ranked?
- "Performance is acceptable" -- what is the threshold? Under 200ms? Under 1s? Under what data volume?

Each criterion should be specific and testable, for example:
- "Users can search packages by name using a `q` query parameter on `GET /api/v2/package/search`"
- "Search returns packages whose name contains the search term (case-insensitive substring match)"
- "Search endpoint responds within 500ms for a database with 10,000 packages"

**4. Vague Test Requirements**

The current test requirement is:
- "Test that search works correctly" -- this does not specify what scenarios to cover.

Test requirements should describe specific cases, for example:
- "Test that searching by exact package name returns the matching package"
- "Test that searching with a partial name returns all matching packages"
- "Test that searching with no results returns an empty paginated response"
- "Test that the search endpoint returns 400 for missing query parameter"

## Decision: Stop Execution

Per the implement-task skill rules:

> "If any required section is missing or the description doesn't follow the template, list the gaps, ask the user for clarification, and stop execution immediately -- do not proceed with any subsequent steps (branching, implementation planning, code changes) until the user provides the missing information."

**Execution is halted.** The task description is missing required sections (API Changes, Implementation Notes) and contains vague, non-verifiable acceptance criteria and test requirements.

## Clarifying Questions

Before proceeding with implementation, please provide the following:

1. **API Changes**: What is the endpoint path, HTTP method, query parameters, and response shape for the package search?
2. **Implementation Notes**: Should this use the existing `SearchService` from `modules/search/`, or should it implement scoped search within the package module using `common/src/db/query.rs` query helpers? Which existing endpoint or service should serve as the pattern to follow?
3. **Searchable fields**: Which package fields should be searchable (name, license, ecosystem, version, description)?
4. **Search behavior**: What type of matching is expected (exact, substring, full-text, fuzzy)?
5. **Acceptance Criteria**: Please provide specific, measurable criteria. What does "relevant" mean? What does "acceptable performance" mean in concrete terms?
6. **Test Requirements**: Please provide specific test scenarios covering success cases, edge cases (empty results, missing parameters), and error cases.
