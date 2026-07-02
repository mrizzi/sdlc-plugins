# Step 1.5 -- Description Integrity Verification for TC-9201

## Process

### 1. Retrieve issue comments

After fetching the task in Step 1, I retrieve all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the digest comment

I search through all returned comments for any whose body starts with the marker string `[sdlc-workflow] Description digest:`. This marker is defined in `shared/description-digest-protocol.md`.

In this case, one comment matches:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

Since there is only one matching comment, no tie-breaking by `created` timestamp is needed. If multiple comments matched, I would select the most recent one by `created` timestamp.

### 3. Check for comment editing

I compare the comment's `created` and `updated` timestamps. In this case they are identical, which means the comment has not been edited after initial posting. No warning is needed for this check -- proceed to digest comparison.

(If `updated` were later than `created`, I would warn: "Digest comment was edited after initial posting -- integrity cannot be fully guaranteed." and proceed with comparison regardless.)

### 4. Extract the stored digest

From the comment body, I parse:

- **Format tag:** `sha256-md`
- **Hex digest:** `0000000000000000000000000000000000000000000000000000000000000000`

The digest uses the current tagged format (not the legacy untagged `sha256:<hex>` format), so I proceed with the full comparison.

### 5. Compute the current digest

I extract the description field from the TC-9201 issue response (the markdown text of the task description), write it to a temporary file, and compute the digest using the script:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format. Since the description is markdown text (not ADF JSON), the script outputs a tagged digest in the form:

```
sha256-md:<computed-64-char-hex>
```

For example, the script might output:

```
sha256-md:a3f8b2c1d4e5f67890abcdef1234567890abcdef1234567890abcdef12345678
```

### 6. Compare format tags

The stored tag is `sha256-md` and the computed tag is `sha256-md` -- the tags match. This means both the producer (plan-feature) and the consumer (implement-task) used the same API access method (both received markdown), so direct hex comparison is valid.

(If the tags differed -- e.g., stored was `sha256-adf` but computed was `sha256-md` -- I would log a warning about format mismatch and skip the integrity check entirely, proceeding normally.)

### 7. Compare hex digests -- MISMATCH DETECTED

The stored hex digest and the computed hex digest do not match:

- **Expected** (from plan-feature digest comment): `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Actual** (computed from current description): `sha256-md:a3f8b2c1d4e5f67890abcdef1234567890abcdef1234567890abcdef12345678`

## Alert to User

At this point, I stop execution and present the following alert:

---

**WARNING: Task description modified after planning**

The description for TC-9201 has been modified since plan-feature created this task. The description digest does not match the value recorded at creation time.

- **Expected digest** (recorded by plan-feature): `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Actual digest** (computed from current description): `sha256-md:a3f8b2c1d4e5f67890abcdef1234567890abcdef1234567890abcdef12345678`

This means someone (or an automated process) changed the task description after plan-feature generated it. The implementation may no longer align with the original plan.

**Options:**

1. **Proceed** -- implement using the current (modified) description as-is
2. **Stop** -- halt implementation so you can re-run plan-feature to regenerate tasks from the updated feature description

Choose (1/2):

---

## Execution State

**Execution is stopped.** I do not proceed to Step 2 (Verify Dependencies), Step 3 (Transition to In Progress), or any subsequent implementation steps until the user responds with their choice.

- If the user chooses **1 (Proceed)**: I continue with Step 2 using the current task description, accepting that it differs from what plan-feature originally produced.
- If the user chooses **2 (Stop)**: I halt entirely and inform the user to re-run plan-feature before re-invoking implement-task.
