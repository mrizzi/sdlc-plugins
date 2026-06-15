# Implementation Plan for TC-9205: Add migration to drop status table column

## Task Summary

Add a database migration that drops the deprecated `status` column from the `advisory` table. The column was replaced by the `severity` enum field in a previous migration and is no longer referenced by any service or entity code.

## Branch Operations

### Target Branch

The task specifies **Target Branch: TC-9005**. This is a feature branch name (the parent feature issue ID), not `main`. Per the skill's branching rules:

1. **Check out the feature branch** `TC-9005` (which must already exist):
   ```
   git checkout TC-9005
   git pull
   ```
2. **Create the task branch** from the feature branch:
   ```
   git checkout -b TC-9205
   ```

This creates branch `TC-9205` based on branch `TC-9005`, not on `main`.

### PR Target

The pull request will target the **feature branch** `TC-9005` (not `main`):
```
gh pr create --base TC-9005 --head TC-9205 ...
```

This is critical -- the `--base` flag must be set to `TC-9005` because that is the Target Branch specified in the task description.

## Files to Create

| # | File Path | Description |
|---|---|---|
| 1 | `migration/src/m0002_drop_advisory_status/mod.rs` | New migration module that drops the `status` column from the `advisory` table |

## Files to Modify

| # | File Path | Description |
|---|---|---|
| 2 | `migration/src/lib.rs` | Register the new migration module `m0002_drop_advisory_status` in the migrations list |

## Pre-Implementation Verification

Before implementing, the following checks would be performed:

1. **Entity verification:** Inspect `entity/src/advisory.rs` to confirm the `status` column is no longer referenced in the entity definition. The task states it was replaced by `severity` -- verify this is the case.
2. **Service code verification:** Search all files under `modules/fundamental/src/advisory/` for any reference to `status` column or `Advisory::Status` to ensure no service code reads or writes it.
3. **Query verification:** Search `common/src/db/query.rs` and advisory-related query code for `status` references.
4. **Ingestor verification:** Search `modules/ingestor/src/graph/advisory/mod.rs` for `status` references.
5. **Sibling migration analysis:** Read `migration/src/m0001_initial/mod.rs` to understand the exact pattern for `MigrationTrait` implementation, imports, and module structure.

## Implementation Details

### File 1: `migration/src/m0002_drop_advisory_status/mod.rs` (CREATE)

A new migration module implementing `MigrationTrait` with:
- **`up` method:** Drops the `status` column from the `advisory` table using `TableAlterStatement`
- **`down` method:** Re-adds the `status` column as a nullable string to allow rollback

See `outputs/file-1-description.md` for detailed implementation.

### File 2: `migration/src/lib.rs` (MODIFY)

Register the new migration module in the migration list:
- Add `mod m0002_drop_advisory_status;` declaration
- Add the migration to the `vec![]` in the `migrations()` function, following the pattern used for `m0001_initial`

See `outputs/file-2-description.md` for detailed implementation.

## Commit Message

```
refactor(migration): drop deprecated status column from advisory table

Add migration m0002_drop_advisory_status that removes the `status` column
from the `advisory` table. The column was replaced by the `severity` enum
field in a previous migration and is no longer read or written by any
service code.

The down() method re-adds the column as a nullable string for rollback.

Implements TC-9205
```

The commit would include `--trailer="Assisted-by: Claude Code"`.

## PR Description

The PR would be created with:

```
gh pr create --base TC-9005 --head TC-9205 --title "refactor(migration): drop deprecated status column from advisory table" --body "..."
```

PR body would include:
- Summary of changes (migration creation, lib.rs registration)
- Link to Jira: `Implements [TC-9205](<webUrl>)`
- Note that this is part of the TC-9005 feature branch

## Post-Implementation Verification

1. **Scope containment:** Verify only the two expected files are modified/created
2. **Acceptance criteria check:**
   - Migration drops the `status` column -- verified by code review of `up()` method
   - Migration `down` re-adds column as nullable string -- verified by code review of `down()` method
   - Migration registered in `lib.rs` -- verified by inspecting the `migrations()` function
   - No service or entity code references `status` -- verified in pre-implementation step
3. **Test execution:** Run `cargo test` to verify migration tests pass
4. **Sensitive pattern check:** Scan diff for secrets/credentials
5. **Data-flow trace:** Migration up drops column (input: schema, processing: ALTER TABLE DROP COLUMN, output: updated schema) -- complete path
6. **Contract verification:** `MigrationTrait` requires both `up()` and `down()` -- both implemented
7. **Sibling parity:** Follows same pattern as `m0001_initial` for imports, trait implementation, and method signatures

## Jira Updates

1. **Assign** the task to the current user
2. **Transition** to In Progress at start
3. **Set Git Pull Request custom field** (`customfield_10875`) with the PR URL
4. **Add comment** with PR link, summary of changes, and no deviations from plan
5. **Transition** to In Review after PR creation
