# Step 1.5 — Description Integrity Verification: Digest Mismatch Handling

## Context

Task TC-9201 has been fetched and parsed in Step 1. The task description contains a structured implementation plan for adding an advisory severity aggregation service and endpoint to the trustify-backend repository. Step 1.5 now verifies description integrity before proceeding to any subsequent steps.

## Procedure

### 1. Retrieve Issue Comments

Fetch all comments on TC-9201 using:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the Digest Comment

Search the returned comments for any whose body starts with the marker string defined in `shared/description-digest-protocol.md`:

```
[sdlc-workflow] Description digest:
```

One comment is found matching this marker. Its body is:

```
[sdlc-workflow] Description digest: sha256:0000000000000000000000000000000000000000000000000000000000000000
```

Since only one comment matches the marker, it is selected directly. (If multiple had matched, the most recent by `created` timestamp would be selected.)

### 3. Comment Edit Detection

The protocol requires comparing the comment's `created` and `updated` timestamps to detect post-hoc editing. In this case, the two timestamps are identical -- the comment has not been edited since it was posted. No "comment was edited" warning is needed.

### 4. Extract the Stored Digest

The stored digest extracted from the comment is:

```
Expected (from comment): sha256:0000000000000000000000000000000000000000000000000000000000000000
```

### 5. Compute the Current Digest

Compute the SHA-256 hash of the current description field text. Following the normalization rules from `shared/description-digest-protocol.md`:

- If the description is ADF JSON (MCP path): parse as JSON and re-serialize with compact separators (`json.dumps(parsed, separators=(',', ':'))`) before hashing.
- If the description is raw text (REST API path): strip leading and trailing whitespace before hashing.

The computation is performed using the `scripts/sha256-digest.py` tool (preferred method per the protocol) to eliminate LLM hashing errors:

```bash
python3 scripts/sha256-digest.py /tmp/desc.json
```

This produces a 64-character lowercase hexadecimal SHA-256 digest of the current description content. The resulting hash will differ from the stored all-zeros digest because the description was modified after plan-feature created the task.

```
Actual (computed from current description): sha256:<computed-64-char-hex-digest>
```

### 6. Compare Digests — MISMATCH Detected

The expected digest (from the comment) and the actual digest (computed from the current description) do NOT match:

```
Expected: sha256:0000000000000000000000000000000000000000000000000000000000000000
Actual:   sha256:<computed-64-char-hex-digest>
```

This indicates that the task description was modified after plan-feature originally created it.

### 7. Alert the User

The following alert is displayed to the user:

> **Warning: Task description modified after planning**
>
> The description of TC-9201 has been modified since plan-feature created this task. The description integrity check failed:
>
> - **Expected digest** (recorded by plan-feature): `sha256:0000000000000000000000000000000000000000000000000000000000000000`
> - **Actual digest** (computed from current description): `sha256:<computed-64-char-hex-digest>`
>
> The task description was changed after plan-feature generated it. This may mean the requirements have shifted and the implementation plan may no longer be aligned with the current description.
>
> **How would you like to proceed?**
>
> 1. **Proceed** — Continue implementing with the current (modified) description as-is
> 2. **Stop** — Abort implementation so you can re-run plan-feature to regenerate tasks from the updated feature description
>
> Choose (1/2):

### 8. STOP Execution

Execution halts immediately at this point. No subsequent steps are performed:

- Step 2 (Verify Dependencies) is NOT executed.
- Step 3 (Transition to In Progress) is NOT executed.
- Step 4 (Understand the Code) is NOT executed.
- Step 5 (Create Branch) is NOT executed.
- No implementation planning, code changes, branching, or Jira transitions occur.

The skill waits for the user to respond with their choice before taking any further action. If the user chooses option 1 (Proceed), execution would continue from Step 2. If the user chooses option 2 (Stop), execution terminates entirely.

## Summary

Step 1.5 detected a digest mismatch between the stored digest (`sha256:000...000`) and the SHA-256 hash of the current task description. This means the description was modified after plan-feature originally created the task. The user is presented with a choice to proceed or stop, and execution is halted until they respond. No plan.md is produced and no implementation work begins.
