# Data Extraction — TC-8001

## Step 0.7 — Assign and Transition to Assigned

**Proposed actions** (simulation — not executed):

1. **Retrieve current user's Jira account ID:**
   ```
   jira.user_info()
   ```

2. **Assign TC-8001 to current user:**
   ```
   jira.edit_issue("TC-8001", assignee=<current-user-account-id>)
   ```
   Rationale: The issue is currently Unassigned. Assigning immediately provides
   visibility into who is actively triaging the issue and enables Step 7
   (Concurrent Triage Detection).

3. **Discover the target transition dynamically:**
   ```
   jira.get_transitions("TC-8001")
   ```
   Select the transition whose target status name is "Assigned".

4. **Transition TC-8001 from New to Assigned:**
   ```
   jira.transition_issue("TC-8001", <assigned-transition-id>)
   ```
   The issue is currently in New status, so the transition proceeds.

---

## Step 1 — Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Stream scope | 2.2.x (mapped from suffix `[rhtpa-2.2]` to Version Streams table) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Ecosystem | Cargo (Rust crate) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |
| Deployment context | upstream (default — no Deployment Context column in Source Repositories) |
