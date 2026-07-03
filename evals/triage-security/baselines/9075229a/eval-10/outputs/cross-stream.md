# Cross-Stream Impact: TC-8020 (CVE-2026-55123)

## Cross-Stream Impact Comment

The following comment would be posted to TC-8020 per Step 8, Case B:

---

Cross-stream impact: tokio < 1.42.0 also affects stream 2.1.x based on lock file analysis.

| Stream | Versions Affected | tokio version | Sibling CVE Jira? |
|--------|-------------------|---------------|-------------------|
| 2.1.x (rhtpa-2.1) | RHTPA 2.1.0, RHTPA 2.1.1 | 1.40.0 | **No** -- no CVE Jira exists |

This stream does not have a companion CVE Vulnerability issue and may require separate PSIRT triage.

---

## Sibling CVE Jira Search

**JQL query:**
```
project = TC AND issuetype = 10024 AND labels = CVE-2026-55123 AND summary ~ "[rhtpa-2.1]"
```

**Result:** No results -- no sibling Vulnerability issue exists for CVE-2026-55123 in stream rhtpa-2.1.

**Action:** Since no CVE Jira exists for stream 2.1.x, preemptive remediation tasks are created (Case B).

## Preemptive Task Details

The following preemptive tasks would be created for stream 2.1.x:

| Task | Type | Summary | Labels | Link to TC-8020 |
|------|------|---------|--------|-----------------|
| Upstream backport (2.1.x) | Task | Remediate CVE-2026-55123: bump tokio to 1.42.0 (2.1.x) | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | Related |
| Downstream propagation (2.1.x) | Task | Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.3.z (2.1.x) | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | Related |

### Key differences from standard remediation tasks (Case A):

1. **Labels**: Include `security-preemptive` alongside standard labels
2. **Link type**: "Related" (not "Depend") to originating CVE Jira TC-8020
3. **Description prefix**: Each task description includes the preemptive remediation note:
   > **Preemptive remediation**: This task was created proactively from cross-stream
   > impact analysis of TC-8020 (stream rhtpa-2.2).
   > No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
   > this task will be linked and the `security-preemptive` label removed.

### Upstream backport task (2.1.x)

- **Repository**: backend
- **Target branch**: release/0.3.z
- **Action**: Bump tokio to >= 1.42.0 in Cargo.lock
- **Affected versions**: RHTPA 2.1.0 (v0.3.8), RHTPA 2.1.1 (v0.3.12)

### Downstream propagation task (2.1.x)

- **Repository**: rhtpa-release.0.3.z
- **Target branch**: main
- **Source pinning method**: artifacts.lock.yaml (download URL contains tag)
- **Action**: Update backend reference after upstream backport merges
- **Blocked by**: Upstream backport task (2.1.x)

## Preemptive Task Comment on TC-8020

The following comment would be posted to TC-8020 after preemptive task creation:

---

Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: upstream backport task key (security-preemptive)
- 2.1.x: downstream propagation task key (security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.

---

## Reconciliation (Step 4.4)

When PSIRT later creates a CVE Jira for stream rhtpa-2.1, the triage-security
skill's Step 4.4 (Preemptive Task Reconciliation) will:

1. Search for existing tasks with label `security-preemptive` and CVE label `CVE-2026-55123`
2. Find the preemptive tasks created here
3. Re-link them from the originating CVE (TC-8020) to the new stream-specific CVE Jira using "Depend"
4. Remove the `security-preemptive` label
5. Post a reconciliation comment on both the new CVE Jira and TC-8020
