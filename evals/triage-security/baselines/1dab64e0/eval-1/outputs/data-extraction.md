# Step 0.7 -- Early Assignment Actions

## Proposed Actions

1. **Retrieve current user's Jira account ID:**
   ```
   jira.user_info()
   ```

2. **Assign TC-8001 to the current user:**
   ```
   jira.edit_issue("TC-8001", assignee=<current-user-account-id>)
   ```
   Rationale: Issue is currently Unassigned. Assigning provides visibility into who is actively triaging and enables concurrent triage detection (Step 7).

3. **Discover the Assigned transition:**
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

# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Stream scope | 2.2.x (maps to Konflux release repo rhtpa-release.0.4.z) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | quinn-rs/quinn#2048 (https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | GHSA-2026-qp73-x4mq (https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |
| Ecosystem | Cargo (Rust crate -- quinn-proto is a Rust crate in the Cargo ecosystem) |
| Deployment context | upstream (default -- Source Repositories table has no Deployment Context column) |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Security Configuration's Version Streams table. This stream corresponds to the Konflux release repo `rhtpa-release.0.4.z`.

Steps 3-8 are scoped to the 2.2.x stream. However, the full version impact analysis (Step 2) covers all configured streams (2.1.x and 2.2.x) to detect cross-stream impact.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The Ecosystem Mappings table for both streams lists **Cargo** with lock file `Cargo.lock` and check command `git show <tag>:Cargo.lock`. The ecosystem is Cargo for both the 2.1.x and 2.2.x streams.
