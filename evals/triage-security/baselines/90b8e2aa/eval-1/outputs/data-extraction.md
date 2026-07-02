# Step 0.7 -- Assign and Transition to Assigned

Before extracting CVE data, assign the Vulnerability issue to the current user
and transition it to Assigned status. This provides immediate visibility into
who is actively triaging TC-8001 and enables Step 7 (Concurrent Triage Detection)
to reliably identify active work.

**Proposed actions:**

1. **Retrieve current user's Jira account ID:**

   ```
   jira.user_info()
   ```

   Returns the current user's account ID (e.g., `557058:current-user-id`).

2. **Assign TC-8001 to the current user:**

   ```
   jira.edit_issue("TC-8001", assignee=<current-user-account-id>)
   ```

   The issue is currently Unassigned. This assigns it to the active triager.

3. **Discover the target transition dynamically:**

   ```
   jira.get_transitions("TC-8001")
   ```

   Select the transition whose target status name is `"Assigned"`. The transition
   ID is not hardcoded -- it is discovered from the available transitions on this
   Vulnerability issue's workflow.

4. **Transition to Assigned:**

   TC-8001 is currently in **New** status. After discovering the Assigned
   transition ID from the transitions list:

   ```
   jira.transition_issue("TC-8001", <assigned-transition-id>)
   ```

   This moves the issue from New to Assigned, signaling that triage is underway.

---

# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 (versions before 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Due date | 2026-07-15 |
| Assignee | Unassigned (prior to Step 0.7) |
| Status | New (prior to Step 0.7) |

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the
**2.2.x** version stream configured in Security Configuration:

- Stream suffix: `[rhtpa-2.2]` -> stream **2.2.x**
- Konflux Release Repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`
- Local Path: `/home/dev/repos/rhtpa-release.0.4.z`

This issue is **stream-scoped** to the 2.2.x stream. Steps 3 and 4 will be
scoped to this stream (Affects Versions correction includes only 2.2.x versions;
sibling detection checks for same-stream vs cross-stream issues).

## Ecosystem Detection

The vulnerable library **quinn-proto** is a Rust crate. The Ecosystem Mappings
table in the 2.2.x stream's security-matrix.md lists **Cargo** as a supported
ecosystem with:

- Repository: backend
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z`

Ecosystem: **Cargo** (source dependency)

This means remediation will follow the two-task path: upstream backport task
(fix in source repo) + downstream propagation subtask (update reference in
Konflux release repo).

## Deployment Context Lookup

The Source Repositories table in Security Configuration does not include a
Deployment Context column. Per backward compatibility rules, all repositories
default to `upstream`. Coordination guidance will be omitted from remediation
task descriptions.
