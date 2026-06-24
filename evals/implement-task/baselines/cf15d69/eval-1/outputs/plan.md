# Implementation Plan for TC-9201

## Task Summary

**Jira ID**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Branch Name**: TC-9201
**Flow**: Default (no Target PR, no Bookend Type)

## Step 0 -- Project Configuration Validation

Validated CLAUDE.md sections:
- Repository Registry: present (trustify-backend, serena_backend, ./)
- Jira Configuration: present (Project key TC, Cloud ID, Feature issue type ID 10142)
- Code Intelligence: present (tool naming convention documented)

All required sections are present. Proceeding.

## Step 1 -- Task Parsing

Parsed all required sections from the task description:
- Repository: trustify-backend
- Target Branch: main
- Description: Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM
- Files to Modify: 3 files
- Files to Create: 3 files
- API Changes: GET /api/v2/sbom/{id}/advisory-summary (NEW)
- Implementation Notes: present with specific code patterns and references
- Acceptance Criteria: 5 criteria
- Test Requirements: 4 test cases
- Dependencies: None
- Target PR: not present
- Bookend Type: not present

### Target Branch Extraction

Target Branch: `main`. This value will be used for `git checkout main` in Step 5 and `gh pr create --base main` in Step 10.

### GitHub Issue Extraction

GitHub Issue custom field: `customfield_10747`. Would be read from the fetched issue's fields. Not present in mock data -- skipped silently.

## Step 1.5 -- Description Digest Verification

Would perform the following:
1. Fetch comments via `jira.get_issue_comments(TC-9201)`
2. Search for comments with marker `[sdlc-workflow] Description digest:`
3. If found, extract tagged digest, compute current digest via `python3 scripts/sha256-digest.py`, compare format tags and hex digests
4. If not found, log warning and proceed

## Step 2 -- Dependency Verification

No dependencies listed. Proceeding.

## Step 3 -- Transition to In Progress

Would execute:
1. `jira.user_info()` to get current user account ID
2. `jira.edit_issue(TC-9201, assignee=<account-id>)` to assign
3. `jira.transition_issue(TC-9201)` to In Progress

## Step 4 -- Code Inspection (Understand the Code)

### Files to inspect before modification

Using Serena instance `serena_backend` (tools called as `mcp__serena_backend__<tool>`):

1. `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/service/advisory.rs` -- understand existing `AdvisoryService` methods (`fetch`, `list`, `search`), their signatures, and the `severity_summary` insertion point
2. `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisoryService::fetch` -- understand the exact pattern for service methods (parameter types, return type, error handling, transactional usage)
3. `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/mod.rs` -- understand route registration pattern
4. `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/get.rs` -- understand endpoint handler pattern (Path extraction, service call, JSON response)
5. `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/mod.rs` -- understand model module registration
6. `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/summary.rs` -- understand `AdvisorySummary` struct and its `severity` field
7. `mcp__serena_backend__find_symbol` on `entity::sbom_advisory` -- understand the join table schema
8. `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` -- identify all callers to ensure backward compatibility

### Sibling analysis for convention conformance

1. Siblings of `severity_summary.rs` (model): inspect `summary.rs` and `details.rs` in `modules/fundamental/src/advisory/model/`
2. Siblings of `severity_summary.rs` (endpoint): inspect `get.rs` and `list.rs` in `modules/fundamental/src/advisory/endpoints/`
3. Siblings of `advisory_summary.rs` (test): inspect `advisory.rs` and `sbom.rs` in `tests/api/`

### CONVENTIONS.md lookup

Would read `CONVENTIONS.md` at the repository root via `mcp__serena_backend__list_dir` or Read. Extract CI check commands and code generation commands for Step 9.

## Step 5 -- Create Branch

```bash
git checkout main
git pull
git checkout -b TC-9201
```

## Files to Modify

1. `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method
2. `modules/fundamental/src/advisory/endpoints/mod.rs` -- register the new route
3. `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;`

## Files to Create

1. `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
2. `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler
3. `tests/api/advisory_summary.rs` -- integration tests

## Step 9 -- Self-Verification Checklist

### Scope containment
Run `git diff --name-only` and verify all modified/created files match the Files to Modify and Files to Create lists exactly. Flag any out-of-scope files.

### Untracked file check
Run `git status --short`, filter `??` entries by proximity to implementation directories, search for code references to untracked files.

### Sensitive-pattern check
Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` and flag any matches.

### Documentation currency
Check if `docs/api.md` needs updating with the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint.

### Data-flow trace
- `GET /api/v2/sbom/{id}/advisory-summary` -> extract path param (Id) -> call `AdvisoryService::severity_summary(sbom_id, tx)` -> query `sbom_advisory` join table -> count by severity -> return `SeveritySummary` JSON -- **COMPLETE**

### Contract & sibling parity
- `SeveritySummary` struct: no trait/interface to implement (it is a standalone DTO) -- N/A
- Sibling parity with `get.rs`, `list.rs` endpoints: verify error handling, path extraction, service call patterns match
- Cross-module shared entity: `sbom_advisory` join table -- verify query patterns match usage in `ingestor/graph/advisory/mod.rs`

### Cross-section reference consistency
- Entity `AdvisoryService`: Files to Modify says `modules/fundamental/src/advisory/service/advisory.rs`, Implementation Notes also says `modules/fundamental/src/advisory/service/advisory.rs` -- **CONSISTENT**
- Entity `SeveritySummary`: Files to Create says `modules/fundamental/src/advisory/model/severity_summary.rs`, Implementation Notes references `AdvisorySummary` in `model/summary.rs` (different entity) -- **CONSISTENT** (different entities, no conflict)

### Duplication check
Search for existing severity aggregation logic in the codebase before implementing new code.

### CI checks from CONVENTIONS.md
Run all CI check commands extracted from `CONVENTIONS.md` (e.g., `cargo fmt --check`, `cargo clippy`, `cargo test`). Hard stop on any failure.

## Step 10 -- Commit and Push

### Commit message

```
feat(advisory): add severity aggregation service and endpoint

Add SeveritySummary model, AdvisoryService::severity_summary method,
and GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
advisory severity counts (critical, high, medium, low, total) for
a given SBOM. Includes integration tests for valid SBOM, non-existent
SBOM (404), empty advisories, and deduplication.

Implements TC-9201
```

With flag: `--trailer='Assisted-by: Claude Code'`

### Branch and PR

```bash
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity aggregation service and endpoint" --body "$(cat <<'EOF'
## Summary

Add advisory severity aggregation service and REST endpoint for dashboard severity breakdowns.

- Add `SeveritySummary` response model with critical, high, medium, low, and total counts
- Add `AdvisoryService::severity_summary` method using the `sbom_advisory` join table
- Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint
- Add integration tests covering valid SBOM, 404 for non-existent SBOM, empty advisories, and deduplication

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)

## Test plan

- [ ] `cargo test` passes all new and existing tests
- [ ] Manual test: GET /api/v2/sbom/{id}/advisory-summary returns correct severity counts
- [ ] Manual test: non-existent SBOM ID returns 404
- [ ] Manual test: SBOM with no advisories returns all zeros
EOF
)"
```

## Step 11 -- Update Jira

1. Update Git Pull Request custom field (`customfield_10875`) with PR URL in ADF format
2. Add Jira comment with PR link, summary of changes, and any deviations
3. Transition TC-9201 to In Review
