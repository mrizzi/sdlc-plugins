# Implementation Plan: TC-9205 — Add migration to drop status table column

## Target Branch Analysis

The task description contains a **Target Branch** section with value **TC-9005**. This is a feature branch (not `main`), indicating this task is part of a feature-branch workflow. The task is linked as "is incorporated by TC-9005", confirming TC-9005 is the parent feature issue whose branch collects all intermediate task PRs.

All branch operations must account for this: the task branch is created from TC-9005, and the PR targets TC-9005.

---

## Branch Operations

### Step 1: Check out the Target Branch (TC-9005)

```bash
git checkout TC-9005
git pull
```

This checks out the feature branch TC-9005 as the base for the new task branch, per the Target Branch section in the task description (constraint 3.1, Step 5 of SKILL.md).

### Step 2: Create the task branch (TC-9205)

```bash
git checkout -b TC-9205
```

The task branch is named after the task issue ID **TC-9205** (not TC-9005, which is the feature branch). This follows constraint 3.1: "The feature branch MUST be named after the Jira issue ID."

---

## Code Inspection (Step 4 — Understand the Code)

Before making any changes, inspect the following files to understand existing patterns and verify assumptions (constraint 1.5, 5.2):

1. **Read `migration/src/m0001_initial/mod.rs`** — Inspect the existing migration to understand the pattern for implementing `MigrationTrait`, including `up()` and `down()` methods, the use of `TableAlterStatement`, `ColumnDef`, and how the `Advisory` entity enum variants are used in migrations.

2. **Read `entity/src/advisory.rs`** — Verify that the `Advisory` entity no longer references the `status` column. This is an explicit acceptance criterion: "No service or entity code references the status column." Must confirm before proceeding.

3. **Read `migration/src/lib.rs`** — Understand how migrations are registered in the `migrations()` function. Inspect the `vec![]` to see the pattern for adding new migration modules and the import convention for migration modules.

Additionally, search for any remaining references to the `status` column across the codebase:
```bash
grep -r "status" entity/src/ --include="*.rs"
grep -r "Status" migration/src/ --include="*.rs"
```

### Convention Conformance Analysis

Identify sibling files to `m0001_initial/mod.rs` in `migration/src/` to discover conventions for:
- Module naming (e.g., `m0001_initial`, `m0002_*` prefix pattern)
- Import and re-export patterns in `lib.rs`
- SeaORM migration trait implementation structure
- Column definition patterns (types, nullability)

---

## Files to Create

### File 1: `migration/src/m0002_drop_advisory_status/mod.rs`

New migration module that drops the deprecated `status` column from the `advisory` table.

- Implement `MigrationTrait` with:
  - `up()` method: uses `manager.alter_table(Table::alter().table(Advisory::Table).drop_column(Advisory::Status).to_owned()).await` to drop the column
  - `down()` method: re-adds the column as `ColumnDef::new(Advisory::Status).string().null()` to allow rollback
- Follow the exact pattern found in `migration/src/m0001_initial/mod.rs`
- Include proper `use` statements for SeaORM types

See `outputs/file-1-description.md` for detailed changes.

---

## Files to Modify

### File 2: `migration/src/lib.rs`

Register the new migration module in the migration list.

- Add `mod m0002_drop_advisory_status;` import alongside existing migration module imports
- Add `Box::new(m0002_drop_advisory_status::Migration)` to the `vec![]` in the `migrations()` function, following the pattern of the `m0001_initial` entry

See `outputs/file-2-description.md` for detailed changes.

---

## Commit

After implementation and testing, commit with:

```bash
git add migration/src/m0002_drop_advisory_status/mod.rs migration/src/lib.rs
git commit --trailer='Assisted-by: Claude Code' -m "feat(migration): add migration to drop advisory status column

Add m0002_drop_advisory_status migration that removes the deprecated
status column from the advisory table. The column was replaced by the
severity enum field and is no longer referenced by any entity or
service code.

The down() method re-adds the column as a nullable string to support
rollback.

Implements TC-9205"
```

Key commit conventions:
- Conventional Commits format: `feat(migration): ...` (type with scope)
- Jira issue ID TC-9205 referenced in the footer
- `--trailer='Assisted-by: Claude Code'` included (constraint 2.3)

---

## Push and PR

```bash
git push -u origin TC-9205
gh pr create --base TC-9005 --title "feat(migration): add migration to drop advisory status column" --body "## Summary
- Add m0002_drop_advisory_status migration to drop the deprecated status column from the advisory table
- Register the new migration in migration/src/lib.rs
- Down method re-adds column as nullable string for rollback support

## Jira
Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)"
```

The PR targets **TC-9005** (`--base TC-9005`), the feature branch, not `main`. This follows constraint 3.3: "gh pr create MUST always specify --base <target-branch> matching the task's Target Branch value."

---

## Jira Updates

1. Update the Git Pull Request custom field (`customfield_10875`) with the PR URL in ADF format
2. Add a comment to TC-9205 with the PR link and summary of changes
3. Transition TC-9205 to "In Review"

---

## Verification Checklist

- [ ] Migration drops the status column from the advisory table (up method)
- [ ] Migration down method re-adds the column as nullable string for rollback
- [ ] Migration is registered in `migration/src/lib.rs`
- [ ] No service or entity code references the status column (verified by inspecting `entity/src/advisory.rs`)
- [ ] Tests pass: migration runs successfully, rollback re-adds column, existing queries unaffected
