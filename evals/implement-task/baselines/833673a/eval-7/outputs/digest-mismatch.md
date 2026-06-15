# Step 1.5 -- Description Integrity Verification: Digest Mismatch Handling

## Task

TC-9201: Add advisory severity aggregation service and endpoint

## Context

After fetching and parsing the Jira task in Step 1, Step 1.5 verifies that the task
description has not been modified since plan-feature originally created it. This
verification uses the digest protocol defined in
`shared/description-digest-protocol.md`.

## Procedure

### 1. Retrieve Issue Comments

Fetch all comments on TC-9201 using the Jira API:

```
jira.get_issue_comments("TC-9201")
```

This returns the full list of comments on the issue, each with body text, `created`
timestamp, and `updated` timestamp.

### 2. Locate the Digest Comment

Search all returned comments for those whose body starts with the marker string:

```
[sdlc-workflow] Description digest:
```

This exact marker prefix is defined in `shared/description-digest-protocol.md` and is
used by plan-feature when posting the digest after task creation.

In this scenario, one comment matches. Its full body is:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

If multiple comments had matched the marker, we would select the most recent one by
`created` timestamp to handle plan-feature re-run scenarios deterministically.

### 3. Check for Comment Editing

Compare the comment's `created` and `updated` timestamps. In this scenario, the
timestamps are identical -- the comment was not edited after initial posting. No
warning is needed.

If `updated` had been later than `created`, we would warn: "Digest comment was edited
after initial posting -- integrity cannot be fully guaranteed." We would still proceed
with the digest comparison regardless.

### 4. Parse the Stored Digest

From the comment body, extract the format-tagged digest value:

```
sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

Parse this into two components:
- **Format tag**: `sha256-md` (indicates the digest was computed from the markdown
  representation of the description)
- **Hex digest**: `0000000000000000000000000000000000000000000000000000000000000000`
  (64 hexadecimal characters -- a full SHA-256 hash)

The format tag is not `sha256:<hex>` (the legacy untagged format), so we proceed with
the full verification rather than skipping with a legacy-format warning.

### 5. Compute the Current Digest

Extract the description field from the Jira issue response (the markdown text of the
task description as returned by the API). Write it to a temporary file and compute the
digest using the project's digest script:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format. Since the description is fetched as markdown
text (via MCP), the script outputs a tagged digest in the form:

```
sha256-md:<computed-64-char-hex>
```

For example (illustrative -- the actual hash would be computed from the real
description content):

```
sha256-md:a3f7b2c1d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1
```

If the script had exited non-zero, we would warn and skip the integrity check without
blocking execution.

### 6. Compare Format Tags

Compare the format tag from the stored digest with the format tag from the computed
digest:

- **Stored tag**: `sha256-md`
- **Computed tag**: `sha256-md`

The tags match. Both the producer (plan-feature) and the consumer (implement-task)
used the same API access method (MCP, which returns markdown), so the digests are
directly comparable.

If the tags had differed (e.g., stored `sha256-adf` vs. computed `sha256-md`), we
would log a warning about different API access methods and skip the integrity check
entirely, proceeding normally.

### 7. Compare Hex Digests -- MISMATCH DETECTED

With matching format tags, compare the hex digest values:

- **Expected** (from digest comment): `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Actual** (computed from current description): `sha256-md:a3f7b2c1d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1`

The hex digests do NOT match. This means the task description was modified after
plan-feature created it.

### 8. Alert the User

Present the following alert to the user:

---

**Description integrity check: MISMATCH**

The task description for TC-9201 was modified after plan-feature created it. The
description digest recorded at planning time does not match the current description.

**Expected digest** (recorded by plan-feature):
`sha256-md:0000000000000000000000000000000000000000000000000000000000000000`

**Actual digest** (computed from current description):
`sha256-md:a3f7b2c1d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1`

This may indicate that someone manually edited the task description after planning, or
that plan-feature was re-run without updating the digest comment. The implementation
may not match the original plan.

**How would you like to proceed?**

1. **Proceed** -- implement the task using the current (modified) description as-is
2. **Stop** -- abort implementation so you can re-run plan-feature to regenerate
   tasks with a fresh plan that matches the current description

---

### 9. Stop Execution

**Execution stops here.** Do not proceed to Step 2 (Verify Dependencies), Step 3
(Transition to In Progress), or any subsequent steps. No implementation plan is
generated. No branch is created. No code changes are made.

The workflow remains paused until the user explicitly responds with their choice:

- If the user chooses **option 1 (Proceed)**: resume from Step 2 using the current
  description content, accepting that it differs from the original plan.
- If the user chooses **option 2 (Stop)**: terminate the implement-task invocation
  entirely. The user should re-run plan-feature on the parent feature to regenerate
  task descriptions, which will post a new digest comment reflecting the updated
  content. After re-planning, the user can re-invoke implement-task.

## Why This Matters

The description digest protocol guards against silent tampering between the planning
and implementation phases of the SDLC workflow. Without this check, a modified task
description could cause the implementation to diverge from the approved plan without
anyone noticing. The pause-and-ask behavior ensures a human makes the conscious
decision to either accept the modified description or re-align the plan.
