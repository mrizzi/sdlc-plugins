# implement-task TC-9202 — Execution Stopped: Incomplete Task Description

## Step 0 — Validate Project Configuration

Verified the project's CLAUDE.md contains all required sections under `# Project Configuration`:

1. **Repository Registry** — present, contains `trustify-backend` with Serena instance `serena_backend` at path `./`
2. **Jira Configuration** — present, contains Project key (`TC`), Cloud ID, Feature issue type ID, Git Pull Request custom field (`customfield_10875`), and GitHub Issue custom field (`customfield_10747`)
3. **Code Intelligence** — present, with tool naming convention `mcp__<serena-instance>__<tool>` and configured instance `serena_backend` using `rust-analyzer`

Project Configuration is valid. Proceeding to Step 1.

## Step 1 — Fetch and Parse Jira Task

Fetched TC-9202. Parsing the structured description against the required template sections:

| Section | Status | Notes |
|---|---|---|
| Repository | Present | `trustify-backend` |
| Target Branch | Present | `main` |
| Description | Present but vague | "Add search capabilities to the package module so users can find packages more easily." — no specifics on search behavior, query parameters, matching strategy, or scope |
| Files to Modify | Present | `modules/fundamental/src/package/endpoints/mod.rs` — add search route |
| Files to Create | Present | `modules/fundamental/src/package/endpoints/search.rs` — search endpoint handler |
| **API Changes** | **MISSING** | No endpoint definition — missing HTTP method, URL path, query parameters, request/response shapes |
| **Implementation Notes** | **MISSING** | No code patterns, references to existing implementations, or architectural guidance on how to implement search (e.g., whether to use the existing `SearchService` in `modules/search/`, database queries, full-text search, or filtering) |
| Acceptance Criteria | Present but vague | Criteria are not measurable: "Users can search for packages" (how?), "Search results are relevant" (by what measure?), "Performance is acceptable" (what threshold?) |
| Test Requirements | Present but vague | "Test that search works correctly" — no specific test scenarios, edge cases, or expected behaviors |
| Target PR | Not present | (optional — OK) |
| Bookend Type | Not present | (optional — OK) |
| Dependencies | Not present | (optional — OK) |

## Gaps Identified

The task description is **incomplete** and does not follow the structured template. The following required sections are missing or insufficient:

1. **API Changes (MISSING):** The task asks to "add search functionality" but provides no API specification. I need to know:
   - What is the endpoint path? (e.g., `GET /api/v2/package/search` or a query parameter on the existing list endpoint?)
   - What query parameters does it accept? (e.g., `q`, `name`, `namespace`, `type`, `purl`?)
   - What is the response shape? (e.g., `PaginatedResults<PackageSummary>` matching the existing list endpoint?)
   - Are there any filtering, pagination, or sorting requirements?

2. **Implementation Notes (MISSING):** There is no guidance on the implementation approach. Key questions:
   - Should this use the existing `SearchService` in `modules/search/` for full-text search, or implement database-level query filtering in `PackageService`?
   - What patterns should be followed? The `advisory` module has a `search` capability in its service (`AdvisoryService: fetch, list, search`) — should the package search follow the same pattern?
   - Should the search be added as a new method on `PackageService` (in `modules/fundamental/src/package/service/mod.rs`), and if so, is that file also in scope for modification?
   - Should `common/src/db/query.rs` shared query helpers be used for filtering?
   - What fields on `PackageSummary` are searchable?

3. **Acceptance Criteria (VAGUE):** The current criteria are not verifiable. They need to specify:
   - What search inputs produce what results (e.g., "searching by partial package name returns matching packages")
   - What "relevant" means in concrete terms (e.g., "exact name matches rank higher than partial matches")
   - What "acceptable performance" means (e.g., "search responds within 500ms for datasets under 10k packages")

4. **Test Requirements (VAGUE):** "Test that search works correctly" needs to specify:
   - Specific test scenarios (e.g., search with matching results, search with no results, search with special characters, pagination of search results)
   - Whether integration tests should be added to `tests/api/` (following the existing pattern in `tests/api/search.rs`)
   - Expected response status codes and body structure for each scenario

## Execution Stopped

Per the skill rules: "If any required section is missing or the description doesn't follow the template, list the gaps, ask the user for clarification, and **stop execution immediately** — do not proceed with any subsequent steps (branching, implementation planning, code changes) until the user provides the missing information."

**I am stopping execution and will not proceed with any subsequent steps (Steps 2-11) until the missing information is provided.**

Please update the task description for TC-9202 with the missing sections (API Changes, Implementation Notes) and clarify the vague sections (Acceptance Criteria, Test Requirements), then re-run `/implement-task TC-9202`.
