# Step 0.7 -- Assign and Transition to Assigned

Before extracting data, assign TC-8020 to the current user and transition to Assigned status:

1. **Retrieve current user's Jira account ID**:
   ```
   jira.user_info()
   ```

2. **Assign the issue to the current user**:
   ```
   jira.edit_issue("TC-8020", assignee=<current-user-account-id>)
   ```

3. **Discover the target transition dynamically**:
   ```
   jira.get_transitions("TC-8020")
   ```
   Select the transition whose target status name is "Assigned".

4. **Transition to Assigned** (issue is currently in New status):
   ```
   jira.transition_issue("TC-8020", <assigned-transition-id>)
   ```

# Step 1 -- Data Extraction for TC-8020

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 |
| Vulnerable library | tokio |
| Affected version range | versions before 1.42.0 |
| Fixed version | 1.42.0 |
| CVSS | 8.1 (High) |
| Upstream fix PR | https://github.com/tokio-rs/tokio/pull/7001 |
| Advisory URL | https://github.com/advisories/GHSA-2026-tk91-v5pp |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-55123 |
| Due date | 2026-08-15 |
| Existing comments | None |
| Upstream Affected Component | tokio (customfield_10632) |
| PS Component | pscomponent:org/rhtpa-server (customfield_10669) |
| Stream | rhtpa-2.2 (customfield_10832) |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Version Streams configuration:

- Stream suffix: `[rhtpa-2.2]` -> stream `2.2.x`
- Konflux Release Repo: git.example.com/rhtpa/rhtpa-release.0.4.z
- Local Path: /home/dev/repos/rhtpa-release.0.4.z

This issue is **scoped** to stream rhtpa-2.2. Steps 3 and 8 will apply only to this stream's versions. However, Step 2 checks ALL streams to detect cross-stream impact.

## Ecosystem Detection

The vulnerable library **tokio** is a Rust crate. Based on the Ecosystem Mappings in security-matrix.md, the ecosystem is **Cargo**:

- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch (2.1.x): `release/0.3.z`
- Upstream Branch (2.2.x): `release/0.4.z`

## Deployment Context Lookup

The affected repository `rhtpa-backend` is found in the Source Repositories table. Deployment context defaults to `upstream` (no Deployment Context column configured).
