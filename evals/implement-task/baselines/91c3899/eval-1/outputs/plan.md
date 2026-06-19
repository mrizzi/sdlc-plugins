# Implementation Plan for TC-9201

## Task Summary

**Jira Key**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Target Branch**: main
**Repository**: trustify-backend
**Dependencies**: None

## Step 1 -- Parsed Task Description

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. Returns a summary with counts per severity level (Critical, High, Medium, Low) and a total.
- **Files to Modify**: 3 files
  - `modules/fundamental/src/advisory/service/advisory.rs`
  - `modules/fundamental/src/advisory/endpoints/mod.rs`
  - `modules/fundamental/src/advisory/model/mod.rs`
- **Files to Create**: 3 files
  - `modules/fundamental/src/advisory/model/severity_summary.rs`
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
  - `tests/api/advisory_summary.rs`
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` -- NEW
- **Target PR**: none
- **Bookend Type**: none
- **Review Context**: none
- **GitHub Issue**: not extracted (no Jira API access)

## Step 1.5 -- Description Integrity Verification

No Jira access available in this eval context. No digest comment can be retrieved.

Per `shared/description-digest-protocol.md` backward compatibility rules:

> "No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced."

In a real execution, implement-task would:
1. Call `jira.get_issue_comments(TC-9201)` to fetch all comments
2. Search for comments starting with marker `[sdlc-workflow] Description digest:`
3. If multiple matches, select the most recent by `created` timestamp
4. If found: extract the tagged digest, compute current description digest via `scripts/sha256-digest.py`, compare format tags, then compare hex digests
5. If not found: log warning and proceed without blocking (backward compatibility)

Proceeding with warning.

## Step 2 -- Verify Dependencies

Dependencies: None. No blocking dependencies to check.

## Step 5 -- Branch Creation

Default flow (no Target PR, no Bookend Type):

```
git checkout main
git pull
git checkout -b TC-9201
```

Branch name: `TC-9201` (named after the Jira issue ID).
Base branch: `main` (extracted from Target Branch section).

## Step 6-7 -- File Changes Overview

### Files to Create (3 files)

| # | File | Description |
|---|------|-------------|
| 1 | `modules/fundamental/src/advisory/model/severity_summary.rs` | SeveritySummary response struct |
| 2 | `modules/fundamental/src/advisory/endpoints/severity_summary.rs` | GET handler for `/api/v2/sbom/{id}/advisory-summary` |
| 3 | `tests/api/advisory_summary.rs` | Integration tests for the new endpoint |

### Files to Modify (3 files)

| # | File | Description |
|---|------|-------------|
| 4 | `modules/fundamental/src/advisory/model/mod.rs` | Add `pub mod severity_summary;` to register the new model module |
| 5 | `modules/fundamental/src/advisory/endpoints/mod.rs` | Register the new route for severity summary |
| 6 | `modules/fundamental/src/advisory/service/advisory.rs` | Add `severity_summary` method to AdvisoryService |

### Detailed changes

See `file-1-description.md` through `file-6-description.md` for detailed changes per file.

## Step 8 -- Acceptance Criteria Verification

Each acceptance criterion and how it is satisfied:

1. **GET /api/v2/sbom/{id}/advisory-summary returns `{ critical, high, medium, low, total }`** -- satisfied by the new endpoint handler that calls `AdvisoryService::severity_summary()` and returns `Json<SeveritySummary>`
2. **Returns 404 when SBOM ID does not exist** -- satisfied by the service method checking SBOM existence first and returning `AppError` with 404 status
3. **Counts only unique advisories (deduplicates by advisory ID)** -- satisfied by using `DISTINCT` or a HashSet to deduplicate advisories by ID before counting
4. **All severity levels default to 0 when no advisories exist** -- satisfied by initializing all counts to 0 in the `SeveritySummary::default()` or explicit initialization
5. **Response time under 200ms for SBOMs with up to 500 advisories** -- satisfied by performing the aggregation in a single SQL query with GROUP BY rather than loading all advisories into memory

## Step 9 -- Self-Verification Notes

### Scope containment
All 6 files (3 modified, 3 created) are within the scope defined by Files to Modify and Files to Create. No out-of-scope files.

### Data-flow trace
- `GET /api/v2/sbom/{id}/advisory-summary` -> extract path param `id` -> call `AdvisoryService::severity_summary(id, tx)` -> query `sbom_advisory` join table -> join with `advisory` table for severity -> aggregate counts -> return `Json<SeveritySummary>` -- **COMPLETE**

### Contract and sibling parity
- `SeveritySummary` follows the same derive pattern as `AdvisorySummary` and `SbomSummary`
- Endpoint handler follows the same pattern as `get.rs` handlers
- Service method follows the same signature pattern as `fetch` and `list`
- Error handling uses `Result<T, AppError>` with `.context()` consistently

## Step 10 -- Commit Message

```
feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary that returns severity counts
(critical, high, medium, low, total) for advisories linked to a given
SBOM. Includes the SeveritySummary model, AdvisoryService method, route
registration, and integration tests.

Implements TC-9201
```

The commit would be executed as:

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
      modules/fundamental/src/advisory/model/mod.rs \
      modules/fundamental/src/advisory/endpoints/severity_summary.rs \
      modules/fundamental/src/advisory/endpoints/mod.rs \
      modules/fundamental/src/advisory/service/advisory.rs \
      tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary that returns severity counts
(critical, high, medium, low, total) for advisories linked to a given
SBOM. Includes the SeveritySummary model, AdvisoryService method, route
registration, and integration tests.

Implements TC-9201"
```

## Step 10 -- Push and PR

```bash
git push -u origin TC-9201
gh pr create --base main --title "feat(api): add advisory severity aggregation endpoint" --body "$(cat <<'EOF'
## Summary

Add a new REST endpoint `GET /api/v2/sbom/{id}/advisory-summary` that aggregates vulnerability advisory severity counts for a given SBOM, returning counts per severity level (Critical, High, Medium, Low) and a total.

Changes:
- New `SeveritySummary` response struct in `modules/fundamental/src/advisory/model/severity_summary.rs`
- New `severity_summary` method on `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs`
- New GET handler in `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
- Route registration in `modules/fundamental/src/advisory/endpoints/mod.rs`
- Integration tests in `tests/api/advisory_summary.rs`

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)

## Test plan

- [ ] Verify `GET /api/v2/sbom/{id}/advisory-summary` returns correct severity counts for an SBOM with known advisories
- [ ] Verify 404 is returned for a non-existent SBOM ID
- [ ] Verify an SBOM with no advisories returns all zeros
- [ ] Verify duplicate advisory links are deduplicated in the count
- [ ] Run `cargo test` to confirm all tests pass
EOF
)"
```

## Step 11 -- Jira Update

In a real execution:
1. Set Git Pull Request custom field (`customfield_10875`) on TC-9201 with the PR URL in ADF format
2. Add a Jira comment summarizing the changes and linking the PR
3. Transition TC-9201 to "In Review"
