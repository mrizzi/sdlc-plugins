# Triage Outcome: TC-8006 -- Step 4.2 Pre-Existing Link Handling

## How Step 4.2 Handled the Pre-Existing Link

### Context

TC-8006 (CVE-2026-31812, stream [rhtpa-2.1]) has a pre-existing `Related` link to TC-8001 (CVE-2026-31812, stream [rhtpa-2.2]). This link was already present in the issue's `issuelinks` array when the issue was fetched in Step 1.

### Step 4.2 Procedure

Step 4.2 (Cross-stream coordination) requires that before creating a `Related` link to a different-stream sibling, the skill must first check the current issue's existing `issuelinks` array for a link that satisfies all of these conditions:

1. `type.name` is `"Related"`
2. `inwardIssue.key` or `outwardIssue.key` matches the sibling key

### What Happened

1. **JQL sibling search** returned TC-8001 as a different-stream companion (stream suffix `[rhtpa-2.2]` vs TC-8006's `[rhtpa-2.1]`).

2. **Existing link check**: The skill inspected TC-8006's `issuelinks` array (already available from the Step 1 `jira.get_issue` response). It found Link ID 1990401 with:
   - `type.name` = `"Related"` (condition 1 satisfied)
   - `outwardIssue.key` = `"TC-8001"` (condition 2 satisfied)

3. **Decision**: Since a matching link already exists, Step 4.2 **skipped link creation** entirely. No `jira.create_link` call was made. The skill logged:
   > "Related link to TC-8001 already exists -- skipping"

4. **Remaining Step 4.2 actions proceeded normally**:
   - Affects Versions overlap check: no overlap detected (RHTPA 2.1.0 vs RHTPA 2.2.0/2.2.1 -- disjoint version sets from different streams)
   - Sibling landscape table: presented to the engineer showing both companion issues

### Why This Matters

This idempotent link-checking behavior prevents duplicate issue links in Jira. Without this check, re-triaging an issue or triaging an issue where PSIRT (or a prior triage run) had already created the Related link would result in redundant links cluttering the issue. The check ensures that Step 4.2 is safe to run multiple times on the same issue without side effects.

### Sibling Landscape (Final)

```
CVE-2026-31812 companion issues:

| Issue       | Stream | Status      | Affects Versions              |
|-------------|--------|-------------|-------------------------------|
| TC-8001     | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1     |
| TC-8006 <-  | 2.1.x  | New         | RHTPA 2.1.0                   |
```

The sibling landscape table is always presented regardless of whether a new link was created or an existing one was found. This gives the triaging engineer full visibility into the cross-stream CVE tracking landscape.

## Overall Triage Status at This Point

- **Step 1 (Data Extraction)**: Complete -- CVE-2026-31812, quinn-proto < 0.11.14, Cargo ecosystem, stream 2.1.x
- **Step 4.1 (Duplicate Check)**: No same-stream duplicates found
- **Step 4.2 (Cross-stream Coordination)**: Pre-existing Related link to TC-8001 found and respected; link creation skipped; sibling landscape presented
- **Step 4.3 (Cross-CVE Overlap)**: Skipped -- Upstream Affected Component, PS Component, and Stream custom fields not configured
- **Step 4.4 (Preemptive Reconciliation)**: No preemptive tasks found for this CVE and stream
- **Next steps**: Proceed to Step 5 (Version Lifecycle Check), Step 6 (Already Fixed Check), Step 7 (Concurrent Triage Detection), and Step 8 (Remediation)
