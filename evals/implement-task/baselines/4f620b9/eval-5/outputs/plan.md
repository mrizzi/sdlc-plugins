# Implementation Plan for TC-9205

## Task Summary

Add a database migration that drops the deprecated `status` column from the `advisory` table. The column was replaced by the `severity` enum field in a previous migration and is no longer read or written by any service code.

## Branch Operations

1. **Checkout the target branch (feature branch TC-9005):**
   ```
   git checkout TC-9005
   git pull
   ```

2. **Create a task branch from the feature branch:**
   ```
   git checkout -b TC-9205
   ```

   The target branch is `TC-9005` (a feature branch, not `main`), so the new task branch `TC-9205` is based on `TC-9005`.

3. **After implementation, push and create PR targeting TC-9005:**
   ```
   git push -u origin TC-9205
   gh pr create --base TC-9005 --title "feat(migration): add migration to drop advisory status column" --body "## Summary
   - Add migration m0002_drop_advisory_status to drop the deprecated status column from the advisory table
   - Register the new migration in migration/src/lib.rs

   ## Jira
   Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)"
   ```

   The PR explicitly targets `--base TC-9005` since the Target Branch is a feature branch, not main.

## Commit Message

```
feat(migration): add migration to drop advisory status column

Add m0002_drop_advisory_status migration that drops the deprecated
`status` column from the `advisory` table. The `down` method re-adds
the column as a nullable string for rollback support.

Register the new migration module in migration/src/lib.rs.

Implements TC-9205
```

With trailer: `--trailer="Assisted-by: Claude Code"`

## Files to Modify

1. **`migration/src/lib.rs`** — Register the new migration module in the migration list
   - See `outputs/file-1-description.md` for detailed changes

## Files to Create

1. **`migration/src/m0002_drop_advisory_status/mod.rs`** — New migration that drops the `status` column
   - See `outputs/file-2-description.md` for detailed changes

## Pre-Implementation Verification

Before implementing, the following verifications would be performed:

1. **Verify entity code**: Confirm that `entity/src/advisory.rs` no longer references the `status` column, as stated in the implementation notes.
2. **Inspect sibling migration**: Read `migration/src/m0001_initial/mod.rs` to understand the existing migration pattern (imports, struct naming, `MigrationTrait` implementation, `up`/`down` method signatures).
3. **Inspect migration registry**: Read `migration/src/lib.rs` to understand how migrations are registered (the `vec![]` in the `migrations()` function).
4. **Check for CONVENTIONS.md**: Read `CONVENTIONS.md` at the repository root for project-specific conventions and CI check commands.
5. **Verify no service code references**: Grep across `modules/` and `common/` for any references to `status` on the advisory entity to confirm the column is truly unused.

## Post-Implementation Verification

1. **Scope containment**: Run `git diff --name-only` and verify only the two expected files are changed.
2. **Untracked file check**: Run `git status --short` to identify any untracked files in `migration/src/m0002_drop_advisory_status/`.
3. **Sensitive-pattern check**: Search staged diff for secrets or credentials.
4. **Data-flow trace**: Migration up drops column -> down re-adds column. Both directions verified complete.
5. **Contract verification**: Verify `MigrationTrait` is fully implemented (both `up` and `down` methods).
6. **Sibling parity**: Compare against `m0001_initial/mod.rs` for consistent patterns.
7. **CI checks**: Run any CI commands found in CONVENTIONS.md, or fall back to `cargo build` and `cargo test`.

## Jira Updates

1. Transition TC-9205 to "In Progress" and assign to current user.
2. After PR creation, update the Git Pull Request custom field (`customfield_10875`) with the PR URL in ADF format.
3. Add a Jira comment with the PR link and summary of changes.
4. Transition TC-9205 to "In Review".
