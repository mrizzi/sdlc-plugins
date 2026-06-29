# Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check

## Step 4 Overview

JQL search for sibling Vulnerability issues with the same CVE label:

```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

**Result**: 1 sibling found -- TC-8001.

## Sibling Classification

| Sibling | Stream Suffix | Stream | Classification |
|---------|---------------|--------|---------------|
| TC-8001 | [rhtpa-2.2]   | 2.2.x  | Different-stream companion |

TC-8001 has stream suffix `[rhtpa-2.2]` (2.2.x stream), while TC-8006 has suffix `[rhtpa-2.1]` (2.1.x stream). These are **different streams**, so TC-8001 is a **cross-stream companion**, NOT a same-stream duplicate.

## Step 4.1 -- Same-stream Duplicate Check

No same-stream siblings found. TC-8001 is in a different stream (2.2.x vs 2.1.x). No duplicate closure needed.

## Step 4.2 -- Cross-stream Coordination

TC-8001 is a different-stream companion for the 2.2.x stream.

### Link Idempotency Check

Before creating a Related link to TC-8001, the existing `issuelinks` array on TC-8006 (fetched in Step 1) is inspected.

**Existing links on TC-8006:**

| Link ID | Type | Direction | Target |
|---------|------|-----------|--------|
| 1990401 | Related | outward (TC-8006 -> TC-8001) | TC-8001 |

**Check**: Does any existing link satisfy ALL of:
1. `type.name` is "Related" -- YES (link 1990401 is type Related)
2. `inwardIssue.key` or `outwardIssue.key` matches TC-8001 -- YES (outwardIssue.key = TC-8001)

**Result**: A matching Related link to TC-8001 already exists (link ID 1990401).

> Related link to TC-8001 already exists -- skipping link creation.

Link creation is SKIPPED. No `jira.create_link` call is made.

### Affects Versions Overlap Check

- TC-8006 (2.1.x stream): Affects Versions = [RHTPA 2.1.0]
- TC-8001 (2.2.x stream): Affects Versions = [RHTPA 2.2.0, RHTPA 2.2.1]

No version overlap detected. Each issue carries only versions from its own stream. This is correct.

### Sibling Landscape

Despite the link already existing, the sibling landscape table is still presented to the engineer for situational awareness:

```
CVE-2026-31812 companion issues:

| Issue      | Stream | Status      | Affects Versions              |
|------------|--------|-------------|-------------------------------|
| TC-8006 <- | 2.1.x  | New         | RHTPA 2.1.0                   |
| TC-8001    | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1     |
```

The arrow (`<-`) marks the current issue being triaged.

TC-8001 is already In Progress in the 2.2.x stream, indicating that remediation work has begun for the 2.2.x stream independently.

## Step 4.3 -- Cross-CVE Overlap Detection

**Prerequisite check**: The Security Configuration in CLAUDE.md does not include:
- Upstream Affected Component custom field -- NOT configured
- PS Component custom field -- NOT configured
- Stream custom field -- NOT configured

Since these fields are not configured, Step 4.3 is **skipped entirely** per the skill specification.

## Step 4.4 -- Preemptive Task Reconciliation

Search for preemptive tasks matching CVE-2026-31812:

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812' ORDER BY created DESC
```

No preemptive tasks found for this CVE and the 2.1.x stream. Proceeding to Step 5.
