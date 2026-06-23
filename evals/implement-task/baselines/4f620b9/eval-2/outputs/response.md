# implement-task: TC-9202 — Add package search functionality

## Step 0 — Validate Project Configuration

I would read the project's CLAUDE.md (provided in `claude-md-mock.md`) and verify the required sections:

1. **Repository Registry** — Present. Contains `trustify-backend` with Serena instance `serena_backend` at path `./`.
2. **Jira Configuration** — Present. Contains Project key (TC), Cloud ID, Feature issue type ID, Git Pull Request custom field (`customfield_10875`), and GitHub Issue custom field (`customfield_10747`).
3. **Code Intelligence** — Present. Tool naming convention documented: `mcp__serena_backend__<tool>`. Configured with `rust-analyzer`.

All required sections are present. Proceeding.

## Step 0.5 — JIRA Access Initialization

I would attempt MCP first for all JIRA operations. If MCP fails, I would prompt the user with the three options (REST API fallback, skip, or retry) as specified in the skill.

## Step 1 — Fetch and Parse Jira Task

I would call `jira.get_issue(TC-9202)` and parse the structured description. Here is the parsing result from the provided task description:

| Section | Status | Content |
|---|---|---|
| Repository | Present | `trustify-backend` |
| Target Branch | Present | `main` |
| Description | **Incomplete** | "Add search capabilities to the package module so users can find packages more easily." — too vague, lacks specifics |
| Files to Modify | Present | `modules/fundamental/src/package/endpoints/mod.rs` — add search route |
| Files to Create | Present | `modules/fundamental/src/package/endpoints/search.rs` — search endpoint handler |
| API Changes | **Missing** | Not provided |
| Implementation Notes | **Missing** | Not provided |
| Acceptance Criteria | **Incomplete** | Vague and unmeasurable criteria |
| Test Requirements | **Incomplete** | Single vague requirement with no specific test scenarios |
| Target PR | Not present (optional — OK) |
| Review Context | Not present (optional — OK) |
| Bookend Type | Not present (optional — OK) |
| Dependencies | **Missing** | Not provided |

### GitHub Issue extraction

The GitHub Issue custom field is configured as `customfield_10747` in the Jira Configuration. I would check the fetched issue's fields for this custom field value. If present, I would extract the GitHub issue URL and parse it into the `<owner>/<repo>#<number>` format for use in the PR description.

### Gaps Identified — STOP EXECUTION

The task description does not follow the expected template and has critical gaps that prevent implementation. I would **stop execution immediately** and ask the user for clarification on the following:

---

**The task description for TC-9202 is incomplete. The following required sections are missing or insufficient. I cannot proceed with implementation until these gaps are addressed.**

**1. API Changes (missing entirely)**
- What HTTP method and path should the search endpoint use? (e.g., `GET /api/v2/package/search?q=...` or query parameters on the existing `GET /api/v2/package`?)
- What query parameters should the endpoint accept? (e.g., `q` for free-text search, filters by license, name pattern, purl type?)
- What should the response shape look like? (e.g., `PaginatedResults<PackageSummary>` matching the existing list endpoint pattern?)

**2. Implementation Notes (missing entirely)**
- Which existing patterns should this follow? The repository has a `modules/search/` module with a `SearchService` for full-text search — should the package search integrate with that service, or implement search logic directly in the package module's service layer?
- Should this use PostgreSQL full-text search (`tsvector`/`tsquery`), SQL `LIKE`/`ILIKE` patterns, or the existing `SearchService`?
- The `common/src/db/query.rs` provides shared query builder helpers for filtering, pagination, and sorting — should the search endpoint use these?
- Should the search support Package URL (purl) matching?

**3. Description (too vague)**
- "Add search capabilities" — search by what fields? Package name? Package URL? License? Version? All of these?
- What matching semantics? Exact match, prefix match, substring, full-text?
- Should results be sorted by relevance, or by a default field?

**4. Files to Modify / Files to Create (incomplete)**
- The task only lists endpoint files, but a search feature requires service layer changes. Should `modules/fundamental/src/package/service/mod.rs` (PackageService) be modified to add a search method?
- Does the `entity/src/package.rs` entity need modifications (e.g., adding a search index or tsvector column)?
- Is a database migration needed in `migration/` for full-text search indexes?
- Should `server/src/main.rs` be updated if route mounting changes?

**5. Acceptance Criteria (unmeasurable)**
- "Users can search for packages" — search by what? What constitutes a valid search query?
- "Search results are relevant" — what defines relevance? Exact name match ranks higher? purl match?
- "Performance is acceptable" — what is acceptable? Under 200ms? Under 1s? Is there a dataset size expectation?

**6. Test Requirements (insufficient)**
- "Test that search works correctly" — what specific scenarios should be tested?
  - Search by name with exact match?
  - Search by partial name / substring?
  - Search with no results?
  - Search with pagination?
  - Search with special characters or empty query?
  - Performance/load testing?

**7. Dependencies (missing)**
- Are there any prerequisite tasks that must be completed before this one? For example, does the `SearchService` in `modules/search/` need to be extended first?

---

**I have stopped execution and will not proceed with branching, implementation planning, or code changes until the user provides the missing information.**

## What I Would Do After Receiving Clarification

If the user provides the missing information, I would proceed with the following steps:

### Step 1.5 — Verify Description Integrity

I would fetch all comments on TC-9202 via `jira.get_issue_comments(TC-9202)` and search for a comment starting with `[sdlc-workflow] Description digest:`. If found, I would compute the current description's SHA-256 digest using `python3 scripts/sha256-digest.py` and compare it against the stored digest. If no digest comment is found, I would log a warning and proceed.

### Step 2 — Verify Dependencies

If dependencies are specified in the clarified description, I would fetch each dependency via `jira.get_issue(<dependency-id>)` and verify its status is Done.

### Step 3 — Transition to In Progress and Assign

1. Call `jira.user_info()` to get the current user's account ID.
2. Call `jira.edit_issue(TC-9202, assignee=<account-id>)` to assign the task.
3. Call `jira.transition_issue(TC-9202)` to transition to "In Progress".

### Step 4 — Understand the Code

Using the Serena instance `serena_backend` (tools called as `mcp__serena_backend__<tool>`):

1. **Overview of files to modify**: Call `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/package/endpoints/mod.rs` to understand the current route registration structure.

2. **Inspect sibling endpoint modules**: Call `mcp__serena_backend__get_symbols_overview` on:
   - `modules/fundamental/src/sbom/endpoints/mod.rs` — to see how SBOM routes are registered
   - `modules/fundamental/src/sbom/endpoints/list.rs` — to see the list endpoint pattern
   - `modules/fundamental/src/advisory/endpoints/mod.rs` — to see advisory route patterns

3. **Inspect the existing search module**: Call `mcp__serena_backend__get_symbols_overview` on:
   - `modules/search/src/service/mod.rs` — to understand the SearchService
   - `modules/search/src/endpoints/mod.rs` — to see the search endpoint pattern

4. **Inspect the package service**: Call `mcp__serena_backend__find_symbol` on `PackageService` in `modules/fundamental/src/package/service/mod.rs` with `include_body=true`.

5. **Inspect shared utilities**: Call `mcp__serena_backend__get_symbols_overview` on:
   - `common/src/db/query.rs` — query builder helpers
   - `common/src/model/paginated.rs` — PaginatedResults wrapper

6. **Check the package entity**: Call `mcp__serena_backend__get_symbols_overview` on `entity/src/package.rs`.

7. **Check for CONVENTIONS.md**: Look for `CONVENTIONS.md` at the repository root and read it if present. Extract CI check commands and code generation commands for use in Step 9.

8. **Convention conformance analysis**: Based on sibling analysis, I would document discovered conventions such as:
   - **Error handling:** All handlers use `Result<T, AppError>` with `.context()` wrapping
   - **Response types:** List endpoints return `PaginatedResults<T>`
   - **Query helpers:** Filtering, pagination, sorting via `common/src/db/query.rs`
   - **Route registration:** Each module's `endpoints/mod.rs` registers routes
   - **Naming:** Service methods likely follow `verb_noun` pattern

9. **Test convention analysis**: Inspect sibling test files:
   - `tests/api/sbom.rs` — SBOM endpoint integration tests
   - `tests/api/advisory.rs` — Advisory endpoint integration tests
   - `tests/api/search.rs` — Search endpoint integration tests
   Document assertion patterns (e.g., `assert_eq!(resp.status(), StatusCode::OK)`), response validation, error case coverage, and naming conventions.

10. **Documentation file identification**: Look for README files, API docs, and architecture docs in parent directories of modified files.

### Step 5 — Create Branch

```
git checkout main
git pull
git checkout -b TC-9202
```

### Step 6 — Implement Changes

Based on the clarified requirements, I would:

1. **Create `modules/fundamental/src/package/endpoints/search.rs`**: Implement the search endpoint handler following the patterns discovered in sibling endpoints (e.g., `list.rs` in sbom). The handler would accept query parameters, call the PackageService search method, and return `PaginatedResults<PackageSummary>`.

2. **Modify `modules/fundamental/src/package/endpoints/mod.rs`**: Register the new search route alongside the existing package routes.

3. **Modify `modules/fundamental/src/package/service/mod.rs`** (if approved): Add a search method to `PackageService` that queries packages using the specified search strategy.

4. **Follow code quality practices**: Add documentation comments to all new structs, types, and public functions.

5. **Verify cross-section reference consistency**: Ensure file paths in the task description are consistent.

### Step 7 — Write Tests

Create or update integration tests in `tests/api/` following the discovered test conventions:
- Use `assert_eq!(resp.status(), StatusCode::OK)` pattern
- Validate response shape (`total_count`, `items.len()`, key field values)
- Include error cases (404, empty search query)
- Add doc comments to every test function
- Use given-when-then structure for non-trivial tests

### Step 8 — Verify Acceptance Criteria

Go through each acceptance criterion (once clarified) and verify it is satisfied by the implementation and tests.

### Step 9 — Self-Verification

1. **Scope containment**: Run `git diff --name-only` and compare against Files to Modify and Files to Create.
2. **Untracked file check**: Run `git status --short` and check for untracked files in modified directories.
3. **Sensitive-pattern check**: Search staged diff for secrets/credentials.
4. **Documentation currency**: Check if API docs need updating for the new search endpoint.
5. **CI checks from CONVENTIONS.md**: Run any extracted CI commands.
6. **Data-flow trace**: Trace the search request from HTTP endpoint through service to database query and back to response.
7. **Contract & sibling parity**: Verify the search endpoint follows the same patterns as list/get endpoints.
8. **Duplication check**: Ensure no duplication with the existing `modules/search/` module.

### Step 10 — Commit and Push

```
git commit --trailer="Assisted-by: Claude Code" -m "feat(package): add package search endpoint

Add search functionality to the package module allowing users to search
packages by [criteria determined after clarification].

Implements TC-9202"

git push -u origin TC-9202

gh pr create --base main --title "feat(package): add package search endpoint" --body "## Summary
- Add search endpoint to the package module
- [Details based on clarified requirements]

Implements [TC-9202](https://redhat.atlassian.net/browse/TC-9202)
[Closes <owner>/<repo>#<number> if GitHub Issue was extracted]"
```

### Step 11 — Update Jira

1. **Update Git Pull Request custom field** (`customfield_10875`) with PR URL in ADF format:
   ```
   jira.update_issue(TC-9202, fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
   ```

2. **Add comment** to TC-9202 with PR link, summary of changes, and any deviations. The comment would end with the required footnote:
   ```
   ---
   This comment was AI-generated by [sdlc-workflow/implement-task](https://github.com/mrizzi/sdlc-plugins) v0.11.0.
   ```

3. **Transition** TC-9202 to "In Review":
   ```
   jira.transition_issue(TC-9202) → In Review
   ```
