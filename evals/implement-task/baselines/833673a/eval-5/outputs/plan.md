# Implementation Plan for TC-9205: Add migration to drop status table column

## Task Summary

Add a database migration that drops the deprecated `status` column from the `advisory`
table. The column was replaced by the `severity` enum field in a previous migration and
is no longer read or written by any service code.

## Target Branch

**TC-9005** (feature branch, NOT main)

## Branch Operations

1. **Check out the target branch (feature branch):**
   ```
   git checkout TC-9005
   git pull
   ```

2. **Create the task branch from the feature branch:**
   ```
   git checkout -b TC-9205
   ```

3. **After implementation, push and open PR targeting the feature branch:**
   ```
   git push -u origin TC-9205
   gh pr create --base TC-9005 --title "feat(migration): add migration to drop advisory status column" --body "..."
   ```
   The PR MUST use `--base TC-9005` to target the feature branch, NOT main.

## Pre-Implementation Verification (Step 4)

Before modifying any files, inspect the following using Serena (`mcp__serena_backend__<tool>`)
or Read/Grep as fallback:

1. **Inspect `migration/src/m0001_initial/mod.rs`** — use `get_symbols_overview` to understand
   the existing migration structure (MigrationTrait implementation, `up`/`down` method
   signatures, import patterns).
2. **Inspect `migration/src/lib.rs`** — use `get_symbols_overview` to see how migrations are
   registered (module declaration, `migrations()` function, Vec construction).
3. **Inspect `entity/src/advisory.rs`** — use `find_symbol` to confirm that the `status`
   column is NOT referenced in the current entity definition (verifying it was already
   removed when `severity` was introduced).
4. **Search for `status` references** — use `search_for_pattern` or Grep across the codebase
   to confirm no service or entity code references `Advisory::Status` or the `status` column.
5. **Identify sibling files** — examine `m0001_initial/mod.rs` as the sibling migration to
   discover conventions (import patterns, trait implementation structure, error handling).
6. **Check for CONVENTIONS.md** at the repository root and extract any CI check commands.
7. **Identify documentation files** — check for README files in `migration/` and root-level
   architecture docs that may reference database schema.

## Files to Create

### 1. `migration/src/m0002_drop_advisory_status/mod.rs`
New migration module that drops the `status` column from the `advisory` table.

### Files to Modify

### 2. `migration/src/lib.rs`
Register the new migration module in the migration list.

## Commit Message

```
feat(migration): drop deprecated status column from advisory table

Add migration m0002_drop_advisory_status that removes the `status` column
from the `advisory` table. The column was replaced by the `severity` enum
field and is no longer referenced by any service or entity code.

The `down` method re-adds the column as a nullable string to support rollback.

Implements TC-9205
```

With the flag: `--trailer="Assisted-by: Claude Code"`

## PR Details

- **Base branch:** TC-9005 (the feature branch, NOT main)
- **Head branch:** TC-9205 (the task branch)
- **Title:** `feat(migration): drop deprecated status column from advisory table`
- **Description:**
  ```
  ## Summary
  - Add migration `m0002_drop_advisory_status` that drops the deprecated `status` column from the `advisory` table
  - Register the new migration in `migration/src/lib.rs`
  - The `down` method re-adds the column as a nullable string to support rollback

  Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)
  ```

## Self-Verification Checklist

1. **Scope containment:** Only `migration/src/lib.rs` (modified) and
   `migration/src/m0002_drop_advisory_status/mod.rs` (created) should appear in `git diff --name-only`.
2. **Acceptance criteria:**
   - Migration drops `status` column from `advisory` table
   - Migration `down` re-adds column as nullable string
   - Migration registered in `lib.rs`
   - No service or entity code references `status` column (verified in Step 4)
3. **Sensitive pattern check:** Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'`
4. **Duplication check:** Search for existing drop-column migrations to confirm no overlap.
5. **Data-flow trace:** Migration up -> drops column; Migration down -> re-adds column. Both paths complete.
6. **Contract verification:** `MigrationTrait` requires `up` and `down` methods — both implemented.
7. **CI checks:** Run any commands from CONVENTIONS.md; fallback to `cargo test` and `cargo check`.

## Jira Updates

1. **Transition to In Progress** at start of implementation.
2. **Set Git Pull Request custom field** (`customfield_10875`) with PR URL in ADF format.
3. **Add comment** with PR link, summary of changes, and any deviations.
4. **Transition to In Review** after PR is created.
