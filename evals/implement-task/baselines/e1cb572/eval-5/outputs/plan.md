# Implementation Plan for TC-9205: Add migration to drop status table column

## Task Summary

**Jira Issue**: TC-9205
**Summary**: Add a database migration that drops the deprecated `status` column from the `advisory` table.
**Repository**: trustify-backend
**Target Branch**: TC-9005 (feature branch, NOT main)
**Linked Issues**: is incorporated by TC-9005
**Dependencies**: None

## Branch Operations

### 1. Check out the feature branch (TC-9005) and create the task branch

The task specifies **Target Branch: TC-9005**, which is a feature branch. The task branch must be created from TC-9005, not from main.

```bash
git checkout TC-9005
git pull
git checkout -b TC-9205
```

**Critical**: The task branch is named `TC-9205` (the task issue ID), not `TC-9005` (the feature issue ID).

### 2. Push and create PR targeting TC-9005

After implementation, push and create a PR that targets the feature branch:

```bash
git push -u origin TC-9205
gh pr create --base TC-9005 --title "feat(migration): add migration to drop advisory status column" --body "..."
```

**Critical**: The PR must use `--base TC-9005`, NOT `--base main`. The target branch for the PR is the feature branch TC-9005.

## Files to Modify

1. **`migration/src/lib.rs`** -- Register the new migration module in the migration list

## Files to Create

1. **`migration/src/m0002_drop_advisory_status/mod.rs`** -- Migration that drops the `status` column from the `advisory` table

## Pre-Implementation Verification

Before making changes, verify:

1. **Entity check**: Read `entity/src/advisory.rs` to confirm the `status` column is no longer referenced in the entity definition (the task states the `advisory` entity no longer references it).
2. **Service code check**: Search `modules/fundamental/src/advisory/` for any references to `status` column to confirm it is not read or written by service code.
3. **Existing migration pattern**: Read `migration/src/m0001_initial/mod.rs` to understand the migration pattern (implements `MigrationTrait` with `up` and `down` methods).
4. **Migration registration pattern**: Read `migration/src/lib.rs` to understand how migrations are registered (added to the `vec![]` in the `migrations()` function).
5. **CONVENTIONS.md**: Read `CONVENTIONS.md` at the repository root to check for project-level conventions and CI check commands.

## Detailed Changes

### File 1: `migration/src/m0002_drop_advisory_status/mod.rs` (CREATE)

Create a new migration module that:
- Implements `MigrationTrait` with `up` and `down` methods
- `up` method: uses `TableAlterStatement` to drop the `status` column from the `advisory` table
- `down` method: re-adds the column as `ColumnDef::new(Advisory::Status).string().null()` for rollback
- Follows the exact pattern from `m0001_initial/mod.rs`

### File 2: `migration/src/lib.rs` (MODIFY)

- Add `mod m0002_drop_advisory_status;` declaration
- Add the new migration to the `vec![]` in the `migrations()` function, following the pattern of `m0001_initial`

## Commit Message

```
feat(migration): drop deprecated status column from advisory table

Add migration m0002_drop_advisory_status that removes the unused status
column from the advisory table. The column was replaced by the severity
enum field in a previous migration and is no longer referenced by any
entity or service code. The down method re-adds the column as a nullable
string for rollback support.

Implements TC-9205
```

The commit command:

```bash
git commit --trailer='Assisted-by: Claude Code' -m "feat(migration): drop deprecated status column from advisory table

Add migration m0002_drop_advisory_status that removes the unused status
column from the advisory table. The column was replaced by the severity
enum field in a previous migration and is no longer referenced by any
entity or service code. The down method re-adds the column as a nullable
string for rollback support.

Implements TC-9205"
```

## PR Details

**PR Title**: `feat(migration): drop deprecated status column from advisory table`

**PR Base**: `TC-9005` (the feature branch)

**PR Description**:
```
## Summary

- Adds migration `m0002_drop_advisory_status` to drop the deprecated `status` column from the `advisory` table
- Registers the migration in `migration/src/lib.rs`
- Includes rollback support (re-adds column as nullable string)

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)
```

**PR Command**:
```bash
gh pr create --base TC-9005 --title "feat(migration): drop deprecated status column from advisory table" --body "## Summary

- Adds migration \`m0002_drop_advisory_status\` to drop the deprecated \`status\` column from the \`advisory\` table
- Registers the migration in \`migration/src/lib.rs\`
- Includes rollback support (re-adds column as nullable string)

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)"
```

## Post-Implementation

### Jira Updates
1. Update Git Pull Request custom field (`customfield_10875`) with the PR URL (in ADF format with inlineCard)
2. Add a comment to TC-9205 with PR link, summary of changes, and any deviations
3. Transition TC-9205 to **In Review**

### Acceptance Criteria Verification
- [ ] Migration drops the `status` column from the `advisory` table -- verified by `up` method implementation
- [ ] Migration `down` method re-adds the column as nullable string for rollback -- verified by `down` method implementation
- [ ] Migration is registered in `migration/src/lib.rs` -- verified by module registration
- [ ] No service or entity code references the `status` column -- verified during pre-implementation check

### Test Verification
- Run `cargo test` to verify migrations compile and pass
- Test migration runs against test database
- Test rollback re-adds the column
- Verify existing advisory queries still work
