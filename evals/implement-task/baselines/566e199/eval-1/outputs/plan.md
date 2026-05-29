# Implementation Plan for TC-9201

## Step 0 -- Validate Project Configuration

Read the project's CLAUDE.md (claude-md-mock.md) and verify the required sections:

1. **Repository Registry** -- PRESENT. Contains one entry: `trustify-backend` with Role `Rust backend service`, Serena Instance `serena_backend`, Path `./`.
2. **Jira Configuration** -- PRESENT. Contains: Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432`, Feature issue type ID `10142`, Git Pull Request custom field `customfield_10875`, GitHub Issue custom field `customfield_10747`.
3. **Code Intelligence** -- PRESENT. Tool naming convention documented (`mcp__<serena-instance>__<tool>`), one configured instance: `serena_backend` for `trustify-backend` with `rust-analyzer`.

**Result**: All three sections are present and complete. Proceed.

## Step 0.5 -- JIRA Access Initialization

Would attempt MCP first for all Jira operations. If MCP fails, prompt the user with the three options (REST API fallback, skip, retry). For this task, the Jira operations needed are:
- `jira.get_issue(TC-9201)` (Step 1)
- `jira.get_issue_comments(TC-9201)` (Step 1.5)
- `jira.user_info()` (Step 3)
- `jira.edit_issue(TC-9201, assignee=...)` (Step 3)
- `jira.transition_issue(TC-9201, "In Progress")` (Step 3)
- `jira.update_issue(TC-9201, fields={customfield_10875: ...})` (Step 11)
- `jira.add_comment(TC-9201, ...)` (Step 11)
- `jira.transition_issue(TC-9201, "In Review")` (Step 11)

## Step 1 -- Fetch and Parse Jira Task

Fetch `TC-9201` via `jira.get_issue(TC-9201)`. Parse the structured description:

- **Repository**: `trustify-backend`
- **Target Branch**: `main`
- **Description**: Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. Returns summary with counts per severity level (Critical, High, Medium, Low) and a total.
- **Files to Modify**:
  - `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method to AdvisoryService
  - `modules/fundamental/src/advisory/endpoints/mod.rs` -- register the new route
  - `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;` to register the new model module
  - `server/src/main.rs` -- no changes needed (routes auto-mount)
- **Files to Create**:
  - `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler
  - `tests/api/advisory_summary.rs` -- integration tests
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` -- NEW
- **Implementation Notes**: Follow existing endpoint pattern in `get.rs`, add method to `AdvisoryService` following `fetch`/`list` pattern, use `sbom_advisory` join table, use `AdvisorySummary.severity` field, register route in `endpoints/mod.rs`, return `AppError` with `.context()`, return struct directly via `Json`.
- **Acceptance Criteria**: 5 criteria covering correct response shape, 404 handling, deduplication, zero defaults, and performance.
- **Test Requirements**: 4 test cases covering valid counts, 404, empty SBOM, and deduplication.
- **Target PR**: Not present (default flow -- new branch and PR)
- **Bookend Type**: Not present (standard implementation)
- **Review Context**: Not present
- **Dependencies**: None

**webUrl**: Would capture from API response, e.g., `https://redhat.atlassian.net/browse/TC-9201`

### Target Branch extraction
Extracted: `main`. This will be used as `--base main` for the PR in Step 10.

### GitHub Issue extraction
The Jira Configuration specifies `GitHub Issue custom field: customfield_10747`. Would read this field from the fetched issue. If present, parse the GitHub issue URL to extract `owner/repo#number` for inclusion in the PR description as `Closes owner/repo#number`. If empty, skip silently.

## Step 1.5 -- Verify Description Integrity

1. Fetch all comments on TC-9201 via `jira.get_issue_comments(TC-9201)`.
2. Search for comments whose body starts with `[sdlc-workflow] Description digest:`.
3. **If no digest comment found**: Log warning and proceed:
   > "No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced."
4. **If digest comment found**:
   a. Check `created` vs `updated` timestamps. If `updated` is later than `created`, warn: "Digest comment was edited after initial posting -- integrity cannot be fully guaranteed."
   b. Extract `sha256:<hex-digest>` from the comment body.
   c. Compute SHA-256 of the current description field text using `python3 scripts/sha256-digest.py` with the description content (ADF JSON normalized with compact separators).
   d. Compare digests:
      - **Match**: Proceed silently.
      - **Mismatch**: Alert user with expected vs actual digest, ask whether to proceed or stop.

Since this is a synthetic test task, no digest comment exists. We would log the backward-compatibility warning and proceed.

## Step 2 -- Verify Dependencies

The task specifies `Dependencies: None`. No dependency checks needed. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's Jira account ID via `jira.user_info()`.
2. Assign TC-9201 to the current user: `jira.edit_issue(TC-9201, assignee=<account-id>)`.
3. Transition TC-9201 to In Progress: `jira.transition_issue(TC-9201, "In Progress")`.

## Step 4 -- Understand the Code

### Repository and Serena Instance
From Repository Registry: `trustify-backend` uses Serena instance `serena_backend`. Tools called as `mcp__serena_backend__<tool>`.

### Inspect files to modify

1. **`modules/fundamental/src/advisory/service/advisory.rs`**:
   - `mcp__serena_backend__get_symbols_overview` to see the structure of `AdvisoryService` (methods: `fetch`, `list`, `search`).
   - `mcp__serena_backend__find_symbol("severity_summary", include_body=false)` to confirm it does not exist yet.
   - `mcp__serena_backend__find_symbol("fetch", include_body=true)` to read the `fetch` method pattern (parameter types, return type, error handling).

2. **`modules/fundamental/src/advisory/endpoints/mod.rs`**:
   - `mcp__serena_backend__get_symbols_overview` to see route registration pattern.
   - Examine how existing routes like `get.rs` and `list.rs` are imported and mounted.

3. **`modules/fundamental/src/advisory/model/mod.rs`**:
   - `mcp__serena_backend__get_symbols_overview` to see existing `pub mod` declarations (e.g., `pub mod summary;`, `pub mod details;`).

4. **`entity/src/sbom_advisory.rs`**:
   - `mcp__serena_backend__get_symbols_overview` to understand the join table entity structure (columns, relations).

5. **`modules/fundamental/src/advisory/model/summary.rs`**:
   - `mcp__serena_backend__find_symbol("AdvisorySummary", include_body=true)` to see the `severity` field and its type.

6. **`common/src/error.rs`**:
   - `mcp__serena_backend__find_symbol("AppError", include_body=true)` to understand the error type and `.context()` wrapping pattern.

### Backward compatibility check
- `mcp__serena_backend__find_referencing_symbols("AdvisoryService")` to identify all callers of the service -- ensure the new method does not break existing usage.

### Convention conformance analysis (sibling files)

For production code, analyze sibling files in the same directories:

**Endpoint siblings** (`modules/fundamental/src/advisory/endpoints/`):
- Read `get.rs` and `list.rs` via `mcp__serena_backend__get_symbols_overview` to discover:
  - Handler function signatures
  - Path parameter extraction pattern
  - Service call pattern
  - Return type pattern
  - Error handling approach

**Service siblings** (`modules/fundamental/src/advisory/service/`):
- Read `advisory.rs` methods `fetch` and `list` to discover:
  - Method signatures (`&self, id: Id, tx: &Transactional<'_>`)
  - Query patterns (SeaORM entity operations)
  - Error wrapping style (`.context("...")`)
  - Return types

**Model siblings** (`modules/fundamental/src/advisory/model/`):
- Read `summary.rs` and `details.rs` to discover:
  - Struct derive macros (`#[derive(Serialize, Deserialize, Debug, Clone)]`)
  - Field documentation style
  - Any trait implementations

**Cross-module siblings** for additional patterns:
- `modules/fundamental/src/sbom/endpoints/get.rs` -- verify consistent endpoint patterns across modules
- `modules/fundamental/src/sbom/service/sbom.rs` -- verify service method pattern consistency

### Test convention analysis

**Test siblings** (`tests/api/`):
- Read `advisory.rs` and `sbom.rs` via `mcp__serena_backend__get_symbols_overview`:
  - Assertion style: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
  - Response validation: check fields, status codes
  - Error cases: 404 tests with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
  - Test naming: `test_<endpoint>_<scenario>` pattern
  - Test setup: database seeding, test server creation
  - Parameterized tests: check if `#[rstest]` is used in sibling tests

### Documentation file identification

- `README.md` at repository root
- `docs/architecture.md` -- system architecture
- `docs/api.md` -- REST API reference (likely needs updating for new endpoint)
- `CONVENTIONS.md` at repository root -- explicit project conventions

### CONVENTIONS.md lookup

Repository root is `./` per Repository Registry. Check for `CONVENTIONS.md` -- it exists per the repo structure. Read it to extract:
- Naming rules
- Directory structure conventions
- Code patterns
- Test conventions
- CI check commands (verification commands extraction)
- Code generation commands

Record any CI check commands for use in Step 9.

## Step 5 -- Create Branch

Default flow (no Target PR, no Bookend Type):

```
git checkout main
git pull
git checkout -b TC-9201
```

Branch named `TC-9201` after the Jira issue ID, checked out from `main` (the Target Branch).

## Step 6 -- Implement Changes

### Files to Create

1. **`modules/fundamental/src/advisory/model/severity_summary.rs`** -- SeveritySummary response struct
2. **`modules/fundamental/src/advisory/endpoints/severity_summary.rs`** -- GET handler
3. **`tests/api/advisory_summary.rs`** -- Integration tests (covered in Step 7)

### Files to Modify

1. **`modules/fundamental/src/advisory/service/advisory.rs`** -- add `severity_summary` method
2. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- register new route
3. **`modules/fundamental/src/advisory/model/mod.rs`** -- add `pub mod severity_summary;`

Detailed changes are described in the file-N-description.md outputs.

### Cross-repo API contract verification
Not applicable -- this task creates a new backend endpoint; it does not make manual REST calls to another service.

### Code quality practices
- Every new struct, function, and method will have a `///` documentation comment.
- Public functions will document parameters and return values where the name alone does not convey intent.

### Documentation impact
- `docs/api.md` likely needs updating with the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint documentation.
- No Documentation Updates section in the task, so check `docs/api.md` and update if it documents REST endpoints.

## Step 7 -- Write Tests

Implement tests in `tests/api/advisory_summary.rs` as described in file-5-description.md.

All test functions will have `///` documentation comments. Non-trivial tests will include `// Given`, `// When`, `// Then` section comments.

Run `cargo test` to verify all tests pass. Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

1. `GET /api/v2/sbom/{id}/advisory-summary` returns `{ critical: N, high: N, medium: N, low: N, total: N }` -- Verified by SeveritySummary struct shape and endpoint implementation.
2. Returns 404 when SBOM ID does not exist -- Verified by service method returning `AppError::NotFound` and test coverage.
3. Counts only unique advisories (deduplicates by advisory ID) -- Verified by using `DISTINCT` or `group_by` in the query and test coverage.
4. All severity levels default to 0 when no advisories exist -- Verified by SeveritySummary `Default` implementation and test coverage.
5. Response time under 200ms for SBOMs with up to 500 advisories -- Verified by efficient SQL query (single aggregation query, no N+1).

## Step 9 -- Self-Verification

### Scope containment
Run `git diff --name-only` and compare against Files to Modify and Files to Create. Expected modified/created files:
- `modules/fundamental/src/advisory/model/severity_summary.rs` (create)
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (create)
- `tests/api/advisory_summary.rs` (create)
- `modules/fundamental/src/advisory/service/advisory.rs` (modify)
- `modules/fundamental/src/advisory/endpoints/mod.rs` (modify)
- `modules/fundamental/src/advisory/model/mod.rs` (modify)

If `docs/api.md` was also modified (documentation impact), flag it as out-of-scope and explain the documentation update reason. Ask user to approve.

If `server/src/main.rs` appears in the diff, flag as unexpected (task says "no changes needed").

### Untracked file check
Run `git status --short`, extract `??` entries. Filter by proximity to implementation directories. Search for code references to any untracked files (e.g., `include_str!` references). Flag any referenced untracked files for staging approval.

### Sensitive-pattern check
Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'`. Flag any matches.

### Documentation currency
If `docs/api.md` describes existing endpoints and the new endpoint was not documented in Step 6, update it now.

### Documentation scope preservation
If `docs/api.md` was modified, verify that replacement text still covers all use cases from the original text. Flag any scope narrowing.

### Eval coverage currency
Check if any `skills/<skill-name>/SKILL.md` was modified. Not applicable for this task (we are modifying application code, not skill definitions).

### Example consistency
If any documentation with composite examples was written, cross-check data structures against narrative. Not expected for this task.

### Cross-section reference consistency
Verify that entity-to-file-path mappings are consistent across Files to Modify, Files to Create, and Implementation Notes:
- `AdvisoryService` -> `modules/fundamental/src/advisory/service/advisory.rs` -- consistent across sections.
- `SeveritySummary` -> `modules/fundamental/src/advisory/model/severity_summary.rs` -- consistent.
- Route registration -> `modules/fundamental/src/advisory/endpoints/mod.rs` -- consistent.

### Duplication check
Search for existing severity aggregation logic in the repository using Grep/Serena. Verify no existing utility computes severity counts. If found, refactor to reuse.

### CI checks from CONVENTIONS.md
Run all CI check commands extracted from `CONVENTIONS.md` in Step 4. If any fail, stop and fix before proceeding. Hard stop on any non-zero exit.

### Data-flow trace
- `GET /api/v2/sbom/{id}/advisory-summary`:
  - Input: HTTP request with SBOM ID path parameter -> extract via `Path<Id>` -- COMPLETE
  - Processing: Call `AdvisoryService::severity_summary(sbom_id, tx)` -> query `sbom_advisory` join table -> aggregate by severity -> build `SeveritySummary` -- COMPLETE
  - Output: Return `Json<SeveritySummary>` with status 200 -- COMPLETE
  - Error path: SBOM not found -> `AppError::NotFound` -> 404 response -- COMPLETE
  - **Result: COMPLETE** -- all stages connected.

### Contract & sibling parity
- **Contract verification**: `SeveritySummary` derives `Serialize` (required for `Json` response). Handler returns `Result<Json<SeveritySummary>, AppError>` matching Axum's `IntoResponse` contract.
- **Sibling parity**: Compare with `get.rs` and `list.rs` handlers:
  - Error handling: All use `Result<T, AppError>` with `.context()` -- matched.
  - Logging: Check if siblings log on success/error -- match pattern.
  - Configuration: Check if siblings accept query parameters -- the new endpoint is a simple GET with path param only, consistent with `get.rs`.
- **Cross-module shared entity analysis**: The new code reads from `sbom_advisory` join table. Search for other modules that interact with this entity (e.g., `ingestor/graph/advisory/mod.rs` writes to it). Verify read patterns are consistent (transaction handling, etc.).
- **Caller-site parity**: Not applicable -- this creates a new endpoint, not a call to a shared abstraction.

## Step 10 -- Commit and Push

### Commit message (Conventional Commits format)

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
aggregated severity counts (critical, high, medium, low, total) for
advisories linked to a given SBOM. Includes SeveritySummary model,
AdvisoryService method, and integration tests.

Implements TC-9201
```

Commit command:
```
git add modules/fundamental/src/advisory/model/severity_summary.rs \
      modules/fundamental/src/advisory/endpoints/severity_summary.rs \
      tests/api/advisory_summary.rs \
      modules/fundamental/src/advisory/service/advisory.rs \
      modules/fundamental/src/advisory/endpoints/mod.rs \
      modules/fundamental/src/advisory/model/mod.rs
git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
aggregated severity counts (critical, high, medium, low, total) for
advisories linked to a given SBOM. Includes SeveritySummary model,
AdvisoryService method, and integration tests.

Implements TC-9201"
```

### Push and create PR

```
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint for SBOM advisories" --body "## Summary

Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint that returns aggregated
severity counts for advisories linked to a given SBOM. The response includes
counts per severity level (critical, high, medium, low) and a total, enabling
dashboard widgets to render severity breakdowns without client-side counting.

### Changes
- New `SeveritySummary` response struct in `advisory/model/severity_summary.rs`
- New `severity_summary` method on `AdvisoryService` using `sbom_advisory` join table
- New GET handler in `advisory/endpoints/severity_summary.rs`
- Route registered in `advisory/endpoints/mod.rs`
- Integration tests covering valid counts, 404, empty SBOM, and deduplication

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)
Closes <owner>/<repo>#<number> (if GitHub Issue custom field was populated)"
```

The `--base main` is explicitly specified to target the correct branch.

## Step 11 -- Update Jira

1. **Git Pull Request custom field**: Update `customfield_10875` on TC-9201 with the PR URL in ADF format:
   ```
   jira.update_issue(TC-9201, fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
   ```

2. **Add comment** with PR link, summary of changes, and any deviations. The comment ends with the plugin version footnote (read from `plugins/sdlc-workflow/.claude-plugin/plugin.json`):
   ```
   Implementation complete for TC-9201.

   PR: <PR-URL>

   Changes:
   - Created SeveritySummary model struct
   - Added severity_summary method to AdvisoryService
   - Added GET /api/v2/sbom/{id}/advisory-summary endpoint
   - Registered route in endpoints/mod.rs
   - Added 4 integration tests

   No deviations from the plan.

   ---
   This comment was AI-generated by sdlc-workflow/implement-task v{version}.
   ```

3. **Transition**: `jira.transition_issue(TC-9201, "In Review")`
