# Step 8 -- Remediation

## Triage Outcome

### Scoped Stream (2.2.x): Case C -- No Supported Versions Affected

The version impact analysis shows that **no versions** in the scoped stream (2.2.x) ship a vulnerable version of h2. All 2.2.x versions ship h2 >= 0.4.8, which is at or above the fix threshold.

**Recommendation**: Close TC-8030 as Not a Bug (not affected).

**Proposed actions** (pending engineer confirmation):

1. **Add comment** to TC-8030:

   > No supported versions in stream 2.2.x ship a vulnerable version of h2.
   > Version impact analysis:
   >
   > | Version | h2 version | Affected? |
   > |---------|------------|-----------|
   > | 2.2.0 | 0.4.8 | NO |
   > | 2.2.1 | 0.4.8 | NO |
   > | 2.2.2 | -- | NO (retag of 2.2.1) |
   > | 2.2.3 | 0.4.9 | NO |
   > | 2.2.4 | 0.4.9 | NO |
   >
   > All supported versions ship h2 0.4.8 or later, which is outside the affected range (< 0.4.8).
   > Fix threshold source: MITRE CVE API (lessThan 0.4.8), cross-validated with OSV.dev (fixed 0.4.8).

2. **Transition** TC-8030 to Closed with resolution "Not a Bug".

3. **Set VEX Justification** (customfield_12345): "Component not Present" -- the vulnerable version of h2 (< 0.4.8) is not shipped in any 2.2.x version. All versions include the fixed version (0.4.8+).

4. **Add label**: `ai-cve-triaged` to TC-8030.

### Cross-Stream Impact (2.1.x): Case B -- Proactive Remediation

The version impact analysis reveals that stream **2.1.x** (outside this issue's scope) IS affected:
- 2.1.0: h2 0.4.5 (AFFECTED)
- 2.1.1: h2 0.4.5 (AFFECTED)

**Cross-stream impact comment** (to be posted on TC-8030):

> Cross-stream impact: h2 < 0.4.8 also affects stream 2.1.x based on lock file analysis.
> All 2.1.x versions (2.1.0, 2.1.1) ship h2 0.4.5, which is within the affected range.
> This stream is tracked by a companion issue (see Related links) or may require separate PSIRT triage.

**Preemptive remediation tasks for 2.1.x** (if no existing CVE Jira for 2.1.x):

Since h2 is a Cargo (source dependency) ecosystem, two tasks are created:

#### Task 1: Upstream Backport -- Bump h2 to >= 0.4.8 on release/0.3.z

**Summary**: CVE-2026-48901: bump h2 >= 0.4.8 on release/0.3.z [rhtpa-2.1] [security-preemptive]

**Labels**: `security`, `security-preemptive`, `CVE-2026-48901`

**Link**: Related to TC-8030 (originating CVE Jira)

**Description**:

> **Preemptive remediation** -- created from triage of TC-8030 (stream 2.2.x).
> Stream 2.1.x does not yet have its own CVE Jira for CVE-2026-48901.
> When PSIRT creates a stream-specific CVE Jira, Step 4.4 reconciliation will link it and remove the security-preemptive label.
>
> ## Context
>
> CVE-2026-48901 affects h2 versions < 0.4.8 (HTTP/2 CONTINUATION flood vulnerability).
> Stream 2.1.x ships h2 0.4.5 via the backend repository (Cargo.lock).
> Upstream fix: [hyperium/h2#800](https://github.com/hyperium/h2/pull/800)
>
> ## Task
>
> Bump the h2 dependency to >= 0.4.8 in the backend repository on the `release/0.3.z` branch.
>
> 1. Update `Cargo.toml` to require h2 >= 0.4.8
> 2. Run `cargo update -p h2` to update `Cargo.lock`
> 3. Verify the build compiles and tests pass
> 4. Open a PR against `release/0.3.z`
>
> ## References
>
> - Advisory: [GHSA-2026-r7f2-kk9p](https://github.com/advisories/GHSA-2026-r7f2-kk9p)
> - Upstream fix PR: [hyperium/h2#800](https://github.com/hyperium/h2/pull/800)
> - CVE record: [CVE-2026-48901](https://www.cve.org/CVERecord?id=CVE-2026-48901)
> - Fix threshold: h2 >= 0.4.8 (source: MITRE CVE API + OSV.dev, cross-validated)

#### Task 2: Downstream Propagation -- Update backend tag in rhtpa-release.0.3.z

**Summary**: CVE-2026-48901: propagate h2 fix to rhtpa-release.0.3.z [rhtpa-2.1] [security-preemptive]

**Labels**: `security`, `security-preemptive`, `CVE-2026-48901`

**Link**: Related to TC-8030 (originating CVE Jira); Blocked by Task 1 (upstream backport)

**Description**:

> **Preemptive remediation** -- created from triage of TC-8030 (stream 2.2.x).
> This task is blocked by the upstream backport task.
>
> ## Context
>
> After the upstream backport bumps h2 to >= 0.4.8 on `release/0.3.z`, the Konflux release repo must be updated to reference the new backend tag.
>
> ## Task
>
> Update the backend source reference in `artifacts.lock.yaml` in the rhtpa-release.0.3.z repo to point to the new backend tag that includes h2 >= 0.4.8.
>
> 1. Wait for the upstream backport PR to merge and a new tag to be created
> 2. Update `artifacts.lock.yaml` to reference the new backend tag
> 3. Trigger a Konflux rebuild
> 4. Verify the rebuilt image ships h2 >= 0.4.8
>
> ## References
>
> - Upstream backport task: (link to Task 1)
> - Current backend tag in 2.1.1: v0.3.12 (h2 0.4.5 -- affected)
> - Source pinning method: artifacts.lock.yaml (download URL contains tag)

## Summary of Remediation Actions

| Action | Target | Details |
|--------|--------|---------|
| Close as Not a Bug | TC-8030 (2.2.x) | No 2.2.x versions affected; all ship h2 >= 0.4.8 |
| Set VEX Justification | TC-8030 | Component not Present (vulnerable h2 version not shipped) |
| Cross-stream comment | TC-8030 | 2.1.x affected (h2 0.4.5 < 0.4.8) |
| Preemptive upstream task | 2.1.x | Bump h2 >= 0.4.8 on release/0.3.z (security-preemptive) |
| Preemptive downstream task | 2.1.x | Propagate fix to rhtpa-release.0.3.z (security-preemptive, blocked by upstream) |
| Add label | TC-8030 | ai-cve-triaged |
