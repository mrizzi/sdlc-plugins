# Implementation Plan for TC-9201

## Task Summary

**Jira Key:** TC-9201
**Summary:** Add advisory severity aggregation service and endpoint
**Repository:** trustify-backend
**Target Branch:** main
**Dependencies:** None

## Pre-Implementation Inspection (Step 4)

Before making any changes, the following files would be inspected using the Serena instance `serena_backend` (tools called as `mcp__serena_backend__<tool>`):

1. **`modules/fundamental/src/advisory/endpoints/get.rs`** -- Use `mcp__serena_backend__get_symbols_overview` to understand the existing endpoint handler pattern (path param extraction, service call, JSON response). Then use `mcp__serena_backend__find_symbol` with `include_body=true` on the handler function to see the full implementation.

2. **`modules/fundamental/src/advisory/service/advisory.rs`** -- Use `mcp__serena_backend__get_symbols_overview` to see the `AdvisoryService` struct and its existing methods (`fetch`, `list`, `search`). Use `mcp__serena_backend__find_symbol` on `fetch` with `include_body=true` to understand the method signature pattern (`&self`, ID param, `tx: &Transactional<'_>`, return type `Result<T, AppError>`).

3. **`modules/fundamental/src/advisory/model/summary.rs`** -- Use `mcp__serena_backend__get_symbols_overview` to inspect the `AdvisorySummary` struct and its `severity` field, which will be used for counting by severity level.

4. **`modules/fundamental/src/advisory/model/mod.rs`** -- Read to see how existing model sub-modules are registered (`pub mod summary;`, `pub mod details;`).

5. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- Read to see how existing routes are registered (`Router::new().route(...)` pattern).

6. **`entity/src/sbom_advisory.rs`** -- Read to understand the SBOM-Advisory join table structure for querying advisories linked to an SBOM.

7. **`common/src/error.rs`** -- Read to understand the `AppError` enum and how 404 responses are produced.

8. **Sibling analysis (endpoints):** Use `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/sbom/endpoints/get.rs` and `modules/fundamental/src/advisory/endpoints/list.rs` to confirm endpoint conventions.

9. **Sibling analysis (services):** Use `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/sbom/service/sbom.rs` to confirm service method conventions across modules.

10. **Sibling analysis (tests):** Use `mcp__serena_backend__get_symbols_overview` on `tests/api/advisory.rs` and `tests/api/sbom.rs` to understand test patterns (assertion style, setup, naming).

11. **CONVENTIONS.md:** Check for `./CONVENTIONS.md` at the repository root. Read it for project-level conventions and CI check commands.

12. **Documentation files:** Check for README files in `modules/fundamental/src/advisory/` and `docs/api.md` for documentation that might need updating.

## Branch Strategy

```
git checkout main
git pull
git checkout -b TC-9201
```

Branch `TC-9201` based on Target Branch `main`.

## Files to Create (3 files)

### 1. `modules/fundamental/src/advisory/model/severity_summary.rs`

New file: `SeveritySummary` response struct for the severity aggregation endpoint.

### 2. `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

New file: GET handler for `/api/v2/sbom/{id}/advisory-summary`.

### 3. `tests/api/advisory_summary.rs`

New file: Integration tests for the new endpoint.

## Files to Modify (3 files)

### 4. `modules/fundamental/src/advisory/service/advisory.rs`

Add `severity_summary` method to `AdvisoryService`.

### 5. `modules/fundamental/src/advisory/endpoints/mod.rs`

Register the new `/api/v2/sbom/{id}/advisory-summary` route.

### 6. `modules/fundamental/src/advisory/model/mod.rs`

Add `pub mod severity_summary;` to register the new model module.

## Out-of-Scope

- `server/src/main.rs` -- the task description confirms no changes are needed (routes auto-mount via module registration).

## Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes SeveritySummary model, service method,
endpoint handler, and integration tests.

Implements TC-9201
```

## Git Commit Command

```
git add modules/fundamental/src/advisory/model/severity_summary.rs \
      modules/fundamental/src/advisory/endpoints/severity_summary.rs \
      tests/api/advisory_summary.rs \
      modules/fundamental/src/advisory/service/advisory.rs \
      modules/fundamental/src/advisory/endpoints/mod.rs \
      modules/fundamental/src/advisory/model/mod.rs

git commit --trailer='Assisted-by: Claude Code' -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes SeveritySummary model, service method,
endpoint handler, and integration tests.

Implements TC-9201"
```

The `--trailer='Assisted-by: Claude Code'` flag is used to attribute AI assistance per the skill instructions.

## Push and PR

```
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint for SBOM advisories" --body "..."
```

The PR description would include:
- Summary of changes
- `Implements [TC-9201](<webUrl>)` with clickable Jira link
- If a GitHub Issue custom field is present on the Jira issue, a `Closes <owner>/<repo>#<number>` line

## Self-Verification Checklist

- [ ] `git diff --name-only` matches Files to Modify and Files to Create -- no out-of-scope files
- [ ] `git status --short` checked for untracked files in modified directories
- [ ] `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` -- no sensitive patterns
- [ ] Documentation currency: `docs/api.md` checked for staleness after adding new endpoint
- [ ] Duplication check: Grep for similar aggregation/summary functions in the codebase
- [ ] Data-flow trace: request -> path param extraction -> service call -> DB query -> response -- all stages connected
- [ ] Contract & sibling parity: handler signature, error handling, response type match siblings
- [ ] CI checks from CONVENTIONS.md: run all extracted verification commands

## Jira Updates (Step 11)

1. Update Git Pull Request custom field (`customfield_10875`) with PR URL in ADF format
2. Add Jira comment with PR link, summary of changes, and any deviations
3. Transition TC-9201 to "In Review"
