# Jira Triage Operations

This companion file contains the detailed procedures for Steps 3–6 of the
triage-security skill. These steps handle Affects Versions correction,
duplicate and sibling detection, cross-CVE overlap detection, preemptive task
reconciliation, version lifecycle checks, and already-fixed detection.

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

Add a comment documenting the correction. If a ProdSec Jira account ID is
configured in Security Configuration, append an @mention before the Comment
Footnote using an ADF mention node:

```json
{ "type": "mention", "attrs": { "id": "<prodsec-jira-account-id>", "text": "@<prodsec-name>" } }
```

If no ProdSec Jira account ID is configured, omit the @mention silently.

```
jira.add_comment(<jira-issue-id>, "Corrected Affects Versions: [old] → [new].
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to stream <stream> per issue suffix.
[ProdSec @mention if configured]")
```

## Step 4 – Duplicate, Sibling, and Overlap Check

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

1. **Check for existing link** before creating one. Read the current issue's
   `issuelinks` array from the `jira.get_issue` response (already fetched in
   Step 1). Check if any existing link satisfies all of:
   - `type.name` is `"Related"`
   - `inwardIssue.key` or `outwardIssue.key` matches the sibling key

   If a matching link exists, skip link creation and log:
   > "Related link to [sibling-key] already exists — skipping"

   If no matching link exists, create the link:
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

**If no siblings found**, proceed to Step 4.3.

### 4.3 – Cross-CVE overlap detection

Search for Vulnerability issues that affect the **same upstream component** as the
current issue, regardless of CVE ID. This detects cases where a different CVE's
remediation already bumped the library past the current CVE's fix threshold.

**Prerequisite:** This step requires the Upstream Affected Component custom field,
PS Component custom field, and Stream custom field to be configured in Security
Configuration (Step 0). If any of these fields are not configured, skip this step
entirely.

1. **Extract the Upstream Affected Component** from the current issue's
   `<upstream-affected-component-field>` (already fetched in Step 1 with
   `fields=["*all"]`). If the field is empty or not present, skip this step —
   cross-CVE overlap detection requires the component field to be populated.

2. **Search for related CVE Jiras** with the same component value:

   ```
   jira.search_jql(
     "project = <project-key> AND issuetype = <vulnerability-issue-type-id> AND cf[<upstream-affected-component-field-number>] ~ '<component-value>' AND key != <current-issue-key>",
     fields: ["summary", "status", "labels", "issuelinks", "<upstream-affected-component-field>", "<ps-component-field>", "<stream-field>"]
   )
   ```

   Where `<upstream-affected-component-field-number>` is the numeric portion of the
   configured field ID (e.g., `10632` from `customfield_10632`).

3. **Filter results** to matching PS Component (`<ps-component-field>`) and Stream
   (`<stream-field>`) values. Only issues that share the same PS Component and
   Stream as the current issue are relevant — different components or streams are
   tracked separately.

4. **Traverse issue links** on each matching CVE Jira. For each match, inspect
   its `issuelinks` array for linked remediation Tasks (link type `"Depend"` —
   the same link type used when `triage-security` creates remediation tasks).
   Fetch each linked remediation Task to inspect its description.

5. **Compare remediation coverage.** For each remediation Task found, extract
   the dependency version bump from its description (the target version the
   library is bumped to). Compare this version against the current CVE's fix
   threshold (from Step 1's Data Extraction — the "fixed version" field):

   - If the remediation task's bump version **meets or exceeds** the current
     CVE's fix threshold: the existing remediation already covers this CVE.
   - If the bump version is **below** the fix threshold: the existing
     remediation does not cover this CVE.

6. **Present findings** to the engineer. If a ProdSec Jira account ID is
   configured in Security Configuration, append an @mention before the Comment
   Footnote in any comments posted during this step, using an ADF mention node:

   ```json
   { "type": "mention", "attrs": { "id": "<prodsec-jira-account-id>", "text": "@<prodsec-name>" } }
   ```

   If no ProdSec Jira account ID is configured, omit the @mention silently.

   - **If a covering remediation exists:**
     ```
     Existing remediation task [task-key] (from [related-CVE-ID]) already bumps
     [library] to [version], which meets or exceeds this CVE's fix threshold
     ([fix-version]). No new remediation task needed.

     Recommendation: Close this issue — the fix is already covered by [task-key].
     [ProdSec @mention if configured]
     ```

     **After engineer confirms closure**, create traceability links and post an
     explanatory comment before transitioning to Closed:

     a. **Create Related link** between the current CVE and the related CVE
        (idempotent — check existing `issuelinks` first, same pattern as
        Step 4.2):

        Check the current issue's `issuelinks` array (already fetched in
        Step 1) for an existing link where `type.name` is `"Related"` and
        `inwardIssue.key` or `outwardIssue.key` matches the related CVE key.

        If a matching link exists, skip and log:
        > "Related link to [related-cve-key] already exists — skipping"

        If no matching link exists, create the link:
        ```
        jira.create_link(
          inwardIssue: <current-cve-key>,
          outwardIssue: <related-cve-key>,
          type: "Related"
        )
        ```

     b. **Create Depend link** from the covering remediation task to the
        current CVE (same link type as standard remediation linkage in
        `remediation-templates.md`):

        Check the current issue's `issuelinks` array for an existing link
        where `type.name` is `"Depend"` and `inwardIssue.key` or
        `outwardIssue.key` matches the covering task key.

        If a matching link exists, skip and log:
        > "Depend link to [covering-task-key] already exists — skipping"

        If no matching link exists, create the link:
        ```
        jira.create_link(
          inwardIssue: <current-cve-key>,
          outwardIssue: <covering-task-key>,
          type: "Depend"
        )
        ```

     c. **Post a comment** on the current CVE documenting the cross-CVE
        overlap finding. If a ProdSec Jira account ID is configured, include
        an @mention before the Comment Footnote:
        ```
        Cross-CVE overlap: existing remediation task [covering-task-key] (from
        [related-CVE-ID] / [related-cve-key]) already bumps [library] to
        [version], which meets or exceeds this CVE's fix threshold
        ([fix-version]).

        Links created:
        - Related: [current-cve-key] ↔ [related-cve-key] (same upstream component)
        - Depend: [current-cve-key] → [covering-task-key] (covering remediation)

        [ProdSec @mention if configured]
        [Comment Footnote]
        ```

        MUST include the Comment Footnote (see SKILL.md).
   - **If related CVEs exist but no covering remediation:**
     ```
     Related CVE Jiras found for [component] in the same stream:

     | Related CVE | Issue | Remediation Task | Bump Version | Covers This CVE? |
     |-------------|-------|------------------|--------------|------------------|
     | CVE-YYYY-XXXXX | TC-1234 | TC-1235 | 1.2.3 | No (threshold: 1.3.0) |

     No existing remediation covers this CVE's fix threshold. Proceeding with
     new remediation task creation.
     [ProdSec @mention if configured]
     ```
   - **If no related CVEs found for this component:** proceed silently to Step 4.4.

### 4.4 – Preemptive task reconciliation

When triaging a new CVE Jira for a specific stream, check whether a proactive
remediation task already exists for this CVE and stream (created by a prior
Step 8 Case B run on a different stream's CVE Jira).

1. **Search for preemptive tasks** matching the current CVE:

   ```
   jira.search_jql(
     "project = <project-key> AND issuetype = Task AND labels = 'security-preemptive' AND labels = '<CVE-ID>' ORDER BY created DESC",
     fields: ["summary", "status", "labels", "issuelinks"]
   )
   ```

2. **Filter results** to tasks whose summary contains the current issue's stream
   name (e.g., the stream suffix from the issue summary). A preemptive task
   created for stream `rhtpa-2.1` will have `(rhtpa-2.1)` in its summary.

3. **If a matching preemptive task is found:**

   a. **Link** the new CVE Jira to the preemptive task with "Depend" (standard
      remediation linkage):
      ```
      jira.create_link(
        inwardIssue: <current-cve-jira-key>,
        outwardIssue: <preemptive-task-key>,
        type: "Depend"
      )
      ```
   b. **Remove the `security-preemptive` label** from the task — it is now
      linked to a proper CVE Jira:
      ```
      current_labels = <preemptive-task-labels>
      updated_labels = current_labels.filter(l => l != "security-preemptive")
      jira.edit_issue(<preemptive-task-key>, fields={
        "labels": updated_labels
      })
      ```
   c. **Inform the engineer:**
      ```
      Existing preemptive remediation task [task-key] found for this CVE and
      stream. Created from cross-stream analysis of [originating-CVE-Jira]
      (linked via "Related").

      Actions taken:
      - Linked [current-cve-key] → [task-key] with "Depend"
      - Removed "security-preemptive" label from [task-key]

      The preemptive task is now a standard remediation task for this CVE Jira.
      Skipping new remediation task creation in Step 8.
      ```
   d. **Record the reconciliation** — mark that remediation already exists for
      this stream so Step 8 skips task creation for it.

4. **If no matching preemptive task found:** proceed silently to Step 5.

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
the unfixed versions and proceed to Step 8.

**If no resolved siblings exist**, proceed to Step 8.

## Step 7 – Concurrent Triage Detection

Before creating remediation tasks (Cases A/B), check whether another engineer is
actively triaging a different CVE that affects the same upstream component. This
prevents duplicate remediation tasks when two triages reach Step 8 simultaneously.

**Prerequisite:** This step requires the Upstream Affected Component custom field
to be configured in Security Configuration (Step 0). If the field is not configured,
skip this step entirely — consistent with Step 4.3's conditional behavior.

1. **Extract the Upstream Affected Component** from the current issue (already
   fetched in Step 1). If the field is empty, skip this step.

2. **Search for in-progress triages** on the same component:

   ```
   jira.search_jql(
     "project = <project-key> AND issuetype = <vulnerability-issue-type-id> AND cf[<upstream-affected-component-field-number>] ~ '<component-value>' AND status IN ('In Progress', 'Code Review') AND key != <current-issue-key>",
     fields: ["summary", "status", "labels", "assignee"]
   )
   ```

3. **If results are returned**, present the concurrent triages to the engineer:

   ```
   ⚠️ Concurrent triage detected on the same upstream component (<component-value>):

   | CVE Issue | Status | Assignee |
   |-----------|--------|----------|
   | <key-1>   | In Progress | <assignee-1> |

   Another engineer is actively triaging a related CVE. Creating remediation
   tasks now may produce duplicates.

   Options:
   1. Wait — pause until the other triage completes, then re-run Step 4.3
      to detect any overlap
   2. Skip — skip remediation task creation for this CVE
   3. Proceed — create tasks anyway with a `concurrent-triage-overlap` label
      so the other engineer's Step 4.3 catches the overlap
   ```

4. **Handle user choice:**
   - **Wait**: stop execution and inform the user to re-run after the concurrent
     triage completes.
   - **Skip**: skip Step 8 entirely (do not create remediation tasks) and add a
     Jira comment explaining why task creation was skipped.
   - **Proceed**: add the `concurrent-triage-overlap` label to the current issue
     and continue to Case A/B/C branching. The label ensures the other triage's
     Step 4.3 cross-CVE overlap detection picks up the overlap.

5. **If no results are returned**, proceed silently to Case A/B/C branching.
