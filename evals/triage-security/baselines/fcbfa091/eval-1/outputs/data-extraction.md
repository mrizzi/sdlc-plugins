# Step 0.7 -- Assign and Transition to Assigned

**PROPOSAL: Assign TC-8001 to the current user and transition to Assigned status.**

The following Jira mutations are proposed (pending confirmation):

1. **Retrieve current user account ID:**
   ```
   jira.user_info()
   ```

2. **Assign the issue to the current user:**
   ```
   jira.edit_issue("TC-8001", assignee=<current-user-account-id>)
   ```
   Rationale: TC-8001 is currently Unassigned. Assigning provides visibility
   into who is actively triaging this CVE and enables concurrent triage
   detection in Step 7.

3. **Discover the Assigned transition:**
   ```
   jira.get_transitions("TC-8001")
   ```
   Select the transition whose target status name is "Assigned". Do not
   hardcode a transition ID -- Vulnerability issues use a different Jira
   workflow than Task issues.

4. **Transition from New to Assigned:**
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
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Due date | 2026-07-15 |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the
**2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`).

This issue is **stream-scoped** to 2.2.x. Steps 3 and 8 will only apply
to versions in the 2.2.x stream. Cross-stream impact on 2.1.x will be
reported via Case B in Step 8.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The Ecosystem Mappings
table in both streams' security-matrix.md files lists **Cargo** as the
ecosystem with:
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Repository: backend

This is a **source dependency ecosystem** (Cargo), which means remediation
requires two tasks per affected stream: an upstream backport task and a
downstream propagation subtask.

## Deployment Context

The affected repository `rhtpa-backend` is listed in the Source Repositories
table without a Deployment Context column. Per backward compatibility rules,
the deployment context defaults to `upstream`.
