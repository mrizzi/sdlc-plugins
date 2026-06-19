# Implementation Plan for TC-9205

## Task Summary

**Jira ID:** TC-9205
**Summary:** Add migration to drop status table column
**Repository:** trustify-backend
**Target Branch:** TC-9005 (feature branch)
**Linked Feature:** TC-9005 (this task is incorporated by TC-9005)
**Dependencies:** None

## Target Branch Handling

The task's Target Branch is **TC-9005**, which is a feature branch (not `main`). This means:

1. The base for branching is `TC-9005`
2. The PR must target `--base TC-9005`
3. The task branch is named `TC-9205` (the task issue ID, not the feature branch ID)

## Branch Operations

```bash
# Step 1: Check out the target branch (the feature branch TC-9005)
git checkout TC-9005
git pull

# Step 2: Create the task branch from TC-9005
git checkout -b TC-9205

# Step 3: (after implementation) Push and create PR targeting TC-9005
git push -u origin TC-9205
gh pr create --base TC-9005 --title "feat(migration): add migration to drop advisory status column" --body "## Summary
- Add database migration m0002_drop_advisory_status that drops the deprecated \`status\` column from the \`advisory\` table
- Register the new migration module in migration/src/lib.rs

## Jira
Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)"
```

## Pre-Implementation Code Inspection (Constraint 1.5)

Before making any changes, the following files would be inspected:

1. **`migration/src/lib.rs`** -- Inspect the current migration registration pattern: how `migrations()` function is structured, how `m0001_initial` is imported and added to the vec.
2. **`migration/src/m0001_initial/mod.rs`** -- Inspect the sibling migration to understand the exact pattern for implementing `MigrationTrait`, including imports, struct definition, `up`/`down` method signatures, and SeaORM API usage.
3. **`entity/src/advisory.rs`** -- Verify that the `status` column is NOT referenced in the entity definition (confirming the description's claim that it was already removed). Check that the `Advisory` enum still has a `Table` variant and whether there is a `Status` variant available for use in the migration.
4. **`entity/src/lib.rs`** -- Check for any re-exports or references to advisory status.
5. **Grep across the codebase** for any references to `status` in the context of advisories -- `advisory.*status` or `Advisory::Status` -- to confirm no service code references the column.
6. **`CONVENTIONS.md`** at repository root -- Read for any migration-specific conventions or CI check commands.

## Files to Modify

### 1. `migration/src/lib.rs`
Register the new migration module in the migration list.

### Files to Create

### 2. `migration/src/m0002_drop_advisory_status/mod.rs`
New migration that drops the `status` column from the `advisory` table.

## Commit Message

```
feat(migration): drop deprecated status column from advisory table

Add migration m0002_drop_advisory_status that removes the unused status
column from the advisory table. The column was replaced by the severity
enum field in a previous migration and is no longer referenced by any
service or entity code.

Implements TC-9205
```

With trailer: `--trailer='Assisted-by: Claude Code'`

Full git commit command:
```bash
git commit --trailer='Assisted-by: Claude Code' -m "feat(migration): drop deprecated status column from advisory table

Add migration m0002_drop_advisory_status that removes the unused status
column from the advisory table. The column was replaced by the severity
enum field in a previous migration and is no longer referenced by any
service or entity code.

Implements TC-9205"
```

## Acceptance Criteria Verification Plan

1. **Migration drops the `status` column from the `advisory` table** -- Verified by inspecting the `up` method uses `TableAlterStatement` with `drop_column(Advisory::Status)`.
2. **Migration `down` method re-adds the column as nullable string for rollback** -- Verified by inspecting the `down` method uses `ColumnDef::new(Advisory::Status).string().null()`.
3. **Migration is registered in `migration/src/lib.rs`** -- Verified by checking the `vec![]` in `migrations()` includes `m0002_drop_advisory_status`.
4. **No service or entity code references the `status` column** -- Verified during pre-implementation grep scan across the codebase.

## Self-Verification Plan

- **Scope containment:** `git diff --name-only` must show only `migration/src/lib.rs` (modified) and `migration/src/m0002_drop_advisory_status/mod.rs` (new).
- **Untracked file check:** Verify `migration/src/m0002_drop_advisory_status/mod.rs` is staged.
- **Sensitive-pattern check:** Scan diff for secrets/credentials.
- **Contract verification:** Verify `MigrationTrait` is fully implemented (both `up` and `down` methods).
- **Sibling parity:** Compare against `m0001_initial/mod.rs` for structural parity.
- **Data-flow trace:** Migration `up` drops column (DDL only, no data flow gaps). Migration `down` re-adds column (DDL only).
- **Duplication check:** Search for any existing migration that already drops or alters the `status` column.
- **CI checks:** Run any CI commands from `CONVENTIONS.md` (e.g., `cargo check`, `cargo clippy`, `cargo test`).
