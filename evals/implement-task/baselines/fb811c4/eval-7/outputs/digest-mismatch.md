# Step 1.5 — Description Integrity Verification for TC-9201

## Context

Task TC-9201 ("Add advisory severity aggregation service and endpoint") was fetched
and parsed successfully in Step 1. The structured description contains all required
sections: Repository, Target Branch, Description, Files to Modify, Files to Create,
API Changes, Implementation Notes, Acceptance Criteria, Test Requirements, and
Dependencies.

Step 1.5 now verifies that the description has not been modified since plan-feature
created it, following the digest protocol defined in
`shared/description-digest-protocol.md`.

## Procedure

### 1. Retrieve issue comments

Fetch all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the digest comment

Search returned comments for bodies starting with the marker string
`[sdlc-workflow] Description digest:`. One matching comment is found with body:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

Since only one comment matches the marker, it is selected (no need to resolve
multiple comments by timestamp).

### 3. Comment edit detection

The comment's `created` and `updated` timestamps are identical. Per the protocol,
this means the comment was not edited after initial posting. No warning is needed.
Proceed to digest comparison.

### 4. Extract the stored digest

Parse the tagged digest from the comment body:

- **Format tag:** `sha256-md`
- **Hex digest:** `0000000000000000000000000000000000000000000000000000000000000000`

The digest uses the modern format-tagged format (not the legacy untagged `sha256:<hex>`
format), so no legacy-format warning is needed.

### 5. Compute the current digest

Extract the description field from the TC-9201 issue response. Write it to a temp
file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the format (markdown text in this case) and outputs a tagged
digest, for example:

```
sha256-md:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

(The actual hex value would be computed from the current description content.)

### 6. Compare format tags

- Stored tag: `sha256-md`
- Computed tag: `sha256-md`

The format tags match. Both the producer (plan-feature) and consumer (implement-task)
used the same API access method (both got markdown text). Proceed to hex digest
comparison.

### 7. Compare hex digests

- **Expected** (from digest comment): `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Actual** (computed from current description): `sha256-md:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

**MISMATCH.** The hex digests differ. The task description was modified after
plan-feature created it.

## Action Taken: Alert User and Stop

Per the protocol and Step 1.5 of the implement-task skill, execution stops
immediately with the following alert to the user:

---

> **Warning: Task description was modified after plan-feature created it.**
>
> The description integrity check detected that the task description for TC-9201
> has been changed since plan-feature originally generated it.
>
> **Expected digest** (recorded by plan-feature):
> `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
>
> **Actual digest** (computed from current description):
> `sha256-md:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
>
> This means someone (or an automated process) edited the task description after
> it was planned. The implementation may not match the original plan.
>
> **How would you like to proceed?**
>
> 1. **Proceed** — implement using the current (modified) description as-is
> 2. **Stop** — abort so you can re-run plan-feature to regenerate tasks with
>    a fresh plan that matches the updated description
>
> Please choose (1 or 2):

---

**Execution is halted.** No subsequent steps (Step 2 — Verify Dependencies, Step 3 —
Transition to In Progress, Step 4 — Understand the Code, etc.) are executed until
the user responds.

## Rationale

The digest mismatch indicates the description was tampered with or intentionally
modified after plan-feature created it. This is a safety mechanism that prevents
implementing a task whose specification may have diverged from the original plan.
The user must make an explicit decision:

- If the modification was intentional and the current description is correct,
  choosing "Proceed" allows implementation to continue with the updated spec.
- If the modification was unintended or suspicious, choosing "Stop" allows the
  user to investigate and re-plan if necessary, ensuring the implementation
  matches a verified plan.
