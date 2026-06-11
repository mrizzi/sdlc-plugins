# Step 1.5 -- Verify Description Integrity: Digest Mismatch Handling

## Context

Task: TC-9201 -- Add advisory severity aggregation service and endpoint
Repository: trustify-backend
Target Branch: main

## Step 1.5 Procedure

### 1. Retrieve Issue Comments

Fetch all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the Digest Comment

Search all returned comments for those whose body starts with the marker string `[sdlc-workflow] Description digest:`.

In this case, one comment is found with body:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

Since only one comment matches the marker, it is selected as the digest comment. (If multiple matched, I would select the most recent by `created` timestamp.)

### 3. Comment Edit Detection

Compare the comment's `created` and `updated` timestamps. In this scenario, the created and updated timestamps are identical, meaning the comment has NOT been edited after initial posting. This is the expected, clean state -- no warning is needed about comment editing. Proceed to digest comparison.

### 4. Extract the Stored Digest

Parse the tagged digest value from the comment body:

- **Full tagged value**: `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Format tag**: `sha256-md` (indicates the description was hashed as markdown text)
- **Hex digest**: `0000000000000000000000000000000000000000000000000000000000000000`

This is NOT a legacy untagged format (`sha256:<hex>`) -- it uses the format-tagged convention (`sha256-md:<hex>`), so we proceed with full verification rather than skipping with a legacy warning.

### 5. Compute the Current Digest

Extract the description field from the TC-9201 issue response (the markdown text of the task description), write it to a temporary file, and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format. Since the description was fetched as markdown text (via MCP or equivalent), the script outputs a tagged digest in the form:

```
sha256-md:<64-char-hex>
```

For this scenario, assume the script exits zero and outputs a digest such as:

```
sha256-md:abc123...def456  (a different 64-character hex value)
```

### 6. Compare Format Tags

- **Stored tag**: `sha256-md`
- **Computed tag**: `sha256-md`

The format tags MATCH. Both the producer (plan-feature) and consumer (implement-task) used the same API access method (both markdown). This means the hex digests are directly comparable.

If the tags had differed (e.g., stored was `sha256-adf` but computed was `sha256-md`), I would log a warning about the format mismatch and skip the integrity check, proceeding normally. But in this case, tags match, so I proceed to hex digest comparison.

### 7. Compare Hex Digests -- MISMATCH DETECTED

- **Expected digest** (from the comment): `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Actual digest** (computed from current description): `sha256-md:<different-64-char-hex>`

The hex digests do NOT match. This means the task description was modified after plan-feature originally created it. The description content has changed between the planning phase and the implementation phase.

### 8. Alert the User and Stop Execution

I would present the following alert to the user:

---

**Warning: Task description integrity check failed.**

The description for TC-9201 has been modified since plan-feature created it. The description digest recorded at planning time does not match the current description.

- **Expected digest** (recorded by plan-feature): `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Actual digest** (computed from current description): `sha256-md:<computed-hex-value>`

The format tags match (`sha256-md`), confirming both digests used the same representation (markdown), so this is a genuine content change -- not a cross-format artifact.

The digest comment was not edited after posting (created and updated timestamps are identical), so the stored digest is trustworthy.

**How would you like to proceed?**

1. **Proceed** -- Continue implementing with the current (modified) description as-is
2. **Stop** -- Abort implementation so you can re-run plan-feature to regenerate tasks with the updated description

---

**Execution is halted immediately.** I would NOT proceed with any subsequent steps (Step 2 dependency verification, Step 3 transition to In Progress, Step 4 code understanding, Step 5 branch creation, Step 6 implementation, etc.) until the user explicitly responds with their choice.

## Rationale

The digest mismatch protocol exists to guard against silent tampering between the planning and implementation phases. When plan-feature creates a task, it records a SHA-256 digest of the description. If someone (human or automated process) later modifies the description -- changing requirements, adding files, altering acceptance criteria -- implement-task would otherwise silently implement the modified version without awareness that the plan has drifted.

By detecting the mismatch and stopping, the protocol ensures:

1. **The user is aware** that the description they are about to implement differs from what was originally planned.
2. **The user can make an informed decision** -- either accept the modifications and proceed, or go back to plan-feature to regenerate a consistent plan.
3. **No implementation work is wasted** on a potentially inconsistent or unauthorized set of requirements.

## Key Details of This Scenario

- **Format tags match** (`sha256-md` == `sha256-md`): This confirms the comparison is valid -- both the producer and consumer used the same Jira access method (markdown), so different hex values genuinely indicate content change rather than a cross-format representation difference.
- **Comment was not edited** (created == updated): The stored digest is trustworthy -- no one tampered with the digest comment itself to make it match a modified description. This rules out the scenario where an attacker modified both the description and the digest comment.
- **Not a legacy format**: The digest uses the format-tagged convention (`sha256-md:` prefix), not the legacy untagged format (`sha256:`), so full verification is performed rather than being skipped with a legacy warning.
- **Blocking behavior**: The mismatch triggers a hard stop. The skill does not proceed to any subsequent step until the user explicitly chooses to proceed or abort.
