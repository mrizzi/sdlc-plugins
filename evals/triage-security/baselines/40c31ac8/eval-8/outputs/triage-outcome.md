# Triage Outcome: TC-8010 (CVE-2026-44492)

## Decision: Close -- Already Covered by Existing Remediation

TC-8010 does **not** require a new remediation task. The vulnerability is already addressed by an in-progress remediation from a related CVE.

## Rationale

CVE-2026-44492 affects axios versions before 1.8.2 (SSRF via crafted URL bypass). A JQL search on the Upstream Affected Component field (customfield_10632 = "axios") revealed that TC-8008 (CVE-2026-42035) targets the same component (axios), same PS Component (pscomponent:org/rhtpa-ui), and same stream (rhtpa-2.2).

TC-8008 has a linked remediation task TC-8009 ("Bump axios to 1.9.0 in rhtpa-ui [rhtpa-2.2]"), which is currently In Progress. This task bumps axios from 1.7.4 to 1.9.0.

**Version comparison:**
- CVE-2026-44492 fix threshold: **1.8.2**
- TC-8009 target version: **1.9.0**
- 1.9.0 >= 1.8.2: **YES -- covered**

When TC-8009 completes, the axios version in rhtpa-ui will be 1.9.0, which is above the 1.8.2 threshold needed to resolve CVE-2026-44492. Therefore, no additional remediation work is required.

## Proposed Jira Actions

The following actions would be performed (each requiring engineer confirmation per the skill's guardrails):

### 1. Link to related CVE and remediation
- Create "Related" link: TC-8010 <-> TC-8008 (same upstream component, different CVEs)
- Create "Depend" link: TC-8010 -> TC-8009 (remediation task that covers this CVE)

### 2. Add triage comment to TC-8010
```
Cross-CVE overlap detected: existing remediation task TC-8009 (from
CVE-2026-42035 / TC-8008) already bumps axios to 1.9.0, which meets
or exceeds this CVE's fix threshold (1.8.2). No new remediation task
needed.

Version impact: axios versions before 1.8.2 are vulnerable.
TC-8009 bumps axios from 1.7.4 to 1.9.0, covering both CVE-2026-42035
(threshold >= 1.8.0) and CVE-2026-44492 (threshold >= 1.8.2).

Closing as covered by existing remediation.
```

### 3. Add ai-cve-triaged label
Add the `ai-cve-triaged` label to TC-8010 to mark it as triaged.

### 4. Close TC-8010
- Transition to Closed
- Resolution: dependent on workflow -- either "Done" (fix is in progress via TC-8009) or "Not a Bug" (no separate fix needed since TC-8009 covers it)
- The close acknowledges that the vulnerability is real but remediation is already handled

## Key Evidence Chain

```
TC-8010 (CVE-2026-44492, axios SSRF, fix >= 1.8.2)
    |
    |-- JQL: cf[10632] ~ 'axios' finds TC-8008
    |
    +-> TC-8008 (CVE-2026-42035, axios Prototype Pollution, fix >= 1.8.0)
            |
            +-> TC-8009 (Remediation: bump axios to 1.9.0) [In Progress]
                    |
                    +-- 1.9.0 >= 1.8.2 --> COVERS CVE-2026-44492
```

## What Would Change This Decision

- If TC-8009 were cancelled or its target version reduced below 1.8.2, a new remediation task would be needed for TC-8010
- If TC-8009 scope changed to a different stream or component, the overlap would no longer apply
- If the fix threshold for CVE-2026-44492 were revised upward (above 1.9.0), TC-8009 would no longer cover it
