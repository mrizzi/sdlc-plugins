# Implementation Plan for TC-9205: Add migration to drop status table column

## Task Summary

Add a database migration that drops the deprecated `status` column from the `advisory` table. The column was replaced by the `severity` enum field in a previous migration and is no longer read or written by any service code.

## Branch Operations

### Checkout and Branch Creation

1. **Checkout the target branch** (TC-9005, NOT main):
   ```
   git checkout TC-9005
   git pull
   ```

2. **Create the task branch** named after the Jira issue ID:
   ```
   git checkout -b TC-9205
   ```

The target branch is `TC-9005` because this task is part of a feature branch workflow -- the task description specifies `Target Branch: TC-9005` and the linked issue shows "is incorporated by TC-9005".

### Commit Message

```
feat(migration): add migration to drop advisory status column

Add m0002_drop_advisory_status migration that removes the deprecated
status column from the advisory table. The column was replaced by the
severity enum field and is no longer referenced by any service or
entity code.

Implements TC-9205
```

With flag: `--trailer="Assisted-by: Claude Code"`

Full command:
```
git commit --trailer="Assisted-by: Claude Code" -m "feat(migration): add migration to drop advisory status column

Add m0002_drop_advisory_status migration that removes the deprecated
status column from the advisory table. The column was replaced by the
severity enum field and is no longer referenced by any service or
entity code.

Implements TC-9205"
```

### Push and PR Creation

```
git push -u origin TC-9205
```

Create PR targeting the feature branch TC-9005 (NOT main):
```
gh pr create --base TC-9005 --title "feat(migration): add migration to drop advisory status column" --body "## Summary

Add database migration m0002_drop_advisory_status that drops the deprecated \`status\` column from the \`advisory\` table. The column was replaced by the \`severity\` enum field in a previous migration and is no longer read or written by any service code.

### Changes
- Created \`migration/src/m0002_drop_advisory_status/mod.rs\` with up (drop column) and down (re-add as nullable string) methods
- Registered the new migration module in \`migration/src/lib.rs\`

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)"
```

## Pre-Implementation Verification

Before implementing, verify:
1. Confirm that `entity/src/advisory.rs` does NOT reference a `status` column (the task states it was already removed from the entity definition).
2. Grep the codebase for any remaining references to `Advisory::Status` or `advisory.status` to confirm no service code depends on it.
3. Read `migration/src/m0001_initial/mod.rs` to understand the existing migration pattern.
4. Read `migration/src/lib.rs` to understand how migrations are registered.
5. Check for `CONVENTIONS.md` at the repository root and follow any conventions found.

## Files to Create

| # | File | Description |
|---|------|-------------|
| 1 | `migration/src/m0002_drop_advisory_status/mod.rs` | New migration module that drops the `status` column from the `advisory` table |

## Files to Modify

| # | File | Description |
|---|------|-------------|
| 2 | `migration/src/lib.rs` | Register the new migration module in the migration list |

## Detailed Changes

See `file-1-description.md` and `file-2-description.md` for detailed change descriptions.
