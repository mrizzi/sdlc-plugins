# Implementation Plan for TC-9205

## Task Summary

**Jira Key**: TC-9205
**Summary**: Add migration to drop status table column
**Linked Issues**: is incorporated by TC-9005

## Target Branch Extraction

The task description contains a **Target Branch** section with the value **TC-9005**. This is a feature branch (not `main`), indicating that TC-9205 is a sub-task incorporated into the TC-9005 feature branch. All branch operations and the PR must target TC-9005.

---

## Step 1: Branch Operations

```bash
# Check out the feature branch (Target Branch from task description)
git checkout TC-9005
git pull

# Create the task branch named after the Jira issue ID
git checkout -b TC-9205
```

This checks out **TC-9005** (the Target Branch) before creating the task branch **TC-9205**. The task branch is distinct from the feature branch.

---

## Step 2: Inspect Existing Code

Before making any changes, read and analyze the following files to understand existing patterns and confirm assumptions:

1. **`migration/src/m0001_initial/mod.rs`** -- Inspect the sibling migration to understand the `MigrationTrait` pattern, how `up` and `down` methods are structured, what imports are used, how the migration name is defined, and how `SeaORM` schema operations are invoked.

2. **`migration/src/lib.rs`** -- Inspect the migration registration list to understand how migrations are added to the `migrations()` function and what module declarations exist.

3. **`entity/src/advisory.rs`** -- Verify that the `advisory` entity no longer references the `status` column. Confirm that removing the column will not break any entity mapping.

4. **`modules/fundamental/src/advisory/service/advisory.rs`** -- Scan for any references to a `status` field on the advisory table to confirm no service code depends on it.

5. **`modules/fundamental/src/advisory/model/summary.rs`** -- Check that the advisory summary model does not reference `status`.

6. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- Check that the advisory endpoints do not reference `status`.

---

## Step 3: Files to Create

### File 1: `migration/src/m0002_drop_advisory_status/mod.rs`

Create a new migration module that:
- Implements `MigrationTrait` following the exact pattern found in `m0001_initial/mod.rs`
- `up` method: uses `TableAlterStatement` to drop the `status` column from the `advisory` table
- `down` method: re-adds the `status` column as a nullable string for rollback
- Defines a migration name consistent with the naming convention observed in `m0001_initial`

See `outputs/file-1-description.md` for detailed changes.

---

## Step 4: Files to Modify

### File 2: `migration/src/lib.rs`

Modify the migration registration file to:
- Add `mod m0002_drop_advisory_status;` module declaration following the pattern of `mod m0001_initial;`
- Add `Box::new(m0002_drop_advisory_status::Migration)` to the `vec![]` in the `migrations()` function, appended after the m0001_initial entry

See `outputs/file-2-description.md` for detailed changes.

---

## Step 5: Verification

Before committing, verify:
- [ ] `entity/src/advisory.rs` does not reference `status` -- confirmed during inspection
- [ ] No service or endpoint code references the `status` column
- [ ] The new migration follows the exact same pattern as `m0001_initial/mod.rs`
- [ ] The migration is properly registered in `lib.rs`
- [ ] Run `cargo check` in the migration crate to verify compilation
- [ ] If a test database is available, run the migration forward and backward

---

## Step 6: Commit

```bash
git add migration/src/m0002_drop_advisory_status/mod.rs
git add migration/src/lib.rs

git commit -m "$(cat <<'EOF'
feat(migration): add migration to drop advisory status column

Add m0002_drop_advisory_status migration that removes the deprecated
`status` column from the `advisory` table. The column was replaced by
the `severity` enum field in a prior migration and is no longer
referenced by any entity or service code.

The `down` method re-adds the column as a nullable string to support
rollback.

Ref: TC-9205
EOF
)" --trailer="Assisted-by: Claude Code"
```

---

## Step 7: Push and Open PR

```bash
git push -u origin TC-9205

gh pr create \
  --base TC-9005 \
  --title "feat(migration): drop advisory status column" \
  --body "$(cat <<'EOF'
## Summary
- Adds `m0002_drop_advisory_status` migration that drops the deprecated `status` column from the `advisory` table
- Rollback (`down`) re-adds the column as a nullable string
- Migration registered in `migration/src/lib.rs`

## Jira
TC-9205

## Test plan
- [ ] Run migration forward against test database and verify `status` column is dropped
- [ ] Run migration rollback and verify `status` column is re-added as nullable string
- [ ] Verify existing advisory queries still function after migration

Generated with Claude Code
EOF
)"
```

The PR targets **`--base TC-9005`** (the Target Branch), not `main`.

---

## Summary of Branch Flow

```
TC-9005 (feature branch / Target Branch)
  └── TC-9205 (task branch, created from TC-9005)
        └── PR targets TC-9005
```
