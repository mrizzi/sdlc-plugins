# Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check: TC-8006

## Step 4 -- JQL Sibling Search

JQL query (simulated):
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

### Search Results

One sibling found:

| Issue | Summary | Status | Labels | Affects Versions | Stream Suffix |
|-------|---------|--------|--------|------------------|---------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 | [rhtpa-2.2] |

### Sibling Classification

- **TC-8001**: stream suffix `[rhtpa-2.2]` maps to stream **2.2.x**
- **TC-8006** (current): stream suffix `[rhtpa-2.1]` maps to stream **2.1.x**
- Classification: **Different-stream sibling** (companion tracker, NOT a duplicate)

PSIRT intentionally created one Vulnerability issue per stream. TC-8001 tracks the 2.2.x stream while TC-8006 tracks the 2.1.x stream.

## Step 4.1 -- Same-Stream Duplicate Check

No same-stream siblings found. TC-8001 is a different-stream sibling (2.2.x vs 2.1.x). No duplicate closure needed.

## Step 4.2 -- Cross-Stream Coordination

TC-8001 is a different-stream companion tracker. Per the skill procedure, before creating a "Related" link, we must check the current issue's existing `issuelinks` array.

### Existing Link Check

The issue data from Step 1 shows that TC-8006 already has the following issue link:

- **Type**: Related
- **Direction**: outward (TC-8006 -> TC-8001)
- **Link ID**: 1990401
- **Target**: TC-8001

**Check result**: A link of type `"Related"` already exists where `outwardIssue.key` matches sibling TC-8001.

**Action**: Skip link creation. Log:
> "Related link to TC-8001 already exists -- skipping"

No new link is created. The pre-existing Related link satisfies the cross-stream coordination requirement. The skill is idempotent -- it does not create duplicate links.

### Affects Versions Overlap Check

- TC-8006 Affects Versions: RHTPA 2.1.0
- TC-8001 Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1

No version overlap detected -- each issue carries versions from its own stream only. No flag needed.

### Sibling Landscape

```
CVE-2026-31812 companion issues:

| Issue      | Stream | Status      | Affects Versions              |
|------------|--------|-------------|-------------------------------|
| TC-8001    | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1     |
| TC-8006 <- | 2.1.x  | New         | RHTPA 2.1.0                   |
```

Note: TC-8006's Affects Versions may need correction in Step 3 -- the version impact table shows both RHTPA 2.1.0 and RHTPA 2.1.1 are affected, but only RHTPA 2.1.0 is currently listed.

## Step 4.3 -- Cross-CVE Overlap Detection

The Upstream Affected Component custom field is not configured in the project's Security Configuration (claude-md-security-config.md does not include this optional field). Per the skill procedure, Step 4.3 is **skipped entirely**.

## Step 4.4 -- Preemptive Task Reconciliation

Simulated JQL search for preemptive tasks:
```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812' ORDER BY created DESC
```

No matching preemptive tasks found for CVE-2026-31812 and stream rhtpa-2.1. Proceeding to Step 5.
