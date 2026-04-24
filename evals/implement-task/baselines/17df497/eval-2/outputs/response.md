# implement-task: TC-9202 — Add package search functionality

## Step 0 — Validate Project Configuration

Reading the project's CLAUDE.md (from `claude-md-mock.md`), I verify the required sections under `# Project Configuration`:

1. **Repository Registry** — present, contains `trustify-backend` with Serena instance `serena_backend` at path `./`.
2. **Jira Configuration** — present, contains Project key (`TC`), Cloud ID, Feature issue type ID, Git Pull Request custom field (`customfield_10875`), and GitHub Issue custom field (`customfield_10747`).
3. **Code Intelligence** — present, with tool naming convention `mcp__<serena-instance>__<tool>` and configured instance `serena_backend` using `rust-analyzer`.

All required Project Configuration sections are present. Proceeding.

## Step 0.5 — JIRA Access Initialization

I would attempt to fetch the task via MCP first:

```
jira.get_issue("TC-9202")
```

If MCP fails, I would prompt the user with the REST API fallback options per the skill protocol.

**Note:** Per eval instructions, no actual Jira calls are made.

## Step 1 — Fetch and Parse Jira Task

Reading the task description from `task-incomplete.md`, I parse the structured sections:

| Section | Status | Content |
|---|---|---|
| **Repository** | Present | `trustify-backend` |
| **Description** | Present (vague) | "Add search capabilities to the package module so users can find packages more easily." |
| **Files to Modify** | Present | `modules/fundamental/src/package/endpoints/mod.rs` — add search route |
| **Files to Create** | Present | `modules/fundamental/src/package/endpoints/search.rs` — search endpoint handler |
| **API Changes** | **MISSING** | No endpoint specifications (path, method, request/response shapes) |
| **Implementation Notes** | **MISSING** | No code patterns, references to existing implementations, or reuse guidance |
| **Acceptance Criteria** | Present (insufficient) | Vague, non-measurable criteria |
| **Test Requirements** | Present (insufficient) | Single vague line with no specific test cases |
| **Dependencies** | **MISSING** | No dependency information |

### Gaps Identified

The task description is **incomplete** and does not follow the expected template. The following gaps prevent implementation:

#### 1. Missing: API Changes section
There is no specification for the search endpoint:
- What is the route path? (e.g., `GET /api/v2/package/search` or `GET /api/v2/package?q=...`)
- What query parameters does it accept? (e.g., `q`, `name`, `namespace`, `type`, `purl`, pagination params)
- What is the response shape? (e.g., `PaginatedResults<PackageSummary>` or a custom search result type)
- What HTTP method is used?

#### 2. Missing: Implementation Notes section
There is no guidance on:
- Which existing patterns to follow (e.g., how does the advisory module's search work in `advisory/service/advisory.rs`?)
- Whether to reuse the shared `SearchService` from `modules/search/` or implement module-local search
- Whether to use the shared query helpers from `common/src/db/query.rs` for filtering
- What database queries or SeaORM patterns to use for the search logic
- Whether to integrate with the existing `PackageService` or create a new service method

#### 3. Missing: Dependencies section
No information on whether this task depends on other tasks (e.g., does it require schema changes, a migration, or the search module to be extended first?).

#### 4. Vague Acceptance Criteria
The existing acceptance criteria are non-measurable:
- "Users can search for packages" — by what fields? Name? PURL? Namespace? License?
- "Search results are relevant" — what defines relevance? Exact match? Substring? Full-text?
- "Performance is acceptable" — what is the performance threshold? Response time? Result set limits?

#### 5. Vague Test Requirements
- "Test that search works correctly" — no specific test cases, no edge cases, no error scenarios defined.

### Execution Halted

Per the implement-task skill rules:

> "If any required section is missing or the description doesn't follow the template, list the gaps, ask the user for clarification, and **stop execution immediately** — do not proceed with any subsequent steps (branching, implementation planning, code changes) until the user provides the missing information."

**I am stopping execution and requesting clarification from the user.**

---

## Clarification Request

The task TC-9202 is missing critical information needed for implementation. Please provide the following before I can proceed:

1. **API Changes**: What is the exact endpoint specification?
   - Route path (e.g., `GET /api/v2/package/search?q={query}`)
   - Query parameters (search term, filters, pagination)
   - Response type and shape

2. **Implementation Notes**: What patterns should be followed?
   - Should this reuse the existing `SearchService` in `modules/search/`, or implement search within the `PackageService`?
   - Which existing endpoint should be used as a reference? (e.g., the advisory search in `modules/fundamental/src/advisory/service/advisory.rs`)
   - What search mechanism to use? (SQL `LIKE`/`ILIKE`, full-text search with `tsvector`, or delegation to the search module)

3. **Dependencies**: Are there any prerequisite tasks that must be completed first?

4. **Acceptance Criteria**: Please provide measurable criteria:
   - Which fields are searchable? (name, PURL, namespace, license, etc.)
   - What type of matching? (exact, substring, full-text)
   - Are there pagination requirements?
   - What is the expected performance target?

5. **Test Requirements**: Please specify concrete test cases:
   - Search by name returns matching packages
   - Search with no results returns empty paginated response
   - Search with special characters is handled safely
   - Pagination works correctly with search results
   - etc.

Once these gaps are filled, I will resume implementation from Step 2.
