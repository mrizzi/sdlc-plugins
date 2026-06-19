# Implementation Plan for TC-9201: Add Advisory Severity Aggregation Service and Endpoint

## Task Summary

Add a service method and REST endpoint to the trustify-backend that aggregates vulnerability advisory severity counts for a given SBOM. The endpoint (`GET /api/v2/sbom/{id}/advisory-summary`) returns counts per severity level (Critical, High, Medium, Low) plus a total.

---

## Step 0 -- Validate Project Configuration

Verify CLAUDE.md contains the required sections:

1. **Repository Registry** -- present, maps `trustify-backend` to Serena instance `serena_backend` at path `./`
2. **Jira Configuration** -- present with Project key `TC`, Cloud ID, Feature issue type ID, custom fields
3. **Code Intelligence** -- present, tool naming convention `mcp__serena_backend__<tool>`, rust-analyzer LSP

All sections are complete. Proceed.

## Step 0.5 -- JIRA Access Initialization

Attempt MCP for all JIRA operations. If MCP fails, prompt user for REST API fallback per the defined protocol.

## Step 1 -- Fetch and Parse Jira Task

Fetch `TC-9201` via `jira.get_issue("TC-9201")`. Parse the structured description:

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | main |
| Description | Add severity aggregation service and endpoint |
| Files to Modify | 3 files (advisory service, endpoints/mod.rs, model/mod.rs) |
| Files to Create | 3 files (severity_summary model, endpoint handler, integration tests) |
| API Changes | `GET /api/v2/sbom/{id}/advisory-summary` (NEW) |
| Bookend Type | (none) |
| Target PR | (none) |
| Dependencies | None |

Capture the issue `webUrl` for use in the PR description.

Check the GitHub Issue custom field (`customfield_10747`) -- extract reference if present.

## Step 1.5 -- Verify Description Integrity

1. Fetch comments: `jira.get_issue_comments("TC-9201")`
2. Locate digest comment by searching for marker `[sdlc-workflow] Description digest:`
3. Found: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
4. Comment `created` == `updated` -- no edit detected, no warning
5. Extract format tag: `md`, hex digest: `a1b2c3d4e5f67890...`
6. Compute current digest: `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt` -- outputs `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
7. Tags match (`sha256-md` == `sha256-md`), hex digests match
8. **Result: MATCH -- proceed silently, no user prompt, no latency**

## Step 2 -- Verify Dependencies

The task lists "Dependencies: None". No dependency checks needed. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user: `jira.user_info()`
2. Assign task: `jira.edit_issue("TC-9201", assignee=<current-user-account-id>)`
3. Transition: `jira.transition_issue("TC-9201")` to "In Progress"

## Step 4 -- Understand the Code

Use Serena instance `serena_backend` (tools called as `mcp__serena_backend__<tool>`).

### 4.1 Inspect files to modify

- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/service/advisory.rs` -- understand `AdvisoryService` structure, `fetch` and `list` method signatures
- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/mod.rs` -- understand route registration pattern
- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/mod.rs` -- understand module registration

### 4.2 Read specific symbols

- `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisoryService::fetch` and `AdvisoryService::list` to understand the method pattern (parameters, return types, transactional handling)
- `mcp__serena_backend__find_symbol` on `AdvisorySummary` to inspect the `severity` field

### 4.3 Check backward compatibility

- `mcp__serena_backend__find_referencing_symbols` on any symbols being modified to ensure no callers break

### 4.4 Inspect sibling files for conventions

- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/get.rs` -- understand endpoint handler pattern (Path extraction, service call, JSON response)
- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/list.rs` -- understand list endpoint pattern
- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/summary.rs` -- understand model struct pattern

### 4.5 Inspect related entities

- `mcp__serena_backend__get_symbols_overview` on `entity/src/sbom_advisory.rs` -- understand the join table for SBOM-Advisory relationships

### 4.6 CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at the repository root. If present, read it and extract:
- Naming conventions, directory structure rules
- CI check commands (for Step 9)
- Code generation commands

### 4.7 Convention conformance analysis

Examine sibling files (advisory endpoints, models, services) for patterns:
- Error handling: `Result<T, AppError>` with `.context()` wrapping
- Naming: service methods follow `verb_noun` pattern
- Endpoint pattern: `Path<Id>` extraction, service call, `Json` response
- Route registration: `Router::new().route("/path", get(handler))`
- Model pattern: structs with `#[derive(Serialize, Deserialize)]`

### 4.8 Test convention analysis

- Inspect `tests/api/advisory.rs` and `tests/api/sbom.rs` for test patterns:
  - Assertion style (`assert_eq!(resp.status(), StatusCode::OK)`)
  - Response validation (body deserialization, field checks)
  - Error case patterns (404 tests)
  - Test naming conventions
  - Setup/teardown patterns

### 4.9 Documentation file identification

- Check for README files in `modules/fundamental/src/advisory/`
- Check `docs/api.md` for API documentation
- Note `CONVENTIONS.md` if found

## Step 5 -- Create Branch

Default flow (no Target PR, no Bookend Type):

```bash
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 -- Implement Changes

### 6.1 Create `modules/fundamental/src/advisory/model/severity_summary.rs`

Define the `SeveritySummary` response struct:

```rust
use serde::{Deserialize, Serialize};

/// Summary of advisory severity counts for an SBOM.
#[derive(Clone, Debug, Default, Serialize, Deserialize)]
pub struct SeveritySummary {
    /// Count of critical-severity advisories.
    pub critical: u32,
    /// Count of high-severity advisories.
    pub high: u32,
    /// Count of medium-severity advisories.
    pub medium: u32,
    /// Count of low-severity advisories.
    pub low: u32,
    /// Total count of unique advisories across all severity levels.
    pub total: u32,
}
```

### 6.2 Modify `modules/fundamental/src/advisory/model/mod.rs`

Add `pub mod severity_summary;` to register the new model module.

### 6.3 Add `severity_summary` method to `AdvisoryService`

Modify `modules/fundamental/src/advisory/service/advisory.rs`:

- Add a `severity_summary` method following the pattern of `fetch` and `list`
- Method signature: `pub async fn severity_summary(&self, sbom_id: Id, tx: &Transactional<'_>) -> Result<SeveritySummary, AppError>`
- Use the `sbom_advisory` join table to find advisories linked to the SBOM
- Load `AdvisorySummary` for each linked advisory, read the `severity` field
- Deduplicate by advisory ID before counting
- Count by severity level (Critical, High, Medium, Low)
- Default all counts to 0 when no advisories exist at that level
- Return 404 (via `AppError`) if the SBOM ID does not exist

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Define the GET handler:

```rust
/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns a severity summary with counts per severity level for all
/// advisories linked to the specified SBOM.
pub async fn severity_summary(
    Path(id): Path<Id>,
    // ... service and transaction extractors following existing pattern
) -> Result<Json<SeveritySummary>, AppError> {
    // Call service method, return JSON response
    // Follow pattern from get.rs
}
```

### 6.5 Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

Register the new route following existing patterns:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::severity_summary))
```

### 6.6 Code quality verification

- Ensure all new structs, types, and public functions have documentation comments (`///`)
- Verify error handling uses `.context()` wrapping consistently

### 6.7 Documentation impact

- Check if `docs/api.md` needs updating with the new endpoint
- No Documentation Updates section in the task, so evaluate based on Step 4 findings

## Step 7 -- Write Tests

Create `tests/api/advisory_summary.rs` with integration tests following sibling test conventions:

### Test 1: Valid SBOM with known advisories

```rust
/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_with_known_advisories() {
    // Given an SBOM with advisories at known severity levels
    // When requesting GET /api/v2/sbom/{id}/advisory-summary
    // Then the response contains correct counts per severity level
}
```

### Test 2: Non-existent SBOM returns 404

```rust
/// Verifies that a non-existent SBOM ID returns 404 Not Found.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID
    // When requesting GET /api/v2/sbom/{id}/advisory-summary
    // Then the response status is 404
}
```

### Test 3: SBOM with no advisories returns all zeros

```rust
/// Verifies that an SBOM with no linked advisories returns all-zero counts.
#[tokio::test]
async fn test_advisory_summary_no_advisories() {
    // Given an SBOM with no linked advisories
    // When requesting GET /api/v2/sbom/{id}/advisory-summary
    // Then all severity counts are 0 and total is 0
}
```

### Test 4: Duplicate advisory links are deduplicated

```rust
/// Verifies that duplicate advisory links are deduplicated in the severity count.
#[tokio::test]
async fn test_advisory_summary_deduplicates() {
    // Given an SBOM with duplicate advisory links
    // When requesting GET /api/v2/sbom/{id}/advisory-summary
    // Then each advisory is counted only once
}
```

Run tests: `cargo test` -- fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| GET endpoint returns `{ critical, high, medium, low, total }` | Test 1 validates response shape and values |
| Returns 404 for non-existent SBOM | Test 2 validates 404 response |
| Counts only unique advisories | Test 4 validates deduplication |
| All severity levels default to 0 | Test 3 validates zero defaults |
| Response time under 200ms for up to 500 advisories | Verify via test timing or manual check |

## Step 9 -- Self-Verification

### Scope containment

Run `git diff --name-only` and compare against the task's Files to Modify and Files to Create lists. Flag any out-of-scope files.

Expected files:
- Modified: `advisory/service/advisory.rs`, `advisory/endpoints/mod.rs`, `advisory/model/mod.rs`
- Created: `advisory/model/severity_summary.rs`, `advisory/endpoints/severity_summary.rs`, `tests/api/advisory_summary.rs`

### Untracked file check

Run `git status --short`, filter `??` entries by proximity to modified directories. Search for code references to any untracked files.

### Sensitive-pattern check

Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` -- ensure no secrets are staged.

### Documentation currency

If public API docs exist (e.g., `docs/api.md`), verify the new endpoint is documented.

### CI checks from CONVENTIONS.md

If CI check commands were extracted in Step 4, run them all. Hard stop on any failure.

### Data-flow trace

- `GET /api/v2/sbom/{id}/advisory-summary` -> extract path param -> call `AdvisoryService::severity_summary` -> query `sbom_advisory` join table -> load advisories -> count by severity -> return `SeveritySummary` JSON -- **COMPLETE**

### Contract and sibling parity

- `SeveritySummary` struct: standalone, no trait/interface to implement
- Sibling parity with `get.rs`, `list.rs` endpoints: error handling, response pattern, route registration
- Cross-module check: `sbom_advisory` entity used in ingestor module -- compare query patterns

### Duplication check

Search for existing severity counting or aggregation logic in the codebase to ensure no duplication.

## Step 10 -- Commit and Push

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
      modules/fundamental/src/advisory/model/mod.rs \
      modules/fundamental/src/advisory/service/advisory.rs \
      modules/fundamental/src/advisory/endpoints/severity_summary.rs \
      modules/fundamental/src/advisory/endpoints/mod.rs \
      tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary that returns severity counts
(critical, high, medium, low, total) for advisories linked to an SBOM.
Includes SeveritySummary model, AdvisoryService method, and integration tests.

Implements TC-9201"

git push -u origin TC-9201

gh pr create --base main --title "feat(api): add advisory severity aggregation endpoint" --body "## Summary

Add a new REST endpoint that aggregates vulnerability advisory severity counts
for a given SBOM, enabling dashboard widgets to render severity breakdowns.

- Add \`SeveritySummary\` response struct in advisory model
- Add \`severity_summary\` method to \`AdvisoryService\`
- Add \`GET /api/v2/sbom/{id}/advisory-summary\` endpoint handler
- Add integration tests for the new endpoint

Implements [TC-9201](<webUrl>)
"
```

## Step 11 -- Update Jira

1. Update Git Pull Request custom field (`customfield_10875`) with the PR URL in ADF format
2. Add comment to TC-9201 with:
   - PR link
   - Summary of changes (new endpoint, model, service method, tests)
   - No deviations from plan
   - Include skill footnote with version from `plugin.json`
3. Transition TC-9201 to "In Review"
