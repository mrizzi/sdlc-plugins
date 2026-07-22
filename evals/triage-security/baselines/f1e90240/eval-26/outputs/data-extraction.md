# Step 0.7 -- Assign and Transition to Assigned

Before extracting data, assign the Vulnerability issue to the current user and
transition to Assigned status for triage visibility.

1. **Retrieve current user's Jira account ID:**
   ```
   jira.user_info()
   ```

2. **Assign TC-8050 to the current user:**
   ```
   jira.edit_issue("TC-8050", assignee=<current-user-account-id>)
   ```

3. **Discover the Assigned transition dynamically:**
   ```
   jira.get_transitions("TC-8050")
   ```
   Select the transition whose target status name is "Assigned".

4. **Transition to Assigned** (issue is currently in New status):
   ```
   jira.transition_issue("TC-8050", <assigned-transition-id>)
   ```

---

# Step 1 -- Data Extraction

## Issue: TC-8050

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-99001 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Stream scope | 2.2.x |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | criterion |
| Affected version range | versions before 0.5.2 |
| Fixed version | 0.5.2 |
| CVSS | 5.3 (Medium) |
| Upstream fix PR | (none) |
| Advisory URL | (none) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99001 |
| Due date | 2026-08-01 |
| Existing comments | (none) |
| Ecosystem | Cargo |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the
configured Version Stream **2.2.x** (Konflux release repo:
`git.example.com/rhtpa/rhtpa-release.0.4.z`). Triage is scoped to this stream.

## Ecosystem Detection

The vulnerable library `criterion` is a Rust crate. The 2.2.x stream's Ecosystem
Mappings table lists **Cargo** with lock file `Cargo.lock` and check command
`git show <tag>:Cargo.lock`. The ecosystem is Cargo.
