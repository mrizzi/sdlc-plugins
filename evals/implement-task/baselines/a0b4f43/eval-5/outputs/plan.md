# Implementation Plan: TC-9205

## Task Summary

**Jira Issue:** TC-9205
**Summary:** Add migration to drop status table column
**Repository:** trustify-backend
**Target Branch:** TC-9005 (feature branch -- extracted from the Target Branch section of the task description)
**Linked Feature:** TC-9005 (this task is incorporated by TC-9005)

The task requires adding a SeaORM database migration that drops the deprecated `status` column from the `advisory` table. The column was previously replaced by a `severity` enum field and is no longer referenced by service or entity code.

---

## Target Branch Analysis

The task description contains a **Target Branch** section with the value `TC-9005`. This indicates the task is part of a **feature-branch workflow** -- the parent feature issue is TC-9005, and all intermediate implementation tasks target that feature branch rather than `main`. This is critical for both branch creation (Step 5) and PR creation (Step 10).

---

## Branch Operations

### Step 5 -- Create Branch (Default flow, no Target PR, no Bookend Type)

The Target Branch is `TC-9005`, so the task branch is based on the feature branch, not `main`.

```bash
git checkout TC-9005
git pull
git checkout -b TC-9205
```

- **Checkout TC-9005** (the Target Branch from the task description) -- NOT `main`
- **Pull latest** to ensure the branch is up to date
- **Create task branch TC-9205** (named after the task issue ID, per constraint 3.1) -- this is distinct from TC-9005 (the feature branch)

### Step 10 -- Push and Open PR

```bash
git push -u origin TC-9205
gh pr create --base TC-9005 --head TC-9205 --title "feat(migration): add migration to drop advisory status column" --body "## Summary
- Add m0002_drop_advisory_status migration that drops the deprecated status column from the advisory table
- Register the new migration in migration/src/lib.rs

## Jira
Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)"
```

- **`--base TC-9005`** targets the feature branch, NOT `--base main` (per constraint 3.3: `gh pr create` MUST always specify `--base <target-branch>` matching the task's Target Branch value)
- **`--head TC-9205`** is the task branch

---

## Commit Message

The commit follows Conventional Commits format (constraint 2.2) with the Jira issue ID in the footer (constraint 2.1) and the `--trailer` flag for AI attribution (constraint 2.3):

```bash
git commit --trailer="Assisted-by: Claude Code" -m "feat(migration): drop deprecated status column from advisory table

Add m0002_drop_advisory_status migration using SeaORM's TableAlterStatement
to drop the status column. The down method re-adds the column as a nullable
string to support rollback.

Implements TC-9205"
```

Key details:
- **Type:** `feat` (new migration capability)
- **Scope:** `migration` (scoped to the migration module)
- **Footer:** `Implements TC-9205` (references the task issue ID)
- **`--trailer="Assisted-by: Claude Code"`** flag is explicitly included on the git commit command

---

## Code Inspection (Step 4 -- Understand the Code)

Before making any modifications, the following files MUST be inspected (constraint 1.5: must inspect code before modifying it):

### Files to Inspect

1. **`migration/src/m0001_initial/mod.rs`** -- Read this file to understand the existing migration pattern: how `MigrationTrait` is implemented, the structure of `up()` and `down()` methods, how SeaORM's schema management API is used. This is the sibling migration that the new migration must follow.

2. **`entity/src/advisory.rs`** -- Read this file to verify that the `advisory` entity no longer references the `status` column. This is an explicit precondition in the task's Implementation Notes ("verify this before proceeding").

3. **`migration/src/lib.rs`** -- Read this file to understand how migrations are registered (the `migrations()` function with the `vec![]` pattern), and to determine where to add the new migration module.

### Additional Inspection

4. **Sibling analysis:** Inspect `migration/src/m0001_initial/mod.rs` as the primary sibling file to understand:
   - How `MigrationTrait` is implemented (required methods: `up`, `down`, `name`)
   - The use of SeaORM schema manager API
   - Import patterns and module structure
   - Error handling in migration methods

5. **Convention conformance:** Check for a `CONVENTIONS.md` file at the repository root for project-specific coding standards, CI check commands, and code generation commands.

6. **Documentation identification:** Check for README files in the `migration/` directory and the repository root `docs/` folder for any migration-related documentation.

7. **Advisory service/module inspection:** Use Grep or Read to search across `modules/fundamental/src/advisory/` to confirm no service or endpoint code references the `status` column, validating the safety of the migration.

---

## Files to Create

### File 1: `migration/src/m0002_drop_advisory_status/mod.rs`

New migration module that drops the `status` column from the `advisory` table. See `outputs/file-1-description.md` for detailed changes.

## Files to Modify

### File 2: `migration/src/lib.rs`

Register the new migration module in the migration list. See `outputs/file-2-description.md` for detailed changes.

---

## Self-Verification Checklist (Step 9)

Before committing, the following verification steps would be performed:

1. **Scope containment:** Run `git diff --name-only` and confirm only `migration/src/m0002_drop_advisory_status/mod.rs` (created) and `migration/src/lib.rs` (modified) are changed.
2. **Untracked file check:** Run `git status --short` to check for untracked files in the `migration/` directory.
3. **Sensitive-pattern check:** Search the staged diff for secrets or credentials.
4. **Data-flow trace:** Trace the migration lifecycle: migration registration in `lib.rs` -> migration runner discovers the module -> `up()` drops the column -> `down()` re-adds it. Verify the path is complete.
5. **Contract verification:** Verify `MigrationTrait` is fully implemented (all required methods: `name()`, `up()`, `down()`).
6. **Sibling parity:** Compare the new migration against `m0001_initial` for parity on error handling, return types, and schema manager usage.
7. **Duplication check:** Search for any existing migration that already drops the `status` column.
8. **CI checks:** Run `cargo test` (or CI commands from CONVENTIONS.md if present) to verify the migration compiles and tests pass.

---

## Jira Updates (Step 11)

1. Set the Git Pull Request custom field (`customfield_10875`) on TC-9205 with the PR URL in ADF format.
2. Add a comment to TC-9205 with: PR link, summary of changes, and confirmation that all acceptance criteria are met.
3. Transition TC-9205 to **In Review**.
