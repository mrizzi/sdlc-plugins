# Triage Outcome: TC-8002 (CVE-2026-28940)

## Decision: Close as Not Affected

### Rationale

CVE-2026-28940 affects serde_json versions **before 1.0.135**. Analysis of all shipped product versions across both supported streams (2.1.x and 2.2.x) shows that every build includes serde_json at version **1.0.137 or higher**, well above the fix threshold.

The vulnerability was patched in upstream serde_json 1.0.135. Since the earliest product build (2.1.0, backend tag v0.3.8, built 2025-09-15) already ships serde_json 1.0.137, the fix predates all shipped versions. No product release has ever been exposed to this vulnerability.

### VEX Justification

**vulnerable_code_not_present** -- The vulnerable version of serde_json (< 1.0.135) was never included in any shipped product build. All builds across all supported streams ship a version that already contains the fix.

### Proposed Jira Actions

1. **Transition TC-8002** from "New" to "Closed" (or the equivalent terminal status)
2. **Set Resolution** to "Not a Bug" / "Won't Fix" (the product was never affected)
3. **Set VEX Justification field** (customfield_12345) to: `vulnerable_code_not_present`
4. **Add comment** to TC-8002 with the following text:

   > **Triage analysis: Not Affected**
   >
   > CVE-2026-28940 affects serde_json versions before 1.0.135. All shipped builds across both supported version streams (2.1.x and 2.2.x) include serde_json >= 1.0.137, which already contains the fix.
   >
   > | Stream | Earliest serde_json shipped | Fix threshold |
   > |--------|---------------------------|---------------|
   > | 2.1.x | 1.0.137 | 1.0.135 |
   > | 2.2.x | 1.0.138 | 1.0.135 |
   >
   > VEX justification: `vulnerable_code_not_present`
   >
   > Closing as not affected -- no remediation required.

5. **Remove Affects Version** "RHTPA 2.2.0" (since 2.2.0 is confirmed not affected)

### No Remediation Required

Since no shipped version is vulnerable, no patch, rebuild, or advisory is needed. No downstream consumers need to take action.
