# Implementation Plan for TC-9205: Add migration to drop status table column

## Task Summary

**Jira Issue:** TC-9205
**Summary:** Add a database migration that drops the deprecated `status` column from the `advisory` table.
**Repository:** trustify-backend
**Target Branch:** TC-9005
**Linked Issues:** is incorporated by TC-9005
**Dependencies:** None

## Target Branch Handling

The task specifies **Target Branch: TC-9005**, which is a feature branch (not `main`). This means:

1. **Checkout the target branch first:** `git checkout TC-9005 && git pull` to get the latest state of the feature branch.
2. **Create the task branch from TC-9005:** `git checkout -b TC-9205` — the new branch is named after this task's Jira issue ID (TC-9205), NOT the parent feature branch (TC-9005).
3. **PR targets TC-9005:** When opening the PR, use `--base TC-9005` to ensure the PR merges into the feature branch, not `main`.

## Branch Operations

```bash
# Step 1: Check out the target branch (TC-9005, the feature branch)
git checkout TC-9005
git pull

# Step 2: Create the task branch named after THIS task (TC-9205)
git checkout -b TC-9205
```

## Code Inspection (Step 4)

Before making any changes, inspect the existing code to understand current patterns and verify assumptions:

1. **Inspect `migration/src/lib.rs`** — Understand how migrations are registered. Use Serena (`mcp__serena_backend__get_symbols_overview`) to see the file structure, then `mcp__serena_backend__find_symbol` to read the `migrations()` function body.

2. **Inspect `migration/src/m0001_initial/mod.rs`** — This is the sibling migration file. Read it to understand the migration pattern: how `MigrationTrait` is implemented, what `up` and `down` methods look like, what imports are used.

3. **Inspect `entity/src/advisory.rs`** — Verify that the `Advisory` entity no longer references the `status` column. Use `mcp__serena_backend__get_symbols_overview` to check the entity definition, and `mcp__serena_backend__find_symbol` with `include_body=true` on the entity struct to confirm `status` is absent.

4. **Check `CONVENTIONS.md`** — Read `./CONVENTIONS.md` at the repository root for any project-level conventions and CI check commands.

5. **Search for `status` column references** — Use `mcp__serena_backend__search_for_pattern` (or Grep) to search for any remaining references to `Advisory::Status` or the `status` column in service or entity code to confirm it is safe to drop.

## Files to Modify

### 1. `migration/src/lib.rs`
- **Change:** Register the new migration module `m0002_drop_advisory_status` in the migration list.
- **Details:** Add `mod m0002_drop_advisory_status;` declaration, then add `Box::new(m0002_drop_advisory_status::Migration)` to the `vec![]` in the `migrations()` function, following the pattern of `m0001_initial`.

## Files to Create

### 1. `migration/src/m0002_drop_advisory_status/mod.rs`
- **Change:** Create a new migration that drops the `status` column from the `advisory` table.
- **Details:** Implement `MigrationTrait` with:
  - `up` method: drops the `status` column using `manager.alter_table(Table::alter().table(Advisory::Table).drop_column(Advisory::Status).to_owned()).await`
  - `down` method: re-adds the column as `ColumnDef::new(Advisory::Status).string().null()` to allow rollback
- **Pattern:** Follow the existing pattern in `migration/src/m0001_initial/mod.rs`

## Commit Message

```
feat(migration): drop deprecated status column from advisory table

Add migration m0002_drop_advisory_status that removes the deprecated
`status` column from the `advisory` table. The column was replaced by
the `severity` enum field in a previous migration and is no longer
referenced by any service or entity code.

The down method re-adds the column as a nullable string for rollback.

Implements TC-9205
```

The commit command would include the Assisted-by trailer:

```bash
git commit --trailer="Assisted-by: Claude Code" -m "feat(migration): drop deprecated status column from advisory table

Add migration m0002_drop_advisory_status that removes the deprecated
\`status\` column from the \`advisory\` table. The column was replaced by
the \`severity\` enum field in a previous migration and is no longer
referenced by any service or entity code.

The down method re-adds the column as a nullable string for rollback.

Implements TC-9205"
```

## Push and PR Creation

```bash
# Push the task branch
git push -u origin TC-9205

# Create PR targeting the feature branch TC-9005 (NOT main)
gh pr create --base TC-9005 --title "feat(migration): drop deprecated status column from advisory table" --body "## Summary

- Add migration \`m0002_drop_advisory_status\` that drops the deprecated \`status\` column from the \`advisory\` table
- The column was replaced by the \`severity\` enum field and is no longer referenced by any service or entity code
- Include rollback support: \`down\` method re-adds the column as a nullable string

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)"
```

Key points:
- **Branch name is TC-9205** (this task's ID), not TC-9005 (the parent feature branch)
- **PR base is TC-9005** (the target branch from the task description), not main
- **Checkout TC-9005 first** before creating the TC-9205 branch

## Jira Updates (Step 11)

1. Update the Git Pull Request custom field (`customfield_10875`) with the PR URL in ADF format.
2. Add a comment summarizing the changes made with the plugin footnote.
3. Transition TC-9205 to "In Review".

## Verification Steps

1. Verify `entity/src/advisory.rs` does not reference `status` column
2. Run `cargo test` to ensure migration compiles and existing tests pass
3. Verify acceptance criteria:
   - Migration drops the `status` column from the `advisory` table
   - Migration `down` method re-adds the column as nullable string for rollback
   - Migration is registered in `migration/src/lib.rs`
   - No service or entity code references the `status` column
4. Run scope containment check (`git diff --name-only`) against Files to Modify/Create
5. Run sensitive-pattern check on staged diff
