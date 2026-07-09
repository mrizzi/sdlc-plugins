# Triage Outcome: TC-8006 -- Step 4.2 Pre-Existing Link Handling

## Summary

TC-8006 (CVE-2026-31812, stream [rhtpa-2.1]) has a pre-existing Related link to sibling TC-8001 (stream [rhtpa-2.2]). Step 4.2 of the triage-security skill detected this existing link and skipped link creation, demonstrating the idempotent linking behavior specified in the procedure.

## How Step 4.2 Handled the Pre-Existing Link

### Procedure followed

Step 4.2 specifies the following for each different-stream sibling:

> "Check for existing link before creating one. Read the current issue's issuelinks array from the jira.get_issue response (already fetched in Step 1). Check if any existing link satisfies all of:
> - type.name is "Related"
> - inwardIssue.key or outwardIssue.key matches the sibling key
>
> If a matching link exists, skip link creation and log:
> 'Related link to [sibling-key] already exists -- skipping'"

### Evaluation

1. **Sibling identified**: The JQL search returned TC-8001 as a sibling with the same CVE label (CVE-2026-31812) but a different stream suffix ([rhtpa-2.2] vs [rhtpa-2.1]). This classifies TC-8001 as a different-stream companion tracker, not a duplicate.

2. **Existing link detected**: The issue's `issuelinks` array (fetched in Step 1) contains an outward Related link to TC-8001 (link ID 1990401). This satisfies both criteria:
   - `type.name` is `"Related"` -- confirmed
   - `outwardIssue.key` matches the sibling key `TC-8001` -- confirmed

3. **Link creation skipped**: Because a matching link already exists, no `jira.create_link` call is made. The skill logs: "Related link to TC-8001 already exists -- skipping". This is the idempotent behavior -- re-running triage on an issue with pre-existing sibling links does not create duplicate links.

4. **Remaining Step 4.2 checks proceed normally**:
   - Affects Versions overlap check: No overlap (TC-8006 has RHTPA 2.1.0; TC-8001 has RHTPA 2.2.0 and RHTPA 2.2.1). Each issue owns its own stream's versions.
   - Sibling landscape presented to the engineer for awareness.

## Why This Matters

Without the idempotent check, re-triaging TC-8006 (or triaging it after the link was manually created) would create a duplicate Related link to TC-8001. The Step 4.2 procedure explicitly guards against this by inspecting the existing `issuelinks` array before attempting link creation. This is the same idempotent pattern used in Step 4.3 for cross-CVE overlap links.

## Overall Triage Status

- **Step 4.1 (Same-stream duplicate)**: Not a duplicate. TC-8001 is in a different stream.
- **Step 4.2 (Cross-stream coordination)**: Related link to TC-8001 already exists -- skipped link creation. No Affects Versions overlap.
- **Step 4.3 (Cross-CVE overlap)**: Skipped -- Upstream Affected Component field not configured.
- **Step 4.4 (Preemptive task reconciliation)**: No preemptive tasks found for this CVE and stream.

The triage would continue to Step 5 (Version Lifecycle Check) and ultimately reach Case A (remediation task creation) since both 2.1.x versions (RHTPA 2.1.0 and RHTPA 2.1.1) ship vulnerable quinn-proto 0.11.9, which is below the fix threshold of 0.11.14.
