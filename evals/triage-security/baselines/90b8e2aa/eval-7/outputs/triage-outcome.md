# Triage Outcome -- Step 4.2 Pre-Existing Link Handling: TC-8006

## Summary

TC-8006 (stream [rhtpa-2.1]) had a pre-existing "Related" link to sibling TC-8001 (stream [rhtpa-2.2]) when triage began. Step 4.2 correctly detected this link and **skipped link creation**, ensuring idempotent behavior.

## How Step 4.2 Handled the Pre-Existing Link

### The Idempotency Check

Step 4.2 specifies that before creating a "Related" link to a cross-stream sibling, the skill must first check the current issue's `issuelinks` array (fetched in Step 1) for an existing link that satisfies ALL of:
1. `type.name` is `"Related"`
2. `inwardIssue.key` or `outwardIssue.key` matches the sibling key

### Application to TC-8006

TC-8006's `issuelinks` array contained one entry:
- Link ID: 1990401
- Type: Related (type.name = "Related")
- Direction: outward (outwardIssue.key = "TC-8001")

Both criteria were satisfied:
- Criterion 1: type.name "Related" matches "Related"
- Criterion 2: outwardIssue.key "TC-8001" matches the sibling key TC-8001

### Result

The skill logged: **"Related link to TC-8001 already exists -- skipping"**

No `jira.create_link()` call was made. The existing link (ID 1990401) was left intact. This prevents duplicate links from being created if triage is re-run or if PSIRT pre-linked the issues before triage began.

## Why This Matters

Without the idempotency check, re-running triage on TC-8006 (or triaging an issue that PSIRT already linked to its sibling) would create a second "Related" link to TC-8001, resulting in duplicate links on the issue. The check-before-create pattern ensures that Step 4.2 is safe to run multiple times on the same issue without side effects.

## Remaining Triage Path

After Step 4.2 completed (with link skipped), the triage continued:
- Step 4.3 (Cross-CVE overlap): **Skipped** -- Upstream Affected Component, PS Component, and Stream custom fields are not configured in Security Configuration
- Step 4.4 (Preemptive task reconciliation): **No matching preemptive tasks found**
- The triage would proceed to Steps 5-8 for lifecycle check, already-fixed check, concurrent triage detection, and remediation task creation for the affected 2.1.x stream versions
