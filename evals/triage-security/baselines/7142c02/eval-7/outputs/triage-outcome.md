# Triage Outcome -- Step 4.2 Pre-existing Link Handling

## Summary

TC-8006 (CVE-2026-31812, stream [rhtpa-2.1]) has a pre-existing Related link to sibling TC-8001 (stream [rhtpa-2.2]). Step 4.2 correctly detected this link and skipped redundant link creation.

## Step 4.2 Detailed Walkthrough

### 1. Sibling Identified

The JQL search for sibling issues with label `CVE-2026-31812` returned one result:

- **TC-8001** -- CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
  - Status: In Progress
  - Stream: 2.2.x (different from TC-8006's 2.1.x)
  - Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1

TC-8001 is classified as a **different-stream companion** (not a same-stream duplicate), because its stream suffix [rhtpa-2.2] differs from TC-8006's [rhtpa-2.1].

### 2. Pre-existing Link Detection (Idempotency Check)

Per the Step 4.2 specification, before creating a Related link, the skill checks the current issue's `issuelinks` array (already fetched in Step 1's `jira.get_issue` response).

TC-8006's existing issue links contain:

```
Link ID: 1990401
Type: Related
Direction: outward (TC-8006 -> TC-8001)
```

The check evaluates whether any existing link satisfies ALL of:
- `type.name` is "Related" -- **YES** (link 1990401 type is Related)
- `inwardIssue.key` or `outwardIssue.key` matches TC-8001 -- **YES** (outwardIssue.key is TC-8001)

Both conditions are met. A matching Related link already exists.

### 3. Link Creation Skipped

Because the pre-existing link satisfies the idempotency check:

> Related link to TC-8001 already exists -- skipping link creation.

No `jira.create_link` call is made. This prevents a duplicate link error from Jira and ensures the skill is idempotent -- running triage multiple times on the same issue does not create redundant links.

### 4. Sibling Landscape Still Presented

Even though link creation was skipped, the sibling landscape table is still presented to the engineer. The link idempotency check only gates the `jira.create_link` mutation; it does not suppress the informational sibling overview. The engineer still needs to see the full companion issue landscape for situational awareness:

```
CVE-2026-31812 companion issues:

| Issue      | Stream | Status      | Affects Versions              |
|------------|--------|-------------|-------------------------------|
| TC-8006 <- | 2.1.x  | New         | RHTPA 2.1.0                   |
| TC-8001    | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1     |
```

### 5. No Affects Versions Overlap

The two companion issues carry versions from their respective streams only:
- TC-8006: RHTPA 2.1.0 (2.1.x stream)
- TC-8001: RHTPA 2.2.0, RHTPA 2.2.1 (2.2.x stream)

No overlap detected. No corrective action needed.

## Key Behaviors Demonstrated

1. **Idempotent link handling**: Step 4.2 checks existing `issuelinks` BEFORE attempting to create a Related link. When a matching link is found, creation is skipped with a log message.

2. **Different-stream companion classification**: TC-8001 ([rhtpa-2.2]) is correctly identified as a cross-stream companion, not a same-stream duplicate. No duplicate closure is recommended.

3. **Sibling landscape always presented**: The companion issue table is shown regardless of whether a new link was created or an existing one was detected. The table provides context the engineer needs.

4. **Log message emitted**: The skip action produces an explicit log message: "Related link to TC-8001 already exists -- skipping link creation." This provides an audit trail that the check was performed and the existing link was recognized.

## Overall Triage Status

After Step 4, the triage proceeds to Steps 5-7:
- Both 2.1.x versions (2.1.0 and 2.1.1) are affected (quinn-proto 0.11.9 < 0.11.14 fix threshold)
- TC-8001 is already tracking remediation for the 2.2.x stream (status: In Progress)
- TC-8006 needs remediation tasks created for the 2.1.x stream (Case A -- affected, create remediation tasks)
- Since the ecosystem is Cargo (Rust), two tasks would be created: upstream backport task (source repo rhtpa-backend, branch release/0.3.z) and downstream propagation subtask (Konflux release repo rhtpa-release.0.3.z)
