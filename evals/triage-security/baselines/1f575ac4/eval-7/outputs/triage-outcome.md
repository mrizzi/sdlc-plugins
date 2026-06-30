# Triage Outcome -- Step 4.2 Pre-Existing Link Handling for TC-8006

## Summary

TC-8006 (CVE-2026-31812 for stream [rhtpa-2.1]) has a pre-existing "Related" link to sibling issue TC-8001 (stream [rhtpa-2.2]). Step 4.2 of the triage-security skill handled this correctly through its **idempotent link creation** logic.

## How Step 4.2 Handled the Pre-Existing Link

### The Idempotency Check

Step 4.2 specifies a guard before creating any link:

> "Check for existing link before creating one. Read the current issue's `issuelinks` array from the `jira.get_issue` response (already fetched in Step 1). Check if any existing link satisfies all of:
> - `type.name` is `"Related"`
> - `inwardIssue.key` or `outwardIssue.key` matches the sibling key"

### Application to TC-8006

1. The JQL search for sibling issues with label CVE-2026-31812 returned TC-8001 as a different-stream sibling (stream [rhtpa-2.2] vs TC-8006's [rhtpa-2.1]).

2. Before attempting to create a "Related" link to TC-8001, the skill inspected TC-8006's existing `issuelinks` array from the Step 1 data extraction.

3. The existing links on TC-8006 include:
   - Type: "Related"
   - Direction: outward (TC-8006 -> TC-8001)
   - Link ID: 1990401

4. This existing link satisfies both conditions:
   - `type.name` is "Related" -- matches
   - `outwardIssue.key` is "TC-8001" -- matches the sibling key

5. **Result**: The skill skipped link creation and logged:
   > "Related link to TC-8001 already exists -- skipping"

### Why This Matters

The idempotency check prevents duplicate links from being created when:
- The skill is re-run on the same issue (re-triage scenario)
- PSIRT or another process has already linked the sibling issues manually
- A previous partial triage run created the link but did not complete all steps

Without this check, each triage run would create an additional "Related" link to the same sibling, cluttering the issue's link list with redundant entries.

### What Happened Next

After confirming the link already exists, Step 4.2 continued with its remaining sub-steps:
- **Affects Versions overlap check**: No overlap found (TC-8006 has RHTPA 2.1.0; TC-8001 has RHTPA 2.2.0, RHTPA 2.2.1)
- **Sibling landscape presentation**: The companion issue table was presented showing both issues and their respective streams

The triage then proceeded to Step 4.3 (skipped due to missing configuration) and Step 4.4 (preemptive task reconciliation).

## Overall Triage Disposition

TC-8006 is a valid, non-duplicate vulnerability issue scoped to the 2.1.x stream. Both versions in that stream (RHTPA 2.1.0 and RHTPA 2.1.1) ship quinn-proto 0.11.9, which is below the fix threshold of 0.11.14. The issue requires remediation (Case A) -- creating upstream and downstream remediation tasks for the 2.1.x stream.
