# Implementation Plan for TC-9205: Add migration to drop status table column

## Target Branch Analysis

The task description specifies:
- **Target Branch**: `TC-9005`
- **Linked Issues**: is incorporated by TC-9005

This means TC-9005 is the parent feature branch. The task branch TC-9205 must be created from TC-9005, and the pull request must target TC-9005 (not `main`).

## Branch Operations

### 1. Fetch and checkout the target feature branch

```bash
git fetch origin TC-9005
git checkout TC-9005
```

### 2. Create the task branch from the feature branch

```bash
git checkout -b TC-9205
```

This creates branch `TC-9205` based on `TC-9005`. The task branch is distinct from the target branch.

## Pre-Implementation Inspection

Before making any changes, inspect existing code to understand conventions and verify assumptions:

1. **Read `migration/src/m0001_initial/mod.rs`** -- Understand the existing migration pattern: how `MigrationTrait` is implemented, naming conventions for the migration struct, how `up` and `down` methods are structured, and how SeaORM schema manager calls are used.

2. **Read `entity/src/advisory.rs`** -- Verify that the `advisory` entity no longer references the `status` column. The task description states this, but we must confirm before proceeding. Check that the `Column` enum and `Model` struct do not include a `Status` variant/field.

3. **Read `migration/src/lib.rs`** -- Understand how migrations are registered: the module declaration pattern and the `vec![]` in the `migrations()` function where new migrations are appended.

## Files to Modify

### 1. `migration/src/lib.rs`
- Add module declaration: `mod m0002_drop_advisory_status;`
- Add the new migration to the `migrations()` function's `vec![]`: `Box::new(m0002_drop_advisory_status::Migration)`

## Files to Create

### 2. `migration/src/m0002_drop_advisory_status/mod.rs`
- Implement `MigrationTrait` with:
  - `up`: Drops the `status` column from the `advisory` table using `TableAlterStatement`
  - `down`: Re-adds the `status` column as a nullable string for rollback

## Commit Message

```
feat(migration): add migration to drop advisory status column

Add m0002_drop_advisory_status migration that removes the deprecated
`status` column from the `advisory` table. The column was replaced by
the `severity` enum field and is no longer referenced by any entity or
service code.

Refs: TC-9205
```

The commit command:
```bash
git add migration/src/m0002_drop_advisory_status/mod.rs migration/src/lib.rs
git commit -m "feat(migration): add migration to drop advisory status column

Add m0002_drop_advisory_status migration that removes the deprecated
\`status\` column from the \`advisory\` table. The column was replaced by
the \`severity\` enum field and is no longer referenced by any entity or
service code.

Refs: TC-9205" --trailer='Assisted-by: Claude Code'
```

## Pull Request

Create a PR targeting the feature branch TC-9005:

```bash
gh pr create --base TC-9005 --title "feat(migration): add migration to drop advisory status column" --body "$(cat <<'EOF'
## Summary

- Adds `m0002_drop_advisory_status` migration that drops the deprecated `status` column from the `advisory` table
- Registers the new migration in `migration/src/lib.rs`
- Includes rollback (`down`) method that re-adds the column as a nullable string

## Acceptance Criteria

- [x] Migration drops the `status` column from the `advisory` table
- [x] Migration `down` method re-adds the column as nullable string for rollback
- [x] Migration is registered in `migration/src/lib.rs`
- [x] No service or entity code references the `status` column

## Test plan

- [ ] Run the migration against a test database and verify the `status` column is dropped
- [ ] Run the rollback and verify the `status` column is re-added as a nullable string
- [ ] Verify existing advisory queries still work after migration

Refs: TC-9205
EOF
)"
```

## Summary of Changes

| File | Action | Description |
|---|---|---|
| `migration/src/m0002_drop_advisory_status/mod.rs` | Create | New migration implementing `MigrationTrait` to drop the `status` column |
| `migration/src/lib.rs` | Modify | Register the new migration module and add it to the migrations list |
