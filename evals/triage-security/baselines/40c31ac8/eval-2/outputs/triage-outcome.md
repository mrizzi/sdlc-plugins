# Triage Outcome -- TC-8002 (CVE-2026-28940)

## Decision: Case C -- No Supported Versions Affected

### Rationale

The version impact analysis shows that **no supported version** ships a vulnerable version of serde_json. The CVE affects serde_json versions before 1.0.135, but every released version across both the 2.1.x and 2.2.x streams ships serde_json 1.0.137 or later:

- Stream 2.1.x: all versions ship serde_json 1.0.137
- Stream 2.2.x: all versions ship serde_json 1.0.138 or 1.0.139

The fix threshold (1.0.135) is exceeded by every shipped version. The vulnerability was never present in any supported product release.

### Recommendation: Close as Not a Bug

The issue should be closed with resolution "Not a Bug" (not affected).

### Proposed Jira Actions

The following Jira mutations would be performed (each requiring engineer confirmation):

#### 1. Affects Versions Correction (Step 3)

The current Affects Versions field lists `RHTPA 2.2.0`, but lock file analysis shows RHTPA 2.2.0 ships serde_json 1.0.138 (not affected). Since no versions are affected, Affects Versions should be cleared or left as-is for the close action.

**Current:** RHTPA 2.2.0
**Proposed:** No versions affected -- Affects Versions will be addressed by closing the issue.

#### 2. Post Triage Comment (Step 8, Case C)

Add comment to TC-8002:

> No supported versions ship a vulnerable version of serde_json. Version impact analysis:
>
> | Stream | Version | serde_json | Affected? |
> |--------|---------|------------|-----------|
> | 2.1.x | 2.1.0 | 1.0.137 | NO |
> | 2.1.x | 2.1.1 | 1.0.137 | NO |
> | 2.2.x | 2.2.0 | 1.0.138 | NO |
> | 2.2.x | 2.2.1 | 1.0.138 | NO |
> | 2.2.x | 2.2.2 | -- (retag) | NO |
> | 2.2.x | 2.2.3 | 1.0.139 | NO |
> | 2.2.x | 2.2.4 | 1.0.139 | NO |
>
> All supported versions ship serde_json >= 1.0.137, which is outside the affected range (before 1.0.135). CVE-2026-28940 does not affect this product.

#### 3. Set VEX Justification

Set `customfield_12345` (VEX Justification) to **"Component not Present"** -- the vulnerable version of serde_json is not included in any supported product version. Although serde_json is present as a dependency, the vulnerable version (before 1.0.135) was never shipped.

#### 4. Transition to Closed

Transition TC-8002 to **Closed** with resolution **"Not a Bug"**.

#### 5. Add ai-cve-triaged Label

Add the `ai-cve-triaged` label to TC-8002 to mark it as triaged and prevent re-triage.

#### 6. Post-Triage Summary Comment

Post a summary comment to TC-8002 with:
- Version impact table (as above)
- Triage outcome: Closed as Not a Bug -- no supported versions affected
- VEX Justification: Component not Present
- @mention of the issue reporter (PSIRT analyst)

### Steps Not Applicable

- **Step 4 (Duplicate/Sibling Check):** Would be performed via JQL search but no remediation actions depend on it since no versions are affected.
- **Step 5 (Lifecycle Check):** Not relevant -- no affected versions to check lifecycle status for.
- **Step 6 (Already Fixed Check):** Not applicable -- the vulnerability was never present, so "already fixed" is not the correct classification. Case C (not affected) is the correct path.
- **Step 7 (Concurrent Triage Detection):** Upstream Affected Component custom field not configured -- step skipped.
- **Step 8 Remediation Task Creation:** No remediation tasks needed -- no versions are affected.

### Cross-Stream Impact

No cross-stream remediation needed. Both the 2.1.x and 2.2.x streams already ship non-vulnerable versions of serde_json. No preemptive remediation tasks are required.
