# Implementation Plan for TC-9205: Add migration to drop status table column

## Task Summary

Add a database migration that drops the deprecated `status` column from the `advisory`
table. The column was replaced by the `severity` enum field in a previous migration and
is no longer read or written by any service code.

## Branch Operations

1. **Checkout target branch**: `git checkout TC-9005` (the parent feature branch, as specified in the Target Branch section)
2. **Pull latest**: `git pull`
3. **Create task branch**: `git checkout -b TC-9205`
4. After implementation, **push and create PR**: `git push -u origin TC-9205`
5. **Create PR targeting TC-9005**: `gh pr create --base TC-9005 --title "feat(migration): add migration to drop advisory status column" --body "..."`

The PR targets branch `TC-9005` (the feature branch), NOT `main`, because the task's Target Branch is `TC-9005`.

## Files to Modify

1. **`migration/src/lib.rs`** — Register the new migration module `m0002_drop_advisory_status` in the migration list by adding it to the `vec![]` in the `migrations()` function.

## Files to Create

1. **`migration/src/m0002_drop_advisory_status/mod.rs`** — New migration implementing `MigrationTrait` with:
   - `up` method: drops the `status` column from the `advisory` table using `TableAlterStatement`
   - `down` method: re-adds the column as a nullable string (`ColumnDef::new(Advisory::Status).string().null()`) for rollback

## Pre-Implementation Verification

Before writing any code:
- Inspect `entity/src/advisory.rs` to verify the `status` column is no longer referenced in the entity definition (per task's implementation notes)
- Inspect `migration/src/m0001_initial/mod.rs` to understand the existing migration pattern (struct definition, `MigrationTrait` implementation, `up`/`down` methods)
- Inspect `migration/src/lib.rs` to understand how migrations are registered (the `vec![]` in the `migrations()` function)
- Check `CONVENTIONS.md` at the repository root for project-level conventions and CI check commands
- Grep across `modules/` and `entity/` for any remaining references to the `status` column on the `advisory` table to confirm safe removal

## Commit Message

```
feat(migration): add migration to drop advisory status column

Add m0002_drop_advisory_status migration that drops the deprecated
`status` column from the `advisory` table. The column was replaced
by the `severity` enum field and is no longer referenced by any
service or entity code.

The down method re-adds the column as a nullable string to support
rollback.

Implements TC-9205
```

With `--trailer="Assisted-by: Claude Code"`.

## PR Description

```
## Summary

Add database migration `m0002_drop_advisory_status` that drops the deprecated `status`
column from the `advisory` table. The column was replaced by the `severity` enum field
in a previous migration and is no longer read or written by any service code. Removing
it reduces confusion and prevents accidental usage.

### Changes
- Created `migration/src/m0002_drop_advisory_status/mod.rs` with `up` (drop column) and `down` (re-add as nullable string) methods
- Registered the new migration in `migration/src/lib.rs`

Implements [TC-9205](<jira-web-url>)
```

## Self-Verification Checklist

- [ ] Scope containment: only `migration/src/lib.rs` modified and `migration/src/m0002_drop_advisory_status/mod.rs` created
- [ ] No references to `status` column remain in entity or service code
- [ ] Migration `up` drops the column
- [ ] Migration `down` re-adds the column as nullable string
- [ ] Migration registered in `lib.rs`
- [ ] No sensitive patterns in diff
- [ ] CI checks pass (cargo build, cargo test, cargo clippy if configured)
- [ ] Data-flow trace: migration up drops column -> down re-adds it (complete lifecycle)

## Jira Updates

1. Transition TC-9205 to **In Progress** at start
2. Assign to current user
3. After PR creation:
   - Set Git Pull Request custom field (`customfield_10875`) to the PR URL (in ADF format)
   - Add comment with PR link and summary of changes
   - Transition TC-9205 to **In Review**
