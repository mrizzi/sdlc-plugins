# Version Impact Analysis: TC-8002

## Vulnerability Threshold

- **Package:** serde_json
- **Vulnerable range:** < 1.0.135
- **Fix version:** 1.0.135

## Stream 1: rhtpa-release.0.3.z (2.1.x product stream)

| Product Version | Build | Build Date | Build Tag | serde_json Version | Affected? |
|----------------|-------|------------|-----------|-------------------|-----------|
| 2.1.0          | 0.3.8 | 2025-09-15 | v0.3.8    | 1.0.137           | **No** -- ships fix (>= 1.0.135) |
| 2.1.1          | 0.3.12| 2025-11-20 | v0.3.12   | 1.0.137           | **No** -- ships fix (>= 1.0.135) |

**Stream 1 verdict: NOT AFFECTED.** All 2.1.x versions ship serde_json 1.0.137, which is above the fix threshold of 1.0.135.

## Stream 2: rhtpa-release.0.4.z (2.2.x product stream)

| Product Version | Build | Build Date | Build Tag | serde_json Version | Affected? |
|----------------|-------|------------|-----------|-------------------|-----------|
| 2.2.0          | 0.4.5 | 2025-12-03 | v0.4.5    | 1.0.138           | **No** -- ships fix (>= 1.0.135) |
| 2.2.1          | 0.4.8 | 2026-02-05 | v0.4.8    | 1.0.138           | **No** -- ships fix (>= 1.0.135) |
| 2.2.2          | 0.4.9 | 2026-02-23 | v0.4.8    | 1.0.138 (retag)   | **No** -- ships fix (>= 1.0.135) |
| 2.2.3          | 0.4.11| 2026-03-23 | v0.4.11   | 1.0.139           | **No** -- ships fix (>= 1.0.135) |
| 2.2.4          | 0.4.12| 2026-05-04 | v0.4.12   | 1.0.139           | **No** -- ships fix (>= 1.0.135) |

**Stream 2 verdict: NOT AFFECTED.** All 2.2.x versions ship serde_json >= 1.0.138, which is above the fix threshold of 1.0.135.

## Overall Impact Summary

| Stream | Versions Checked | Lowest serde_json | Affected Count | Verdict |
|--------|-----------------|-------------------|----------------|---------|
| 2.1.x  | 2               | 1.0.137           | 0              | Not affected |
| 2.2.x  | 5               | 1.0.138           | 0              | Not affected |
| **Total** | **7**        | **1.0.137**       | **0**          | **Not affected** |

**Conclusion:** Zero supported versions across all streams ship a vulnerable version of serde_json. The lowest version found in any build is 1.0.137, which is two patch releases above the fix version (1.0.135). The vulnerability was never present in any shipped build of RHTPA.
