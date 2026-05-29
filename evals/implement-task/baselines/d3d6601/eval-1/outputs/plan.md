# Implementation Plan for TC-9201

## Task Summary

Add an advisory severity aggregation service method and REST endpoint that returns severity counts (Critical, High, Medium, Low, total) for a given SBOM, enabling dashboard widgets to render severity breakdowns.

## Branch

- **Branch name**: TC-9201
- **Base branch (Target Branch)**: main
- **Commands**:
  ```
  git checkout main
  git pull
  git checkout -b TC-9201
  ```

## Pre-Implementation: Code Inspection (Step 4)

Before modifying any files, inspect existing code using Serena instance `serena_backend`:

1. `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/service/advisory.rs` -- understand AdvisoryService structure (fetch, list, search methods)
2. `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisoryService::fetch` -- understand existing method pattern for the new `severity_summary` method
3. `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/get.rs` -- understand endpoint handler pattern (Path extraction, service call, JSON return)
4. `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/summary.rs` -- understand AdvisorySummary struct and its `severity` field
5. `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/mod.rs` -- understand route registration pattern
6. `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/mod.rs` -- understand model module registration
7. `mcp__serena_backend__get_symbols_overview` on `entity/src/sbom_advisory.rs` -- understand the join table for SBOM-Advisory relationships
8. `mcp__serena_backend__find_referencing_symbols` on any symbols planned for modification -- verify no callers would break
9. Read `CONVENTIONS.md` at repository root for CI check commands and additional conventions
10. Inspect sibling files for convention conformance analysis (see conventions.md)

## Files to Create

1. **`modules/fundamental/src/advisory/model/severity_summary.rs`** -- SeveritySummary response struct
2. **`modules/fundamental/src/advisory/endpoints/severity_summary.rs`** -- GET handler for /api/v2/sbom/{id}/advisory-summary
3. **`tests/api/advisory_summary.rs`** -- Integration tests for the new endpoint

## Files to Modify

1. **`modules/fundamental/src/advisory/service/advisory.rs`** -- Add `severity_summary` method to AdvisoryService
2. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- Register the new route
3. **`modules/fundamental/src/advisory/model/mod.rs`** -- Add `pub mod severity_summary;` to register the new model module

## Files NOT Modified

- `server/src/main.rs` -- No changes needed (routes auto-mount via module registration, as confirmed by task description)

## Cross-Section Reference Consistency Check

- Entity `AdvisoryService` -- Files to Modify: `modules/fundamental/src/advisory/service/advisory.rs`, Implementation Notes: `modules/fundamental/src/advisory/service/advisory.rs` -- **CONSISTENT**
- Entity `AdvisorySummary` -- Implementation Notes reference `modules/fundamental/src/advisory/model/summary.rs` for its `severity` field -- **CONSISTENT** (reading from this file, not modifying it)
- Entity `sbom_advisory` join table -- Implementation Notes: `entity/src/sbom_advisory.rs` -- **CONSISTENT**
- Entity route registration -- Files to Modify: `modules/fundamental/src/advisory/endpoints/mod.rs`, Implementation Notes: same -- **CONSISTENT**

## Data-Flow Trace

- `GET /api/v2/sbom/{id}/advisory-summary` request received
  -> Axum extracts `Path<Id>` (sbom_id) -- **INPUT**
  -> Handler calls `AdvisoryService::severity_summary(sbom_id, tx)` -- **PROCESSING**
  -> Service queries `sbom_advisory` join table for advisories linked to SBOM -- **PROCESSING**
  -> Service loads `AdvisorySummary` for each advisory, reads `severity` field -- **PROCESSING**
  -> Service deduplicates by advisory ID -- **PROCESSING**
  -> Service counts by severity level (Critical, High, Medium, Low), computes total -- **PROCESSING**
  -> Service returns `SeveritySummary` struct -- **OUTPUT**
  -> Handler returns `Json<SeveritySummary>` as HTTP response -- **OUTPUT**
  -> **COMPLETE**

## Commit Message

```
feat(api): add advisory severity aggregation endpoint

Add SeveritySummary model, AdvisoryService::severity_summary method,
and GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
per-severity advisory counts for a given SBOM.

Implements TC-9201
```

With trailer: `--trailer="Assisted-by: Claude Code"`

## PR Details

- **Base branch**: main (from Target Branch)
- **Command**: `gh pr create --base main --title "feat(api): add advisory severity aggregation endpoint" --body "..."`
- **PR description** would include:
  - Summary of changes
  - `Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)` (clickable Jira link)
  - If GitHub Issue custom field had a value, would include `Closes <owner>/<repo>#<number>`

## Jira Updates (Step 11)

1. Update Git Pull Request custom field (`customfield_10875`) with PR URL in ADF format
2. Add comment with PR link, summary of changes, and any deviations
3. Transition TC-9201 to "In Review"

## Self-Verification Checklist (Step 9)

- [ ] `git diff --name-only` matches Files to Modify + Files to Create
- [ ] No out-of-scope files modified
- [ ] Untracked file check -- verify all new files are in Files to Create
- [ ] Sensitive-pattern check on staged diff
- [ ] Documentation currency -- update `docs/api.md` if it lists API endpoints
- [ ] Duplication check -- search for existing severity aggregation logic
- [ ] CI checks from CONVENTIONS.md -- run all extracted verification commands
- [ ] Contract & sibling parity -- verify SeveritySummary follows sibling model patterns
- [ ] Caller-site parity -- no shared abstractions called in novel ways
