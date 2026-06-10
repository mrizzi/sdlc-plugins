# Jira Triage Operations

This companion file contains the detailed procedures for Steps 3–6 of the
triage-security skill. These steps handle Affects Versions correction,
duplicate and sibling detection, version lifecycle checks, and already-fixed
detection.

## Step 3 – Affects Versions Correction

### 3.1 – Discover available Jira versions

Before correcting Affects Versions, dynamically discover what version values exist
in the Jira project. This is done via API — no hardcoded version IDs.

1. Call `getJiraIssueTypeMetaWithFields` for the Vulnerability issue type:
   ```
   jira.getJiraIssueTypeMetaWithFields(
     projectIdOrKey: "<project-key>",
     issueTypeId: "<vulnerability-issue-type-id>"
   )
   ```
2. Extract the `versions` field's `allowedValues` array. Each entry contains:
   - `id` — the Jira version ID (used for mutations)
   - `name` — the display name (e.g., `MYPRODUCT 2.1.0`)
   - `released` — boolean indicating release status
   - `releaseDate` — planned or actual release date
3. Filter by the Jira version prefix (e.g., `MYPRODUCT`) to exclude unrelated versions
   (Helm Charts, Operators, DA releases, etc.).

Present the filtered version registry:

```
Jira Versions matching "<prefix>":

| Jira ID | Name        | Released | Release Date |
|---------|-------------|----------|--------------|
| 62643   | MYPRODUCT 2.1.0 | yes      | 2025-07-27   |
| 62604   | MYPRODUCT 2.1.1 | yes      | 2025-09-16   |
| ...     | ...         | ...      | ...          |
| 104611  | MYPRODUCT 3.0   | no       | 2026-06-30   |
```

### 3.2 – Compare and correct Affects Versions

**Scope the correction to the issue's stream.** If the issue has a stream scope
(from Step 1 stream scope resolution), only include versions belonging to that
stream. If the issue is unscoped, include all affected versions across all streams.

Example for a **scoped** issue with suffix `[myproduct-2.2]`:
- Version impact table shows: MYPRODUCT 2.1.0 (YES), 2.1.1 (YES), 2.2.0 (YES), 2.2.1 (YES)
- This issue is scoped to stream `2.2.x` → only propose: `[MYPRODUCT 2.2.0, MYPRODUCT 2.2.1]`
- The 2.1.x versions belong to a sibling issue (see Step 4)

Compare the PSIRT-assigned Affects Versions (from the Jira `versions` field) against
the **stream-scoped** version impact table:

- **If PSIRT version is wrong** (e.g., "MYPRODUCT 2.0.0" when 2.0 doesn't exist):
  - Show the diff: `Current: [MYPRODUCT 2.0.0] → Proposed: [MYPRODUCT 2.2.0, MYPRODUCT 2.2.1]`
  - Present correction to engineer for confirmation

- **If PSIRT version is correct but incomplete**:
  - Show the additions: `Current: [MYPRODUCT 2.2.0] → Proposed: [MYPRODUCT 2.2.0, MYPRODUCT 2.2.1]`
  - Present correction to engineer for confirmation

- **If the version impact table includes versions not registered in Jira**:
  - Flag: "MYPRODUCT X.Y.Z is in the supportability matrix but has no matching Jira
    version — notify project admin"
  - Continue with available versions; do not block triage

- **If Affects Versions are already correct**: note this and proceed without changes.

**After engineer confirmation**, update the Affects Versions:

```
jira.edit_issue(<jira-issue-id>, fields={
  "versions": [{"id": "<version-id-1>"}, {"id": "<version-id-2>"}, ...]
})
```

Use the Jira version IDs discovered in Step 3.1, not hardcoded values.

**Include development stream versions**: if the issue's stream includes the
development stream and it is affected (from Step 2.2), include the unreleased
Jira version in the Affects Versions correction. Unreleased versions are valid
Affects Versions values — they track that the CVE must be fixed before the next
release ships.

Add a comment documenting the correction:

```
jira.add_comment(<jira-issue-id>, "Corrected Affects Versions: [old] → [new].
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to stream <stream> per issue suffix.")
```

## Step 4 – Duplicate and Sibling Check

Search for sibling Vulnerability issues with the same CVE label:

```
jira.search_jql(
  "project = <project-key> AND labels = '<CVE-ID>' AND issuetype = <vulnerability-issue-type-id> AND key != <current-issue-key>"
)
```

For each sibling found, parse its summary stream suffix (e.g., `[myproduct-2.0]`) to
determine its stream scope. Classify siblings into:

- **Same-stream siblings** — same stream suffix as the current issue (or both unscoped)
- **Different-stream siblings** — different stream suffix (companion trackers)

### 4.1 – Same-stream duplicates

If a same-stream sibling exists and is open or in progress:
- **Recommendation**: Close the current issue as Duplicate.
- Present the sibling issue key and its Affects Versions to the engineer.
- After confirmation:
  1. Add comment: "Duplicate of [sibling-key] — same CVE tracked for the same
     stream [stream]. Version impact analysis confirms overlap."
  2. Transition to Closed with resolution "Duplicate".
  3. Assign to current user.

### 4.2 – Cross-stream coordination

Different-stream siblings are **companion trackers**, not duplicates. PSIRT creates
one issue per stream intentionally. For each different-stream sibling:

1. **Link** the current issue to the sibling with a "Related" link type:
   ```
   jira.create_link(
     inwardIssue: <current-issue-key>,
     outwardIssue: <sibling-key>,
     type: "Related"
   )
   ```
2. **Verify no Affects Versions overlap** — each issue should only carry versions
   from its own stream. If overlap is detected (e.g., both issues claim MYPRODUCT 2.2.0),
   flag it to the engineer: "Version overlap detected between [current-key] and
   [sibling-key] — both claim [overlapping versions]. Please confirm which issue
   should own these versions."
3. **Present the sibling landscape** to the engineer:
   ```
   CVE-YYYY-XXXXX companion issues:

   | Issue     | Stream | Status      | Affects Versions          |
   |-----------|--------|-------------|---------------------------|
   | TC-1234   | 2.1.x  | In Progress | MYPRODUCT 2.1.0, MYPRODUCT 2.1.1 |
   | TC-5678 ← | 2.2.x  | New         | MYPRODUCT 2.2.0, MYPRODUCT 2.2.1 |
   ```

**If no siblings found**, proceed to Step 5.

## Step 5 – Version Lifecycle Check

Verify that the affected product versions are still within their support lifecycle.

1. Fetch the product lifecycle page using the Product pages URL from Security
   Configuration:
   ```
   WebFetch(url: "<product-pages-url>", prompt: "Extract the list of supported
   product versions and their support status (active, maintenance, EOL)")
   ```
2. For each affected version (from the version impact table), check whether it
   appears as actively supported.

**If ALL affected versions are EOL or unsupported**:
- **Recommendation**: Close as Won't Do.
- After confirmation:
  1. Add comment: "All affected versions ([versions]) are EOL per product pages —
     no fix required."
  2. Transition to Closed with resolution "Won't Do".
  3. Assign to current user.

**If SOME affected versions are EOL**: note the EOL versions but continue with
triage for the supported versions. Remove EOL versions from Affects Versions if
they were included.

**If ALL affected versions are supported**: proceed to Step 6.

## Step 6 – Already Fixed Check

Cross-reference resolved sibling Vulnerability issues for the same CVE against the
version impact table.

1. Reuse the JQL results from Step 4 (sibling issues).
2. For siblings with status "Closed" and resolution "Done":
   - Check their Affects Versions.
   - Cross-reference against the version impact table.

**If the current issue's affected versions are all already covered by resolved
siblings**, and the version impact table shows "NO" (not affected) for remaining
versions:
- **Recommendation**: Close as Not a Bug (already fixed by sibling).
- After confirmation:
  1. Add comment: "All affected versions are already covered by resolved sibling
     [sibling-key]. No additional fix required."
  2. Transition to Closed with resolution "Not a Bug".
  3. Assign to current user.
Do **not** set VEX Justification for already-fixed closures — VEX applies only when
the vulnerability does not affect the product.

**If the fix is partial** (some versions covered, others not), narrow the scope to
the unfixed versions and proceed to Step 7.

**If no resolved siblings exist**, proceed to Step 7.
