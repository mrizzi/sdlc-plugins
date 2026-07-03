# Sibling and Link Analysis — Step 4

## Step 4: Duplicate, Sibling, Overlap, and Reconciliation Check

### JQL Search for Siblings

Search query (simulated):
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

**Result**: 1 sibling found.

| Issue | Summary | Status | Stream Suffix | Affects Versions |
|-------|---------|--------|---------------|------------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | [rhtpa-2.2] | RHTPA 2.2.0, RHTPA 2.2.1 |

### Step 4.1 — Same-Stream Duplicate Check

TC-8001 has stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream.
TC-8006 has stream suffix `[rhtpa-2.1]`, which maps to the **2.1.x** stream.

These are **different streams**. TC-8001 is NOT a same-stream duplicate.

Result: **No same-stream duplicates found.** Proceed to Step 4.2.

### Step 4.2 — Cross-Stream Coordination

TC-8001 is a **different-stream sibling** (companion tracker). PSIRT creates one Vulnerability issue per stream intentionally. This is expected behavior.

#### Existing Link Check

Before creating a Related link, check the current issue's `issuelinks` array (fetched in Step 1):

- TC-8006 has an existing link:
  - **Type**: Related
  - **Direction**: outward (TC-8006 -> TC-8001)
  - **Link ID**: 1990401

Checking if this link satisfies the criteria:
1. `type.name` is `"Related"` -- YES
2. `outwardIssue.key` matches the sibling key `TC-8001` -- YES

**Both conditions are met.** A matching Related link already exists.

> Related link to TC-8001 already exists -- skipping

Link creation is **skipped** (idempotent behavior).

#### Affects Versions Overlap Check

- TC-8006 Affects Versions: RHTPA 2.1.0 (stream 2.1.x)
- TC-8001 Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1 (stream 2.2.x)

No overlap detected. Each issue carries versions from its own stream only. This is the correct state.

#### Sibling Landscape

```
CVE-2026-31812 companion issues:

| Issue      | Stream | Status      | Affects Versions             |
|------------|--------|-------------|------------------------------|
| TC-8001    | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1    |
| TC-8006 <- | 2.1.x  | New         | RHTPA 2.1.0                  |
```

The arrow (`<-`) marks the current issue being triaged.

### Step 4.3 — Cross-CVE Overlap Detection

The Upstream Affected Component custom field is **not configured** in the Security Configuration (no `Upstream Affected Component custom field` entry exists). Per the skill definition, Step 4.3 is **skipped entirely** when this field is not configured.

### Step 4.4 — Preemptive Task Reconciliation

Search for preemptive tasks (simulated):
```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812' ORDER BY created DESC
```

No preemptive tasks were specified in the eval scenario. Proceeding to Step 5.
