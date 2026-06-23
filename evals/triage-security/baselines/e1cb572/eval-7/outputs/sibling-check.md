# Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check for TC-8006

## Step 4 Overview

Search for sibling Vulnerability issues with the same CVE label (CVE-2026-31812).

### JQL Query (simulated)

```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

### JQL Result

One sibling found:

| Issue | Summary | Status | Labels | Affects Versions | Stream Suffix |
|-------|---------|--------|--------|------------------|---------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 | [rhtpa-2.2] |

## Step 4.1 -- Same-Stream Duplicate Check

TC-8006 has stream suffix `[rhtpa-2.1]`. TC-8001 has stream suffix `[rhtpa-2.2]`.

These are **different streams** -- TC-8001 is NOT a same-stream duplicate. It is a cross-stream companion tracker.

**Result**: No same-stream duplicates found. Proceed to Step 4.2.

## Step 4.2 -- Cross-Stream Coordination

TC-8001 is a different-stream sibling (companion tracker for the 2.2.x stream). Per the skill procedure:

### Step 4.2.1 -- Check for Existing Link

Before creating a Related link, check the current issue's `issuelinks` array (already fetched in Step 1).

TC-8006's existing issue links:

- **Related** (outward): TC-8001 (Link ID: 1990401)

**Check result**: A link already exists that satisfies all conditions:
- `type.name` is "Related" -- YES
- `outwardIssue.key` matches the sibling key TC-8001 -- YES

**Action**: Related link to TC-8001 already exists -- skipping link creation.

> "Related link to TC-8001 already exists -- skipping"

### Step 4.2.2 -- Verify No Affects Versions Overlap

Compare Affects Versions between the two issues:

- **TC-8006** (stream 2.1.x): Affects Versions = [RHTPA 2.1.0]
- **TC-8001** (stream 2.2.x): Affects Versions = [RHTPA 2.2.0, RHTPA 2.2.1]

No overlapping versions. Each issue carries only versions from its own stream.

**Result**: No Affects Versions overlap detected.

### Step 4.2.3 -- Sibling Landscape

```
CVE-2026-31812 companion issues:

| Issue       | Stream | Status      | Affects Versions              |
|-------------|--------|-------------|-------------------------------|
| TC-8001     | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1     |
| TC-8006 <-  | 2.1.x  | New         | RHTPA 2.1.0                   |
```

The arrow `<-` marks the current issue being triaged.

## Step 4.3 -- Cross-CVE Overlap Detection

**Skipped.** The Security Configuration in claude-md-security-config.md does not include the Upstream Affected Component custom field, PS Component custom field, or Stream custom field. Per the skill definition, Step 4.3 is skipped entirely when these fields are not configured.

## Step 4.4 -- Preemptive Task Reconciliation

### Simulated JQL Query

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812' ORDER BY created DESC
```

### Result

No preemptive remediation tasks found for CVE-2026-31812 with stream rhtpa-2.1. Proceeding to Step 5.
