# Triage Outcome — TC-8006

## How Step 4.2 Handled the Pre-Existing Link

### Context

TC-8006 (stream [rhtpa-2.1]) had a **pre-existing** Related link to sibling TC-8001 (stream [rhtpa-2.2]) before triage began. The link was already present in the issue's `issuelinks` array with:
- Link ID: 1990401
- Type: Related
- Direction: outward (TC-8006 -> TC-8001)

### Step 4.2 Idempotent Link Handling

Step 4.2 of the triage-security skill requires that before creating a Related link to a different-stream sibling, the skill must **check the current issue's `issuelinks` array** (already fetched in Step 1) for any existing link that satisfies both:

1. `type.name` is `"Related"`
2. `inwardIssue.key` or `outwardIssue.key` matches the sibling key

In this case, the existing outward link to TC-8001 with type "Related" satisfies both conditions. Therefore:

- **Link creation was skipped** with the log message: "Related link to TC-8001 already exists -- skipping"
- **No duplicate link was created** -- the skill behaved idempotently
- **No Jira mutation occurred** for the link step

This idempotent behavior is critical for re-triage scenarios and cases where PSIRT or another process has already linked companion issues. The skill does not blindly create links; it checks first and only creates when no matching link exists.

### Remaining Step 4.2 Actions

Even though link creation was skipped, the skill still performed the remaining Step 4.2 checks:

1. **Affects Versions overlap check**: No overlap detected. TC-8006 carries RHTPA 2.1.0 (2.1.x stream) and TC-8001 carries RHTPA 2.2.0, RHTPA 2.2.1 (2.2.x stream). Each issue correctly owns versions from its own stream only.

2. **Sibling landscape presentation**: The companion issue table was presented to the engineer showing both TC-8001 (2.2.x, In Progress) and TC-8006 (2.1.x, New) with their respective Affects Versions.

### Overall Triage Outcome

TC-8006 is scoped to the 2.1.x stream, where both versions (2.1.0 and 2.1.1) ship quinn-proto 0.11.9, which is below the fix threshold of 0.11.14. The issue falls under **Case A (Affected)** -- remediation tasks would be created for the 2.1.x stream.

The sibling TC-8001 is already In Progress for the 2.2.x stream, so no Case B cross-stream action is needed for that stream -- it already has its own CVE Jira being actively triaged.

No same-stream duplicates were found (Step 4.1). Cross-CVE overlap detection (Step 4.3) was skipped because the Upstream Affected Component custom field is not configured. No preemptive tasks were found (Step 4.4).
