# Step 4.3 -- Cross-CVE Overlap Detection

## Prerequisite Check

The following custom fields are configured in Security Configuration and available on the current issue:

| Field | Custom Field ID | Value on TC-8011 |
|---|---|---|
| Upstream Affected Component | customfield_10632 | webpack |
| PS Component | customfield_10669 | pscomponent:org/rhtpa-ui |
| Stream | customfield_10832 | rhtpa-2.2 |

All three fields are present and populated. Step 4.3 proceeds.

## 1. Upstream Affected Component Extraction

The current issue TC-8011 has `customfield_10632` (Upstream Affected Component) set to **webpack**.

## 2. JQL Search for Related CVE Jiras

Search query:
```
project = TC AND issuetype = 10024 AND cf[10632] ~ 'webpack' AND key != TC-8011
```
Fields requested: summary, status, labels, issuelinks, customfield_10632, customfield_10669, customfield_10832

### Search Results

| Issue | Summary | Status | CVE Label | customfield_10632 | customfield_10669 | customfield_10832 |
|---|---|---|---|---|---|---|
| TC-8012 | CVE-2026-43210 webpack - ReDoS in chunk name validation [rhtpa-2.2] | Closed (Done) | CVE-2026-43210 | webpack | pscomponent:org/rhtpa-ui | rhtpa-2.2 |

## 3. Filter by PS Component and Stream

Filtering TC-8012 against the current issue's PS Component and Stream:

- PS Component match: `pscomponent:org/rhtpa-ui` == `pscomponent:org/rhtpa-ui` -- **Match**
- Stream match: `rhtpa-2.2` == `rhtpa-2.2` -- **Match**

TC-8012 passes both filters and is relevant for overlap analysis.

## 4. Traverse Issue Links on TC-8012

TC-8012's `issuelinks` array contains:

| Link Type | Direction | Linked Issue | Summary | Status |
|---|---|---|---|---|
| Depend | outward | TC-8013 | Bump webpack to 5.96.1 in rhtpa-ui [rhtpa-2.2] | Closed (Done) |

TC-8013 is a remediation Task linked via the "Depend" link type, which is the standard link type used by triage-security for remediation tasks. Fetching TC-8013 to inspect its description.

### TC-8013 Description Excerpt

> "Bump webpack from 5.95.0 to 5.96.1 to resolve CVE-2026-43210. The fix requires webpack >= 5.96.0."

The remediation task bumps webpack to version **5.96.1**.

## 5. Remediation Coverage Comparison

| Parameter | Value |
|---|---|
| Current CVE fix threshold (TC-8011, CVE-2026-45678) | 5.98.0 |
| Existing remediation bump version (TC-8013, from CVE-2026-43210) | 5.96.1 |
| Comparison | 5.96.1 < 5.98.0 |
| Covers this CVE? | **No** |

The existing remediation task TC-8013 bumps webpack to 5.96.1, which is **below** the current CVE's fix threshold of 5.98.0. The fix for CVE-2026-43210 does not resolve CVE-2026-45678. A new remediation task is required.

## 6. Overlap Analysis Summary

Related CVE Jiras found for **webpack** in the same stream (rhtpa-2.2) and PS Component (pscomponent:org/rhtpa-ui):

| Related CVE | Issue | Remediation Task | Bump Version | Covers This CVE? |
|-------------|-------|------------------|--------------|------------------|
| CVE-2026-43210 | TC-8012 | TC-8013 | 5.96.1 | No (threshold: 5.98.0) |

No existing remediation covers this CVE's fix threshold of 5.98.0. Proceeding with new remediation task creation in Step 7.
