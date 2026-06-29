# Implementation Plan for TC-9205

## Task Summary

**Key**: TC-9205
**Summary**: Add migration to drop status table column
**Target Branch**: TC-9005 (feature branch)
**Repository**: trustify-backend

## Target Branch Identification

The task description contains a **Target Branch** section with value `TC-9005`. This is a feature branch (not `main`), indicating feature-branch workflow. All branch operations and PR targeting must use TC-9005 as the base.

## Pre-Implementation: Code Inspection

Before writing any code, inspect the following existing files to understand current patterns and verify assumptions from the task description:

1. **Read `migration/src/m0001_initial/mod.rs`** -- Understand the existing migration pattern: how `MigrationTrait` is implemented, what `up` and `down` methods look like, how `TableAlterStatement` and column operations are structured. This is the sibling migration that the new migration must follow.

2. **Read `entity/src/advisory.rs`** -- Verify that the `Advisory` entity no longer references the `status` column. The task description states this, but it must be confirmed before proceeding. If the entity still references `status`, stop and report the discrepancy.

3. **Read `migration/src/lib.rs`** -- Understand how migrations are registered (the `vec![]` in the `migrations()` function) and where the new migration module should be added.

Additionally, use Grep/Serena to search the entire codebase for any remaining references to `Advisory::Status` or the `status` column on the `advisory` table to ensure no service code depends on it.

## Branch Operations

### 1. Check out the target branch (TC-9005)

```bash
git checkout TC-9005
git pull
```

This checks out the **feature branch** TC-9005 (the Target Branch from the task description), NOT `main`.

### 2. Create task branch (TC-9205)

```bash
git checkout -b TC-9205
```

The task branch is named `TC-9205` (the task's Jira issue ID), which is distinct from `TC-9005` (the feature branch / Target Branch).

## Files to Create

### 1. `migration/src/m0002_drop_advisory_status/mod.rs`

A new SeaORM migration module that:
- Implements `MigrationTrait` following the pattern from `m0001_initial/mod.rs`
- `up` method: drops the `status` column from the `advisory` table using `TableAlterStatement`
- `down` method: re-adds the `status` column as a nullable string (`ColumnDef::new(Advisory::Status).string().null()`) for rollback support

See `file-1-description.md` for detailed implementation.

## Files to Modify

### 1. `migration/src/lib.rs`

Register the new migration module `m0002_drop_advisory_status` in the migration list:
- Add `mod m0002_drop_advisory_status;` declaration
- Add the migration to the `vec![]` in the `migrations()` function, following the pattern of `m0001_initial`

See `file-2-description.md` for detailed changes.

## Tests

Tests would be implemented as described in the Test Requirements section:
- Test that the migration runs successfully against a test database
- Test that the rollback (down) re-adds the column
- Verify that existing advisory queries still work after the column is dropped

These would likely be added to `tests/api/advisory.rs` or a dedicated migration test file, following the project's existing test conventions (integration tests against a real PostgreSQL test database using `assert_eq!(resp.status(), StatusCode::OK)` pattern).

See `file-3-description.md` for detailed test plan.

## Commit Message

```
feat(migration): drop deprecated status column from advisory table

Add migration m0002_drop_advisory_status that removes the unused status
column from the advisory table. The column was previously replaced by the
severity enum field and is no longer referenced by any service or entity
code. The down method re-adds the column as a nullable string for
rollback support.

Implements TC-9205
```

The commit command:

```bash
git add migration/src/m0002_drop_advisory_status/mod.rs migration/src/lib.rs
git commit --trailer='Assisted-by: Claude Code' -m "feat(migration): drop deprecated status column from advisory table

Add migration m0002_drop_advisory_status that removes the unused status
column from the advisory table. The column was previously replaced by the
severity enum field and is no longer referenced by any service or entity
code. The down method re-adds the column as a nullable string for
rollback support.

Implements TC-9205"
```

## Push and Pull Request

```bash
git push -u origin TC-9205
```

Open a PR targeting the feature branch TC-9005 (not main):

```bash
gh pr create --base TC-9005 --title "feat(migration): drop deprecated status column from advisory table" --body "## Summary
- Add migration m0002_drop_advisory_status to drop the deprecated \`status\` column from the \`advisory\` table
- Register the new migration in migration/src/lib.rs
- The \`down\` method re-adds the column as a nullable string for rollback support

## Jira
Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)"
```

Key points:
- `--base TC-9005` ensures the PR targets the feature branch, not `main`
- The PR description follows the conventions-spec format with Summary and Jira sections
- The Jira link is a clickable Markdown link

## Jira Updates

1. Update custom field `customfield_10875` with the PR URL (in ADF format with inlineCard)
2. Add a comment summarizing the changes and linking to the PR
3. Transition TC-9205 to "In Review"

## Self-Verification Checklist

Before committing, the following checks would be performed:

- **Scope containment**: `git diff --name-only` should only show `migration/src/m0002_drop_advisory_status/mod.rs` and `migration/src/lib.rs`
- **Untracked file check**: verify no untracked files in migration directories need staging
- **Sensitive-pattern check**: scan staged diff for secrets/credentials
- **Codebase search**: grep for any remaining references to `Advisory::Status` or `status` column in advisory-related code
- **Data-flow trace**: verify the migration is registered and will be picked up by the migration runner
- **Convention conformance**: ensure the new migration follows the same structure as `m0001_initial`
- **CI checks**: run any CI check commands from CONVENTIONS.md (if present), including `cargo build`, `cargo test`, `cargo clippy`, `cargo fmt --check`
