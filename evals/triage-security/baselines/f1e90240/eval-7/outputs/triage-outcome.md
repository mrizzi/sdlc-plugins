# Triage Outcome: TC-8006 -- Step 4.2 Pre-Existing Link Handling

## Summary

TC-8006 (CVE-2026-31812, stream [rhtpa-2.1]) has a pre-existing Related link to sibling issue TC-8001 (stream [rhtpa-2.2]). Step 4.2 of the triage-security skill handled this through its **idempotent link creation** protocol, which checks for existing links before attempting to create new ones.

## How Step 4.2 Handled the Pre-Existing Link

### The Idempotency Protocol

Step 4.2 specifies that before creating a Related link to a different-stream sibling, the skill must first check the current issue's `issuelinks` array (already fetched in Step 1) for any existing link that satisfies **all** of the following conditions:

1. `type.name` is `"Related"`
2. `inwardIssue.key` or `outwardIssue.key` matches the sibling key

### Application to TC-8006

When processing sibling TC-8001:

1. The skill reads TC-8006's existing `issuelinks` array from the Step 1 data.
2. It finds one existing link:
   - Type: Related
   - Direction: outward (TC-8006 -> TC-8001)
   - Link ID: 1990401
3. It checks the criteria:
   - `type.name` is `"Related"` -- **match**
   - `outwardIssue.key` is `TC-8001` -- **match** (the sibling being processed)
4. Both criteria are satisfied, so the link already exists.

### Result

The skill **skips link creation** and logs:

> "Related link to TC-8001 already exists -- skipping"

No `jira.create_link()` API call is made. The pre-existing link is sufficient to establish the cross-stream sibling relationship. This prevents duplicate links and avoids potential Jira API errors from creating a link that already exists.

### Why This Matters

The idempotent check in Step 4.2 ensures that:

- **Re-triaging** an issue does not create duplicate links
- **Pre-linked issues** (where PSIRT or another process already created the Related link) are handled gracefully
- The skill is safe to run multiple times on the same issue without side effects on link state

## Remaining Triage Steps

After Step 4.2 completes (with the link skip), the triage continues normally:

- **Step 4.3** (Cross-CVE Overlap): Skipped because Upstream Affected Component custom field is not configured.
- **Step 4.4** (Preemptive Task Reconciliation): No preemptive tasks found for CVE-2026-31812 in stream 2.1.x.
- **Step 5** (Version Lifecycle Check): Would verify RHTPA 2.1.0 is still within support lifecycle.
- **Step 6** (Already Fixed Check): TC-8001 is In Progress (not Closed/Resolved), so no already-fixed scenario applies.
- **Step 7** (Concurrent Triage Detection): Skipped because Upstream Affected Component is not configured.
- **Step 8** (Remediation): Since both versions in the 2.1.x stream (RHTPA 2.1.0) are affected (quinn-proto 0.11.9 < 0.11.14), the outcome is **Case A** -- create remediation tasks for the 2.1.x stream. Additionally, the 2.2.x stream is also affected (versions 2.2.0 and 2.2.1), but since TC-8001 already exists as a companion CVE Jira for that stream, **Case B** would post a cross-stream impact comment but skip preemptive task creation for the 2.2.x stream (it has its own CVE Jira).
