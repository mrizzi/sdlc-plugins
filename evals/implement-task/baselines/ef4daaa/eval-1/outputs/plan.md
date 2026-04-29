# Implementation Plan: TC-9201

## Task Summary

**Jira Key**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Branch**: `TC-9201`

Add a service method and REST endpoint that aggregates vulnerability advisory severity
counts for a given SBOM. The endpoint `GET /api/v2/sbom/{id}/advisory-summary` returns
a summary with counts per severity level (Critical, High, Medium, Low) and a total,
enabling dashboard widgets to render severity breakdowns without client-side counting.

---

## Step 0 -- Validate Project Configuration

The project's CLAUDE.md contains all required sections:
- Repository Registry: `trustify-backend` mapped to `serena_backend`
- Jira Configuration: Project key `TC`, Cloud ID, Feature issue type ID, custom fields
- Code Intelligence: `serena_backend` with `rust-analyzer`

Validation passes. Proceeding.

## Step 0.5 -- JIRA Access Initialization

Would attempt MCP first for all Jira operations. If MCP fails, would prompt user for REST API fallback choice.

## Step 1 -- Fetch and Parse Jira Task

Would call: `mcp__atlassian__jira__get_issue("TC-9201")`

Parsed sections from the structured description:

| Section | Content |
|---|---|
| Repository | trustify-backend |
| Description | Add severity aggregation service and endpoint |
| Files to Modify | 3 files (advisory.rs service, endpoints/mod.rs, model/mod.rs) |
| Files to Create | 3 files (severity_summary model, severity_summary endpoint, integration tests) |
| API Changes | `GET /api/v2/sbom/{id}/advisory-summary` -- NEW |
| Implementation Notes | Follow existing endpoint and service patterns |
| Acceptance Criteria | 5 items |
| Test Requirements | 4 test cases |
| Target PR | Not present (default flow) |
| Dependencies | None |

**GitHub Issue extraction**: Would check the `customfield_10747` field on the Jira issue. If present, extract the GitHub issue reference for use in the PR description's `Closes` line.

**webUrl**: Would capture the issue URL (e.g., `https://redhat.atlassian.net/browse/TC-9201`) for use in the PR description.

All required sections are present. No gaps. Proceeding.

## Step 2 -- Verify Dependencies

No dependencies listed. Proceeding.

## Step 3 -- Transition to In Progress and Assign

Would execute:
1. `mcp__atlassian__jira__user_info()` to get current user's account ID
2. `mcp__atlassian__jira__edit_issue("TC-9201", assignee=<accountId>)`
3. `mcp__atlassian__jira__transition_issue("TC-9201")` to "In Progress"

## Step 4 -- Understand the Code

### 4.1 Inspect existing files

Would use the `serena_backend` Serena instance to inspect each file:

1. **`modules/fundamental/src/advisory/service/advisory.rs`** -- `mcp__serena_backend__get_symbols_overview` to see existing methods (`fetch`, `list`, `search`). Then `mcp__serena_backend__find_symbol("fetch", include_body=true)` to understand the service method signature pattern, transactional context usage, and return types.

2. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- `mcp__serena_backend__get_symbols_overview` to see route registration pattern. Confirm `Router::new().route(...)` chain structure.

3. **`modules/fundamental/src/advisory/endpoints/get.rs`** -- `mcp__serena_backend__find_symbol("get", include_body=true)` to understand the handler pattern: `Path<Id>` extraction, service call, `Json` return.

4. **`modules/fundamental/src/advisory/model/mod.rs`** -- Read to see existing `pub mod` declarations (`pub mod summary;`, `pub mod details;`).

5. **`modules/fundamental/src/advisory/model/summary.rs`** -- `mcp__serena_backend__find_symbol("AdvisorySummary", include_body=true)` to examine the `severity` field type and derive macros.

6. **`entity/src/sbom_advisory.rs`** -- `mcp__serena_backend__get_symbols_overview` to understand the join table entity structure and available relations.

7. **`common/src/error.rs`** -- `mcp__serena_backend__find_symbol("AppError", include_body=true)` to understand error variants and `.context()` pattern.

### 4.2 Check backward compatibility

Would call `mcp__serena_backend__find_referencing_symbols` on:
- `AdvisoryService` -- to ensure adding a method won't break existing callers
- `advisory/endpoints/mod.rs` router -- to understand how routes are mounted

### 4.3 Convention conformance analysis

See `outputs/conventions.md` for full details. Key findings:
- Service methods: `verb_noun` pattern, `&self`, `Id`, `&Transactional<'_>` params, `Result<T, AppError>` return
- Endpoints: `Path<Id>` extraction, service call, `Json<T>` return
- Models: derive `Serialize, Deserialize, Debug, Clone`, doc comments on fields
- Errors: `Result<T, AppError>` with `.context()` wrapping
- Tests: `assert_eq!(resp.status(), StatusCode::OK)`, body deserialization, 404 tests included

### 4.4 CONVENTIONS.md lookup

Would read `CONVENTIONS.md` at repository root. Extract any CI check commands for Step 9.

### 4.5 Documentation files identified

- `docs/api.md` -- needs new endpoint entry
- `docs/architecture.md` -- no changes expected
- `CONVENTIONS.md` -- no changes expected

### 4.6 Cross-section reference consistency

All entity-to-path references are consistent across task sections. No mismatches detected. See `outputs/conventions.md` for the full cross-reference table.

---

## Step 5 -- Create Branch

Default flow (no Target PR). Would execute:

```
git checkout -b TC-9201
```

---

## Step 6 -- Implement Changes

### Files to Create

| # | File | Description | Details |
|---|---|---|---|
| 1 | `modules/fundamental/src/advisory/model/severity_summary.rs` | SeveritySummary response struct | See `outputs/file-1-description.md` |
| 2 | `modules/fundamental/src/advisory/endpoints/severity_summary.rs` | GET handler for `/api/v2/sbom/{id}/advisory-summary` | See `outputs/file-2-description.md` |
| 3 | `tests/api/advisory_summary.rs` | Integration tests for the new endpoint | See `outputs/file-3-description.md` |

### Files to Modify

| # | File | Description | Details |
|---|---|---|---|
| 4 | `modules/fundamental/src/advisory/service/advisory.rs` | Add `severity_summary` method to AdvisoryService | See `outputs/file-4-description.md` |
| 5 | `modules/fundamental/src/advisory/endpoints/mod.rs` | Register the new `/api/v2/sbom/{id}/advisory-summary` route | See `outputs/file-5-description.md` |
| 6 | `modules/fundamental/src/advisory/model/mod.rs` | Add `pub mod severity_summary;` module registration | See `outputs/file-6-description.md` |

### Files NOT modified

- `server/src/main.rs` -- no changes needed (routes auto-mount via module registration, as confirmed in the task description)

### Documentation impact

- `docs/api.md` -- would add a new entry for `GET /api/v2/sbom/{id}/advisory-summary` documenting the endpoint path, method, path parameters, and response shape.

---

## Step 7 -- Write Tests

See `outputs/file-3-description.md` for full test implementation details.

Four test cases per the Test Requirements:
1. `test_advisory_summary_valid_sbom` -- Valid SBOM with known advisories returns correct severity counts
2. `test_advisory_summary_not_found` -- Non-existent SBOM ID returns 404
3. `test_advisory_summary_no_advisories` -- SBOM with no advisories returns all zeros
4. `test_advisory_summary_deduplication` -- Duplicate advisory links are deduplicated in the count

Would run: `cargo test` and fix any failures before proceeding.

---

## Step 8 -- Verify Acceptance Criteria

| # | Criterion | Verification Method |
|---|---|---|
| 1 | GET /api/v2/sbom/{id}/advisory-summary returns `{ critical, high, medium, low, total }` | Test `test_advisory_summary_valid_sbom` validates response shape and field values |
| 2 | Returns 404 when SBOM ID does not exist | Test `test_advisory_summary_not_found` asserts `StatusCode::NOT_FOUND` |
| 3 | Counts only unique advisories (deduplicates by advisory ID) | Test `test_advisory_summary_deduplication` creates duplicate links and verifies counts |
| 4 | All severity levels default to 0 when no advisories exist | Test `test_advisory_summary_no_advisories` verifies all zeros |
| 5 | Response time under 200ms for SBOMs with up to 500 advisories | Verified by using an efficient SQL query with GROUP BY rather than in-memory iteration; the database handles aggregation |

---

## Step 9 -- Self-Verification

### Scope containment

Would run `git diff --name-only` and verify the output matches exactly:
- `modules/fundamental/src/advisory/service/advisory.rs` (modified)
- `modules/fundamental/src/advisory/endpoints/mod.rs` (modified)
- `modules/fundamental/src/advisory/model/mod.rs` (modified)
- `modules/fundamental/src/advisory/model/severity_summary.rs` (created)
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (created)
- `tests/api/advisory_summary.rs` (created)

Plus potentially `docs/api.md` (documentation update) -- if present, would explain it as a documentation-impact update and ask user to approve.

### Untracked file check

Would run `git status --short` and check for `??`-prefixed entries in directories where implementation occurred. Any untracked files referenced by code (e.g., via `include_str!`) would be flagged.

### Sensitive-pattern check

Would run: `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'`

No secrets expected in this implementation.

### Documentation currency

Would verify `docs/api.md` reflects the new endpoint if it was not already updated in Step 6.

### Duplication check

Would search for existing severity aggregation functions or similar patterns using:
- `mcp__serena_backend__search_for_pattern("severity_summary")` or `mcp__serena_backend__search_for_pattern("severity.*count")`
- Grep for similar function names or logic patterns

If no duplicates found, proceed.

### Data-flow trace

```
GET /api/v2/sbom/{id}/advisory-summary
  -> Path<Id> extraction (input)
  -> AdvisoryService::severity_summary(sbom_id, tx) (processing)
    -> Query sbom_advisory join table for SBOM (database read)
    -> Join with advisory table to get severity values (database join)
    -> GROUP BY severity, COUNT, deduplicate by advisory ID (aggregation)
    -> Map results to SeveritySummary struct (transformation)
  -> Json<SeveritySummary> (output)
```

All stages connected. Data flow is COMPLETE.

### Contract and sibling parity

- **SeveritySummary** struct: no trait/interface contract to implement beyond `Serialize`, `Deserialize`, which are derived
- **severity_summary handler**: follows the same pattern as `get.rs` handler (Path extraction, service call, Json return) -- parity maintained
- **severity_summary service method**: follows the same signature pattern as `fetch` and `list` methods -- parity maintained
- **Error handling**: uses `AppError` with `.context()` wrapping, same as siblings
- **404 handling**: returns `AppError::NotFound` for non-existent SBOM, consistent with sibling endpoints

### Cross-module shared entity analysis

- Entity `sbom_advisory`: read-only access (SELECT/JOIN only). The new code does not insert, update, or delete from this entity. No cross-module anomaly risk.

### CI checks from CONVENTIONS.md

Would run all CI check commands extracted from `CONVENTIONS.md` (e.g., `cargo fmt --check`, `cargo clippy`, `cargo test`). Fix any failures.

---

## Step 10 -- Commit and Push

### Commit message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add a new service method and REST endpoint that aggregates vulnerability
advisory severity counts for a given SBOM. The endpoint returns counts
per severity level (Critical, High, Medium, Low) and a total, enabling
dashboard widgets to render severity breakdowns without client-side
counting.

New endpoint: GET /api/v2/sbom/{id}/advisory-summary

Implements TC-9201
```

### Commit command

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
      modules/fundamental/src/advisory/endpoints/severity_summary.rs \
      modules/fundamental/src/advisory/service/advisory.rs \
      modules/fundamental/src/advisory/endpoints/mod.rs \
      modules/fundamental/src/advisory/model/mod.rs \
      tests/api/advisory_summary.rs

git commit --trailer='Assisted-by: Claude Code' -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add a new service method and REST endpoint that aggregates vulnerability
advisory severity counts for a given SBOM. The endpoint returns counts
per severity level (Critical, High, Medium, Low) and a total, enabling
dashboard widgets to render severity breakdowns without client-side
counting.

New endpoint: GET /api/v2/sbom/{id}/advisory-summary

Implements TC-9201"
```

### Push and PR

```bash
git push -u origin TC-9201
```

Would create a pull request:

```bash
gh pr create --title "feat(advisory): add severity aggregation endpoint for SBOM advisories" --body "$(cat <<'EOF'
## Summary

Add a new service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM.

- New response struct `SeveritySummary` with `critical`, `high`, `medium`, `low`, `total` fields
- New `severity_summary` method on `AdvisoryService` querying the `sbom_advisory` join table
- New endpoint handler at `GET /api/v2/sbom/{id}/advisory-summary`
- Integration tests covering valid SBOM, 404, empty advisories, and deduplication

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)

## Test plan

- [x] `test_advisory_summary_valid_sbom` -- Valid SBOM returns correct severity counts
- [x] `test_advisory_summary_not_found` -- Non-existent SBOM returns 404
- [x] `test_advisory_summary_no_advisories` -- Empty SBOM returns all zeros
- [x] `test_advisory_summary_deduplication` -- Duplicate advisory links are deduplicated
EOF
)"
```

If a GitHub issue reference was extracted from `customfield_10747` in Step 1, would append `Closes <owner>/<repo>#<number>` to the PR body.

---

## Step 11 -- Update Jira

1. **Update Git Pull Request custom field** (`customfield_10875`) with PR URL using ADF format:
   ```
   mcp__atlassian__jira__update_issue("TC-9201", fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
   ```

2. **Add comment** to TC-9201 via `mcp__atlassian__jira__add_comment`:
   - PR link
   - Summary: Added SeveritySummary model, severity_summary service method, GET endpoint at /api/v2/sbom/{id}/advisory-summary, and 4 integration tests
   - No deviations from the plan
   - Comment footer with AI-generation attribution (sdlc-workflow/implement-task v{version})

3. **Transition** TC-9201 to "In Review":
   ```
   mcp__atlassian__jira__transition_issue("TC-9201") -> In Review
   ```
