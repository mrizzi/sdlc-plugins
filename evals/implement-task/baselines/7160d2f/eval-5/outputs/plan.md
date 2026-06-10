# Implementation Plan for TC-9205: Add migration to drop status table column

## Task Summary

**Jira Issue:** TC-9205
**Summary:** Add a database migration that drops the deprecated `status` column from the `advisory` table.
**Parent Feature:** TC-9005 (linked via "is incorporated by")
**Target Branch:** TC-9005 (feature branch, NOT main)
**Repository:** trustify-backend

## Branch Operations

### Branch Creation

1. **Check out the target branch (feature branch TC-9005):**
   ```
   git checkout TC-9005
   git pull
   ```

2. **Create the task branch from the feature branch:**
   ```
   git checkout -b TC-9205
   ```

   The task branch `TC-9205` is based off the feature branch `TC-9005`, not `main`. This is because the task's Target Branch is `TC-9005`.

### Commit

After implementation, commit using Conventional Commits format:

```
git commit --trailer="Assisted-by: Claude Code" -m "feat(migration): add migration to drop advisory status column

Add m0002_drop_advisory_status migration that removes the deprecated
status column from the advisory table. The column was replaced by the
severity enum field and is no longer used by any service code.

The down method re-adds the column as a nullable string to support
rollback.

Implements TC-9205"
```

### Push and PR Creation

Push the branch and create a PR targeting the **feature branch TC-9005** (not main):

```
git push -u origin TC-9205
gh pr create --base TC-9005 --title "feat(migration): add migration to drop advisory status column" --body "## Summary

Add a database migration (m0002_drop_advisory_status) that drops the deprecated \`status\` column from the \`advisory\` table.

- The column was replaced by the \`severity\` enum field in a previous migration
- The \`down\` method re-adds the column as a nullable string for rollback support
- Migration is registered in \`migration/src/lib.rs\`

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)"
```

**Key detail:** The PR uses `--base TC-9005` to target the feature branch, because the task's Target Branch is `TC-9005`.

## Pre-Implementation Verification

### Step 0 - Validate Project Configuration

The project's CLAUDE.md contains all required sections:
- **Repository Registry** -- present with `trustify-backend` entry, Serena instance `serena_backend`, path `./`
- **Jira Configuration** -- present with Project key `TC`, Cloud ID, Feature issue type ID `10142`
- **Code Intelligence** -- present with tool naming convention and `serena_backend` instance for rust-analyzer

### Step 1 - Parse Task Description

All required sections are present:
- **Repository:** trustify-backend
- **Target Branch:** TC-9005 (feature branch)
- **Description:** Drop deprecated `status` column from `advisory` table
- **Files to Modify:** `migration/src/lib.rs`
- **Files to Create:** `migration/src/m0002_drop_advisory_status/mod.rs`
- **Implementation Notes:** Present with detailed patterns
- **Acceptance Criteria:** 4 items
- **Test Requirements:** 3 items
- **Dependencies:** None
- **No Target PR** (this is a new branch, not a review fix)
- **No Bookend Type** (this is a normal implementation task)

### Step 1.5 - Verify Description Integrity

Would fetch issue comments via `jira.get_issue_comments(TC-9205)` and check for a `[sdlc-workflow] Description digest:` comment. Compare computed digest against stored digest.

### Step 2 - Verify Dependencies

No dependencies listed. Proceed.

### Step 3 - Transition and Assign

1. Get current user: `jira.user_info()`
2. Assign task: `jira.edit_issue(TC-9205, assignee=<account-id>)`
3. Transition: `jira.transition_issue(TC-9205) -> In Progress`

## Code Inspection (Step 4)

### Files to Inspect

1. **`entity/src/advisory.rs`** -- Verify that the `status` column is NOT referenced in the entity model. The task states it was already removed; confirm this before proceeding.

2. **`migration/src/m0001_initial/mod.rs`** -- Inspect the existing migration to understand the pattern:
   - How `MigrationTrait` is implemented
   - The `up` and `down` method signatures
   - How table and column operations are structured
   - Import patterns

3. **`migration/src/lib.rs`** -- Inspect how migrations are registered:
   - The `mod` declaration pattern for migration modules
   - How migrations are added to the `vec![]` in the `migrations()` function

4. **Sibling analysis:** `m0001_initial/mod.rs` serves as the primary sibling for convention conformance.

5. **Advisory service and endpoint files** -- Search for any remaining references to `status` column:
   - `modules/fundamental/src/advisory/service/advisory.rs`
   - `modules/fundamental/src/advisory/model/summary.rs`
   - `modules/fundamental/src/advisory/model/details.rs`
   - `modules/fundamental/src/advisory/endpoints/list.rs`
   - `modules/fundamental/src/advisory/endpoints/get.rs`
   - `modules/ingestor/src/graph/advisory/mod.rs`

6. **CONVENTIONS.md** -- Read for project-level conventions and CI check commands.

7. **Documentation files:** Check `README.md`, `docs/architecture.md`, `docs/api.md` for migration-related documentation.

### Convention Conformance Analysis

See `conventions.md` for the full list of discovered conventions from sibling analysis.

## Files to Create

### 1. `migration/src/m0002_drop_advisory_status/mod.rs` (NEW)

A new migration module that drops the `status` column from the `advisory` table. See `file-1-description.md` for detailed implementation.

## Files to Modify

### 2. `migration/src/lib.rs` (MODIFY)

Register the new migration module. See `file-2-description.md` for detailed changes.

## Verification Steps

### Step 7 - Tests

Run `cargo test` to verify:
- The migration compiles and runs against a test database
- The rollback (down) re-adds the column
- Existing advisory queries still work after the column is dropped

### Step 8 - Acceptance Criteria Verification

1. Migration drops the `status` column from the `advisory` table -- verified by `up` method implementation
2. Migration `down` method re-adds the column as nullable string -- verified by `down` method implementation
3. Migration is registered in `migration/src/lib.rs` -- verified by lib.rs modification
4. No service or entity code references the `status` column -- verified by code inspection in Step 4

### Step 9 - Self-Verification

1. **Scope containment:** `git diff --name-only` should show only:
   - `migration/src/lib.rs` (modified)
   - `migration/src/m0002_drop_advisory_status/mod.rs` (created)

2. **Untracked file check:** Verify `m0002_drop_advisory_status/mod.rs` is staged.

3. **Sensitive-pattern check:** Scan staged diff for secrets/credentials.

4. **Data-flow trace:** Migration up drops column -> down re-adds column. Complete lifecycle.

5. **Contract & sibling parity:** `MigrationTrait` requires `up` and `down` methods -- both implemented. Sibling parity with `m0001_initial` -- same pattern followed.

6. **CI checks:** Run any CI commands from `CONVENTIONS.md`.

## Jira Updates (Step 11)

1. **Update Git Pull Request custom field** (`customfield_10875`) with PR URL in ADF format
2. **Add comment** to TC-9205 with PR link and summary of changes
3. **Transition** TC-9205 to **In Review**
