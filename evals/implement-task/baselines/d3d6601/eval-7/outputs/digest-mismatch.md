# Step 1.5 — Verify Description Integrity: Digest Mismatch Handling

## Context

Task: TC-9201 — "Add advisory severity aggregation service and endpoint"

The Jira issue has one comment posted by a previous plan-feature run with the body:

```
[sdlc-workflow] Description digest: sha256:0000000000000000000000000000000000000000000000000000000000000000
```

## Step-by-Step Handling

### 1. Retrieve issue comments

Fetch all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the digest comment

Search all returned comments for those whose body starts with the marker string `[sdlc-workflow] Description digest:`.

One comment matches the marker. If multiple had matched, we would select the most recent one by `created` timestamp. In this case there is only one matching comment.

### 3. Check for comment editing (timestamp comparison)

Compare the comment's `created` and `updated` timestamps. Per the scenario, the `created` and `updated` timestamps are identical. This means the comment was **not edited** after initial posting. No warning is needed for comment tampering — proceed with digest comparison.

### 4. Extract the stored digest

From the comment body `[sdlc-workflow] Description digest: sha256:0000000000000000000000000000000000000000000000000000000000000000`, extract:

- **Stored digest (expected):** `sha256:0000000000000000000000000000000000000000000000000000000000000000`

### 5. Compute the current digest

Take the current description field text of TC-9201 as returned by the Jira API and compute its SHA-256 hash.

Per the description digest protocol, use the `scripts/sha256-digest.py` script (preferred method) to compute the digest, or normalize manually:
- If the description is ADF JSON (MCP path): parse as JSON, re-serialize with compact separators (`json.dumps(parsed, separators=(',', ':'))`), then hash.
- If the description is raw text (REST API path): strip leading and trailing whitespace, then hash.

The output is a lowercase 64-character hexadecimal SHA-256 digest.

In practice this would be done via:
```bash
python3 scripts/sha256-digest.py /tmp/desc.json
```

The computed digest would be some value like `sha256:abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890` (the actual hash of the current description content).

- **Computed digest (actual):** `sha256:<actual-64-char-hex-from-current-description>`

### 6. Compare digests — MISMATCH DETECTED

The stored digest `sha256:0000000000000000000000000000000000000000000000000000000000000000` does **not** match the computed digest of the current description. This means the task description was modified after plan-feature created it.

### 7. Alert the user

Present the following warning to the user:

---

**Warning: Task description integrity check failed.**

The task description for TC-9201 was modified after plan-feature created it. The description digest does not match the value recorded at creation time.

- **Expected digest** (from plan-feature comment): `sha256:0000000000000000000000000000000000000000000000000000000000000000`
- **Actual digest** (computed from current description): `sha256:<actual-64-char-hex-from-current-description>`

This means someone (or something) changed the task description between planning and implementation. The implementation may no longer align with what was originally planned.

**Options:**
1. **Proceed** — implement the task using the current (modified) description as-is
2. **Stop** — halt execution so you can review the changes and optionally re-run plan-feature to regenerate tasks with a fresh digest

Choose (1/2):

---

### 8. STOP — Do NOT proceed to Step 2

**Execution halts here.** Per the SKILL.md instructions:

> "Stop execution immediately — do not proceed with any subsequent steps until the user responds."

No further steps are taken. Specifically:
- Do NOT proceed to Step 2 (Verify Dependencies)
- Do NOT begin implementation planning
- Do NOT create branches or modify code
- Do NOT transition the Jira issue

The skill waits for the user's explicit choice before continuing.

## Summary of Verification Logic

| Check | Result |
|---|---|
| Digest comment found? | Yes — one comment matches `[sdlc-workflow] Description digest:` marker |
| Comment edited after posting? | No — `created` equals `updated` |
| Stored digest | `sha256:0000000000000000000000000000000000000000000000000000000000000000` |
| Computed digest | Different from stored (description was modified) |
| Digests match? | **No — MISMATCH** |
| Action | Alert user with expected vs actual values, offer proceed/stop choice, halt execution |
