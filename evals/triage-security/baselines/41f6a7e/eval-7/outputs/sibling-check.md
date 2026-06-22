# Step 4 -- Duplicate and Sibling Check: TC-8006

## JQL Search for Siblings

Simulated JQL query:
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

### Search Results

| Issue Key | Summary | Status | Labels | Affects Versions | Stream Suffix |
|-----------|---------|--------|--------|------------------|---------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 | [rhtpa-2.2] |

## Sibling Classification

- **TC-8006** stream suffix: `[rhtpa-2.1]` -> stream `2.1.x`
- **TC-8001** stream suffix: `[rhtpa-2.2]` -> stream `2.2.x`

Classification: **Different-stream sibling** (companion tracker). TC-8001 tracks the same CVE (CVE-2026-31812) for a different product version stream (2.2.x vs 2.1.x). This is intentional -- PSIRT creates one Vulnerability issue per stream.

### 4.1 -- Same-stream Duplicate Check

No same-stream siblings found. TC-8001 has a different stream suffix (`[rhtpa-2.2]`) than TC-8006 (`[rhtpa-2.1]`). This is NOT a duplicate.

### 4.2 -- Cross-stream Coordination

TC-8001 is a different-stream sibling (companion tracker for the 2.2.x stream).

#### Link Check (Idempotent)

Before creating a new "Related" link, the skill checks the existing `issuelinks` array from the `jira.get_issue` response fetched in Step 1.

**Existing links on TC-8006:**
- Link ID 1990401: type = "Related", direction = outward, outwardIssue.key = **TC-8001**

**Check criteria (all must match):**
1. `type.name` is "Related" -- YES (type is "Related")
2. `inwardIssue.key` or `outwardIssue.key` matches sibling key TC-8001 -- YES (outwardIssue.key = TC-8001)

**Result: A matching "Related" link to TC-8001 already exists.**

Action taken:
> "Related link to TC-8001 already exists -- skipping"

No `jira.create_link` call is made. The pre-existing link is sufficient; creating another would produce a duplicate link.

#### Affects Versions Overlap Check

- TC-8006 Affects Versions: RHTPA 2.1.0 (stream 2.1.x)
- TC-8001 Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1 (stream 2.2.x)

No version overlap detected. Each issue carries only versions from its own stream, which is the expected pattern.

#### Sibling Landscape

```
CVE-2026-31812 companion issues:

| Issue      | Stream | Status      | Affects Versions         |
|------------|--------|-------------|--------------------------|
| TC-8001    | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |
| TC-8006 <- | 2.1.x  | New         | RHTPA 2.1.0              |
```

The arrow `<-` marks the current issue being triaged.

TC-8001 is already In Progress for the 2.2.x stream, indicating that remediation work has begun for that stream. TC-8006 still needs remediation for the 2.1.x stream.
