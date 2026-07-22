# Step 0.7 -- Early Assignment Actions

## 1. Retrieve current user's Jira account ID

```
jira.user_info()
```

Result: current user account ID (e.g., `712020:current-user-id`)

## 2. Assign the issue to the current user

```
jira.edit_issue("TC-8001", assignee="712020:current-user-id")
```

TC-8001 is currently Unassigned. This assigns it to the current user to provide
visibility into who is actively triaging the issue.

## 3. Discover the target transition dynamically

```
jira.get_transitions("TC-8001")
```

Select the transition whose target status name is `"Assigned"`. Do not hardcode
a transition ID -- Vulnerability issues use a different Jira workflow than Task
issues.

## 4. Transition to Assigned

```
jira.transition_issue("TC-8001", <assigned-transition-id>)
```

TC-8001 is currently in `New` status, so the transition to `Assigned` proceeds.

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
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x**
version stream (Konflux release repo: `rhtpa-release.0.4.z`).

This issue is **scoped** to stream 2.2.x. Steps 3 and 8 will only include
versions belonging to the 2.2.x stream. Other affected streams (2.1.x) will
be addressed via Case B cross-stream impact.

## Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. This maps to the
**Cargo** ecosystem. The lock file is `Cargo.lock` and the check command is
`git show <tag>:Cargo.lock`.

## Deployment Context

The affected repository `rhtpa-backend` has no explicit Deployment Context
column in the Source Repositories table. Defaulting to `upstream`.
