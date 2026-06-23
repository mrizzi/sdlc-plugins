# Step 2 -- Version Impact Analysis: CVE-2026-28940

## Scoped Stream: 2.2.x

This issue is scoped to the 2.2.x stream per the summary suffix `[rhtpa-2.2]`. However, per the skill's rules (check ALL supported versions), both streams are analyzed for completeness and cross-stream impact assessment.

## Version Impact Table

Version Impact for CVE-2026-28940 (serde_json < 1.0.135):

| Version | Stream | Build Tag | serde_json version | Affected? | Notes |
|---------|--------|-----------|-------------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 1.0.137 | NO | Ships patched version (>= 1.0.135) |
| 2.1.1 | 2.1.x | v0.3.12 | 1.0.137 | NO | Ships patched version (>= 1.0.135) |
| 2.2.0 | 2.2.x | v0.4.5 | 1.0.138 | NO | Ships patched version (>= 1.0.135) |
| 2.2.1 | 2.2.x | v0.4.8 | 1.0.138 | NO | Ships patched version (>= 1.0.135) |
| 2.2.2 | 2.2.x | v0.4.9 | 1.0.138 | NO | Retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | v0.4.11 | 1.0.139 | NO | Ships patched version (>= 1.0.135) |
| 2.2.4 | 2.2.x | v0.4.12 | 1.0.139 | NO | Ships patched version (>= 1.0.135) |

## Analysis

The CVE affects serde_json versions **before 1.0.135**. The fixed version is **1.0.135**.

Every supported product version -- across both the 2.1.x and 2.2.x streams -- ships serde_json **1.0.137 or later**, which is well above the fix threshold of 1.0.135. No supported version has ever shipped a vulnerable version of serde_json for this CVE.

### Scoped stream (2.2.x) summary

All five versions in the 2.2.x stream (2.2.0 through 2.2.4) ship serde_json 1.0.138 or 1.0.139. None are affected.

### Cross-stream (2.1.x) summary

Both versions in the 2.1.x stream (2.1.0 and 2.1.1) ship serde_json 1.0.137. Neither is affected.

## Upstream Fix Status

Not applicable -- no versions are affected, so upstream fix status is moot. For reference, the upstream `release/0.4.z` branch would be checked at HEAD for the 2.2.x stream's Cargo ecosystem, but since no versions ship a vulnerable serde_json, no remediation is needed.

## Conclusion

**No supported versions are affected.** All versions ship serde_json >= 1.0.137, which is above the CVE's fix threshold of 1.0.135. This is a Case C outcome (no supported versions affected).
