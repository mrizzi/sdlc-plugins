# Cross-Stream Impact — CVE-2026-55123 (tokio)

## Cross-Stream Impact Comment

The following comment would be posted to TC-8020:

---

Cross-stream impact: tokio < 1.42.0 also affects stream rhtpa-2.1 based on lock file analysis.

| Version     | Stream    | tokio version | Affected? |
|-------------|-----------|---------------|-----------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0        | YES       |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0        | YES       |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1        | YES       |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1        | YES       |

Stream rhtpa-2.1 does not have its own CVE Jira for CVE-2026-55123.
Preemptive remediation tasks have been created (see below).

---

## Sibling CVE Jira Check

- JQL: `project = TC AND labels = 'CVE-2026-55123' AND issuetype = 10024 AND key != TC-8020`
- Results for stream rhtpa-2.1: **No results** — no CVE Jira exists for this stream
- Action: Create preemptive remediation tasks for rhtpa-2.1 (Case B)

## Preemptive Task Details

Since no CVE Jira exists for stream rhtpa-2.1, preemptive remediation tasks are created
with the `security-preemptive` label and linked to TC-8020 via "Related" (not "Depend").

### Preemptive Tasks Created

| Task | Type | Stream | Summary | Labels |
|------|------|--------|---------|--------|
| (new) | Upstream backport | rhtpa-2.1 | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | ai-generated-jira, Security, CVE-2026-55123, security-preemptive |
| (new) | Downstream propagation | rhtpa-2.1 | Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1) | ai-generated-jira, Security, CVE-2026-55123, security-preemptive |

### Preemptive Task Linkage

- Both preemptive tasks are linked to TC-8020 with link type **Related** (not Depend)
  because the originating CVE Jira belongs to stream rhtpa-2.2, not rhtpa-2.1
- The downstream propagation subtask is blocked by the upstream backport task (link type: Blocks)
- When PSIRT creates a stream-specific CVE Jira for rhtpa-2.1, Step 4.4 (preemptive task
  reconciliation) will:
  1. Link the new CVE Jira to the preemptive tasks with "Depend"
  2. Remove the `security-preemptive` label from the tasks

### Preemptive Comment on TC-8020

The following comment would be posted to TC-8020 documenting the preemptive tasks:

---

Preemptive remediation tasks created for streams without CVE Jiras:
- rhtpa-2.1: upstream backport task (security-preemptive) — Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)
- rhtpa-2.1: downstream propagation task (security-preemptive) — Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.

---

## Reconciliation Path

When PSIRT creates a CVE Jira for stream rhtpa-2.1 (e.g., TC-XXXX with summary
"CVE-2026-55123 tokio - Use-after-free in task abort [rhtpa-2.1]"), triaging that
issue will trigger Step 4.4 (preemptive task reconciliation):

1. JQL search finds the preemptive tasks (label `security-preemptive` + `CVE-2026-55123`)
2. Filter matches tasks whose summary contains `(rhtpa-2.1)`
3. Link the new CVE Jira to each preemptive task with "Depend"
4. Remove `security-preemptive` label from each task
5. Skip new remediation task creation in Step 8 (tasks already exist)
