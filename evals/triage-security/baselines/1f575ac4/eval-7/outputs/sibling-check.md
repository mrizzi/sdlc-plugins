# Step 4 -- Sibling and Link Analysis for TC-8006

## Step 4 Overview

Step 4 performs Duplicate, Sibling, Overlap, and Reconciliation checks. For TC-8006, the key sub-steps are:

- **Step 4.1** -- Same-stream duplicate check
- **Step 4.2** -- Cross-stream coordination (sibling linking)
- **Step 4.3** -- Cross-CVE overlap detection (skipped -- no Upstream Affected Component field configured)
- **Step 4.4** -- Preemptive task reconciliation

## JQL Search for Siblings

Simulated JQL:
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

**Result**: 1 sibling issue found.

| Issue | Summary | Status | Labels | Affects Versions |
|-------|---------|--------|--------|------------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 |

## Step 4.1 -- Same-Stream Duplicate Check

- TC-8006 stream suffix: `[rhtpa-2.1]` (stream 2.1.x)
- TC-8001 stream suffix: `[rhtpa-2.2]` (stream 2.2.x)
- Classification: **Different-stream sibling** (companion tracker, not a duplicate)

Conclusion: TC-8001 is NOT a same-stream duplicate. It tracks a different stream (2.2.x vs 2.1.x). No duplicate closure recommended.

## Step 4.2 -- Cross-Stream Coordination

TC-8001 is a **different-stream sibling** -- a companion tracker for the same CVE in the 2.2.x stream. Per the SKILL.md Step 4.2 procedure:

### Link Existence Check

Per Step 4.2 rule 1: "Check for existing link before creating one. Read the current issue's `issuelinks` array from the `jira.get_issue` response (already fetched in Step 1)."

Checking TC-8006's existing issue links:
- Link found: type.name = "Related", outwardIssue.key = "TC-8001", Link ID = 1990401

All three conditions are satisfied:
1. `type.name` is "Related" -- YES
2. `outwardIssue.key` matches the sibling key (TC-8001) -- YES
3. Link already exists -- YES

**Result**: Related link to TC-8001 already exists -- skipping link creation.

> "Related link to TC-8001 already exists -- skipping"

### Affects Versions Overlap Check

Per Step 4.2 rule 2: "Verify no Affects Versions overlap."

- TC-8006 Affects Versions: RHTPA 2.1.0
- TC-8001 Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1

No overlap detected. Each issue carries versions only from its own stream:
- TC-8006 owns the 2.1.x versions
- TC-8001 owns the 2.2.x versions

### Sibling Landscape

Per Step 4.2 rule 3: "Present the sibling landscape to the engineer."

```
CVE-2026-31812 companion issues:

| Issue      | Stream | Status      | Affects Versions             |
|------------|--------|-------------|------------------------------|
| TC-8001    | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1    |
| TC-8006 <- | 2.1.x  | New         | RHTPA 2.1.0                  |
```

The arrow indicates TC-8006 is the current issue being triaged.

## Step 4.3 -- Cross-CVE Overlap Detection

**Skipped.** The project's Security Configuration does not include the Upstream Affected Component custom field, PS Component custom field, or Stream custom field. Per the SKILL.md: "If any of these fields are not configured, skip this step entirely."

## Step 4.4 -- Preemptive Task Reconciliation

A search for preemptive tasks matching CVE-2026-31812 would be performed:

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812' ORDER BY created DESC
```

Assuming no preemptive tasks are found for this CVE and stream, proceed to Step 5.
