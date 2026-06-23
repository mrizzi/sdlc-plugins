# Triage Outcome: TC-8010 (CVE-2026-44492)

## Summary

**Decision: Close TC-8010 -- remediation already covered by existing task TC-8009.**

CVE-2026-44492 requires axios >= 1.8.2 to fix an SSRF vulnerability. A related
CVE (CVE-2026-42035 / TC-8008) targeting the same upstream component (axios),
same PS Component (pscomponent:org/rhtpa-ui), and same stream (rhtpa-2.2) already
has an in-progress remediation task (TC-8009) that bumps axios from 1.7.4 to 1.9.0.
Since 1.9.0 >= 1.8.2, the existing remediation fully covers this CVE's fix
threshold.

## Rationale

1. **Cross-CVE overlap detected (Step 4.3):** JQL search on
   `cf[10632] ~ 'axios'` returned TC-8008 (CVE-2026-42035), which shares the
   same Upstream Affected Component, PS Component, and Stream as TC-8010.

2. **Existing remediation covers this CVE:** TC-8008's linked remediation task
   TC-8009 bumps axios to 1.9.0. The current CVE (CVE-2026-44492) requires
   axios >= 1.8.2. Since 1.9.0 >= 1.8.2, TC-8009 already resolves both
   CVE-2026-42035 and CVE-2026-44492.

3. **No new remediation task needed:** Creating a separate task to bump axios
   for this CVE would be redundant -- TC-8009 already accomplishes the required
   version bump.

## Proposed Actions

The following Jira mutations are recommended (pending engineer confirmation):

### 1. Link TC-8010 to TC-8009

Create a "Depend" link from TC-8010 to TC-8009 so the vulnerability issue
tracks the existing remediation:

```
jira.create_link(
  inwardIssue: "TC-8010",
  outwardIssue: "TC-8009",
  type: "Depend"
)
```

### 2. Link TC-8010 to TC-8008 as Related

Create a "Related" link between the two CVE Jiras that share the same
component and stream:

```
jira.create_link(
  inwardIssue: "TC-8010",
  outwardIssue: "TC-8008",
  type: "Related"
)
```

### 3. Add triage comment to TC-8010

```
jira.add_comment("TC-8010", "
Cross-CVE overlap analysis: existing remediation task TC-8009 (from
CVE-2026-42035 / TC-8008) already bumps axios to 1.9.0, which meets or
exceeds this CVE's fix threshold (>= 1.8.2). No new remediation task needed.

Version impact: axios is consumed by rhtpa-ui in stream rhtpa-2.2. The
current version (1.7.4) is within the affected range (< 1.8.2). The
in-progress bump to 1.9.0 via TC-8009 will resolve both CVE-2026-42035
and CVE-2026-44492.

Triage outcome: Covered by existing remediation. Linking TC-8010 to TC-8009
(Depend) and TC-8008 (Related).

---
_Triage performed by triage-security skill._
")
```

### 4. Add the ai-cve-triaged label

```
jira.edit_issue("TC-8010", fields={
  "labels": ["CVE-2026-44492", "pscomponent:org/rhtpa-ui", "ai-cve-triaged"]
})
```

### 5. Transition and resolution

Since the existing remediation (TC-8009) is still In Progress, TC-8010 should
remain open and linked until TC-8009 completes. The recommended approach:

- Transition TC-8010 to **In Progress** to reflect that remediation is underway
  (via TC-8009).
- Once TC-8009 completes and the axios bump lands, TC-8010 can be closed as
  **Done** alongside TC-8008.

Alternatively, if the team prefers to close overlap issues immediately:
- Close TC-8010 with a comment noting it is covered by TC-8009.
- Resolution: "Done" (the fix is in progress and will resolve this CVE).

## Key Evidence

| Evidence Point | Detail |
|----------------|--------|
| Current CVE | CVE-2026-44492 (SSRF in axios < 1.8.2) |
| Fix threshold | axios >= 1.8.2 |
| Related CVE | CVE-2026-42035 (Prototype Pollution in axios < 1.8.0) |
| Related CVE Jira | TC-8008 (In Progress) |
| Remediation task | TC-8009: Bump axios to 1.9.0 (In Progress) |
| Coverage | 1.9.0 >= 1.8.2 -- fully covered |
| Stream | rhtpa-2.2 (both CVEs target the same stream) |
| Component | pscomponent:org/rhtpa-ui (both CVEs target the same component) |
