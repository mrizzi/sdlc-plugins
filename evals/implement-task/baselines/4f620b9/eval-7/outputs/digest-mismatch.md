# Step 1.5 — Description Integrity Verification for TC-9201

## Context

Task TC-9201 ("Add advisory severity aggregation service and endpoint") has been
fetched from Jira in Step 1. The structured description was successfully parsed,
yielding all required sections (Repository, Target Branch, Description, Files to
Modify, Files to Create, API Changes, Implementation Notes, Acceptance Criteria,
Test Requirements, Dependencies). Step 1 completed without issues.

Step 1.5 now verifies that the task description has not been modified since
plan-feature originally created it, following the protocol defined in
`shared/description-digest-protocol.md`.

## Procedure

### 1. Retrieve issue comments

Fetch all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the digest comment

Search the returned comments for any whose body starts with the marker string:

```
[sdlc-workflow] Description digest:
```

In this scenario, one comment is found with the body:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

Since only one comment matches the marker, it is selected (if multiple had matched,
the most recent by `created` timestamp would be selected).

### 3. Comment edit detection

The comment's `created` and `updated` timestamps are compared. In this scenario,
they are identical, which means the comment has not been edited after initial
posting. No warning is emitted for comment tampering. Proceed with digest
comparison.

### 4. Extract the stored digest

Parse the tagged digest value from the comment body:

- **Format tag**: `sha256-md`
- **Hex digest**: `0000000000000000000000000000000000000000000000000000000000000000`

The digest uses the tagged format (`sha256-md:`), not the legacy untagged format
(`sha256:`), so the legacy format warning does not apply.

### 5. Compute the current digest

Extract the description field from the Jira issue response (the markdown text of
the Description section). Write it to a temporary file:

```bash
# Write the current description to a temp file
cat > /tmp/desc-TC-9201.txt << 'DESCRIPTION'
Add a service method and REST endpoint that aggregates vulnerability advisory severity
counts for a given SBOM. The endpoint returns a summary with counts per severity level
(Critical, High, Medium, Low) and a total, enabling dashboard widgets to render severity
breakdowns without client-side counting.
DESCRIPTION
```

Compute the digest using the project script:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format (plain text / markdown in this case) and
outputs a tagged digest. Example output:

```
sha256-md:b7e9f3a2d1c8e5f4a3b2c1d0e9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0
```

(The actual hex value would be the real SHA-256 of the normalized description text.)

### 6. Compare format tags

- Stored tag: `sha256-md`
- Computed tag: `sha256-md`

The format tags **match**. Both the producer (plan-feature) and consumer
(implement-task) used the same API access method (both obtained the description as
markdown text). Proceed to hex digest comparison.

If the tags had differed (e.g., stored `sha256-adf` vs. computed `sha256-md`), the
skill would log a warning ("Digest format mismatch — skipping integrity check") and
proceed normally without blocking.

### 7. Compare hex digests — MISMATCH DETECTED

- **Expected** (from digest comment): `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Actual** (computed from current description): `sha256-md:b7e9f3a2d1c8e5f4a3b2c1d0e9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0`

The hex digests do **not** match. This means the task description was modified after
plan-feature originally created it.

### 8. Alert the user and STOP execution

The skill immediately alerts the user with the following message:

---

> **Description integrity check failed for TC-9201.**
>
> The task description has been modified since plan-feature created it.
> This may indicate manual edits to the description that could cause the
> implementation to diverge from the original plan.
>
> **Expected digest** (recorded by plan-feature):
> `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
>
> **Actual digest** (computed from current description):
> `sha256-md:b7e9f3a2d1c8e5f4a3b2c1d0e9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0`
>
> **Options:**
> 1. **Proceed** — implement the task using the current (modified) description as-is
> 2. **Stop** — abort so you can re-run plan-feature to regenerate tasks from the updated feature description
>
> Please choose (1 or 2):

---

**Execution is halted immediately.** No subsequent steps (Step 2 through Step 11)
are executed. The skill does not proceed with dependency verification, branch
creation, code understanding, implementation, or any other action. It waits for the
user's explicit response before taking any further action.

## User response handling

- **If the user chooses "Proceed" (option 1)**: The skill continues with Step 2
  (Verify Dependencies) using the current description as-is. The mismatch is noted
  but does not block further execution. The implementation proceeds based on the
  modified description content.

- **If the user chooses "Stop" (option 2)**: The skill terminates. The user is
  expected to re-run plan-feature to regenerate the task descriptions from the
  current feature specification, which will post a new digest comment reflecting
  the updated description. The user can then re-invoke implement-task on the
  regenerated task.

## Rationale

The digest mismatch check guards against silent description tampering between the
planning and implementation phases. Without this check, a manual edit to the task
description could cause the implementation to diverge from the original plan without
any visibility. By comparing the SHA-256 digest recorded at creation time against
the current description, the skill detects modifications and gives the user the
opportunity to either accept the changes or re-plan.

The check is designed to be non-blocking for benign scenarios (missing digest
comments from older tasks, format mismatches from different API access methods,
legacy digest formats) while being a hard stop for confirmed content modifications
(matching format tags but different hex digests).
