# Triage Outcome: TC-8006 -- Step 4.2 Pre-existing Link Handling

## Summary

TC-8006 (CVE-2026-31812 for stream [rhtpa-2.1]) has a pre-existing "Related" link to sibling issue TC-8001 (stream [rhtpa-2.2]). Step 4.2 of the triage-security skill handles this case through an **idempotent link check** that prevents duplicate link creation.

## How Step 4.2 Handled the Pre-existing Link

### The Idempotent Check

Step 4.2 requires that before creating a "Related" link to any cross-stream sibling, the skill must first check the current issue's `issuelinks` array (already fetched in Step 1 via `jira.get_issue`). The check verifies whether any existing link satisfies ALL of:

1. `type.name` is `"Related"`
2. `inwardIssue.key` or `outwardIssue.key` matches the sibling key

### Application to TC-8006

TC-8006's issue links (from the Step 1 fetch) include:
- Link ID 1990401, type "Related", outward direction, outwardIssue.key = TC-8001

When the JQL search in Step 4 identifies TC-8001 as a cross-stream sibling, Step 4.2 checks for an existing link before attempting to create one. The existing link matches both criteria:
1. Type is "Related" -- matches
2. outwardIssue.key is "TC-8001" -- matches the sibling key

### Result

Because a matching link already exists, the skill **skips link creation** and logs:

> "Related link to TC-8001 already exists -- skipping"

No `jira.create_link` call is made. This prevents creating a duplicate "Related" link between TC-8006 and TC-8001.

### Why This Matters

Without the idempotent check, re-running triage on TC-8006 (or triaging it after TC-8001 already created the reciprocal link) would produce duplicate "Related" links in Jira. The Step 4.2 protocol ensures that:

- Links are checked before creation, not blindly created
- The direction of the existing link does not matter (the check looks at both `inwardIssue.key` and `outwardIssue.key`)
- The skill is safe to re-run without side effects on link state

## Remaining Step 4.2 Actions

After the link check, Step 4.2 continues with:

1. **Affects Versions overlap check**: No overlap found. TC-8006 carries RHTPA 2.1.0 (2.1.x stream) and TC-8001 carries RHTPA 2.2.0, RHTPA 2.2.1 (2.2.x stream). Each issue correctly owns only its own stream's versions.

2. **Sibling landscape presentation**: The companion issue table is presented to the engineer showing both TC-8001 (In Progress, 2.2.x) and TC-8006 (New, 2.1.x), giving full visibility into the CVE's cross-stream tracking status.

## Overall Triage Status

TC-8006 is NOT a duplicate (different stream from TC-8001). Both 2.1.x versions (2.1.0, 2.1.1) ship quinn-proto 0.11.9, which is vulnerable (before fixed version 0.11.14). The issue requires remediation for the 2.1.x stream. The sibling TC-8001 is already In Progress for the 2.2.x stream.
