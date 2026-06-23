# Triage Outcome: TC-8006

## Step 4.2 -- Pre-Existing Link Handling

### What Happened

When processing the cross-stream sibling TC-8001 (stream [rhtpa-2.2]) in Step 4.2, the skill checked the current issue's `issuelinks` array -- which was already fetched in Step 1 via `jira.get_issue(TC-8006)` -- before attempting to create a Related link.

### Link Check Details

The `issuelinks` array on TC-8006 contained:

```
{
  "id": "1990401",
  "type": { "name": "Related" },
  "outwardIssue": { "key": "TC-8001" }
}
```

This satisfies both conditions specified in Step 4.2 of `jira-triage-operations.md`:
1. `type.name` is `"Related"` -- YES
2. `outwardIssue.key` matches the sibling key `TC-8001` -- YES

### Decision

> Related link to TC-8001 already exists -- skipping

Because a matching Related link was already present, **no `jira.create_link` call was made**. This is the correct idempotent behavior -- the skill avoids creating duplicate links by checking existing links before proposing any mutation.

### What Was Still Done

Even though the link already existed, the skill still completed the remaining Step 4.2 obligations:

1. **Affects Versions overlap check**: Verified no version overlap between TC-8006 (RHTPA 2.1.0, stream 2.1.x) and TC-8001 (RHTPA 2.2.0, RHTPA 2.2.1, stream 2.2.x). No overlap detected.

2. **Sibling landscape table**: Presented the full companion issue landscape to the engineer:

   | Issue | Stream | Status | Affects Versions |
   |-------|--------|--------|------------------|
   | TC-8006 (current) | 2.1.x | New | RHTPA 2.1.0 |
   | TC-8001 | 2.2.x | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |

### Why This Matters

The pre-existing link check ensures idempotent behavior. If the skill is run multiple times on the same issue (e.g., re-triage after new information), it will not create duplicate Related links. The check is performed against the issue's existing `issuelinks` data from Step 1, requiring no additional Jira API calls.

## Overall Triage Status

### Proposed Actions (Not Yet Executed)

All actions below are **proposals** requiring engineer confirmation before execution:

1. **Affects Versions Correction (Step 3):** The current Affects Versions (RHTPA 2.1.0) should be verified against the version impact table. Both 2.1.0 and 2.1.1 ship quinn-proto 0.11.9 (vulnerable). If RHTPA 2.1.1 has a matching Jira version, the proposed correction would be:
   - Current: `[RHTPA 2.1.0]`
   - Proposed: `[RHTPA 2.1.0, RHTPA 2.1.1]`

2. **Sibling Link (Step 4.2):** No action needed -- Related link to TC-8001 already exists.

3. **Cross-CVE Overlap (Step 4.3):** Skipped -- required custom fields not configured.

4. **Version Lifecycle (Step 5):** Pending -- requires WebFetch of the product lifecycle page at `https://access.example.com/product-life-cycle/rhtpa`.

5. **Already Fixed Check (Step 6):** TC-8001 (the only sibling) has status "In Progress", not "Closed/Done". No already-fixed scenario applies.

6. **Remediation (Step 7):** Since both 2.1.x versions are affected (quinn-proto 0.11.9 < 0.11.14 fix threshold), the expected outcome is Case A (create remediation tasks). For a Cargo ecosystem dependency, this means:
   - **Upstream backport task**: Bump quinn-proto to >= 0.11.14 in the backend source repo on branch `release/0.3.z`
   - **Downstream propagation subtask**: Update the artifact reference in the Konflux release repo (`rhtpa-release.0.3.z`) to pick up the fixed backend build

   These tasks would be linked to TC-8006 and follow `task-description-template.md` format for `/implement-task` compatibility.
