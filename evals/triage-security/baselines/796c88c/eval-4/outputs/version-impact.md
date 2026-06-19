# Version Impact Analysis — TC-8004

## CVE-2026-33501: h2 < 0.4.8

**Vulnerability condition**: h2 version < 0.4.8
**Fixed version**: h2 >= 0.4.8

Since the issue is **UNSCOPED** (no stream suffix), all versions across all streams are checked.

## Version Impact Table

| Stream | Version | Build Tag | h2 Version | Vulnerable (< 0.4.8)? | Affected? |
|--------|---------|-----------|------------|------------------------|-----------|
| 2.1.x | RHTPA 2.1.0 | `v0.3.8` | 0.4.5 | YES | **YES** |
| 2.1.x | RHTPA 2.1.1 | `v0.3.12` | 0.4.5 | YES | **YES** |
| 2.2.x | RHTPA 2.2.0 | `v0.4.5` | 0.4.8 | NO (= 0.4.8) | NO |
| 2.2.x | RHTPA 2.2.1 | `v0.4.8` | 0.4.8 | NO (= 0.4.8) | NO |
| 2.2.x | RHTPA 2.2.2 | `v0.4.9` | 0.4.8 (retag of v0.4.8) | NO (= 0.4.8) | NO |
| 2.2.x | RHTPA 2.2.3 | `v0.4.11` | 0.4.9 | NO (> 0.4.8) | NO |
| 2.2.x | RHTPA 2.2.4 | `v0.4.12` | 0.4.9 | NO (> 0.4.8) | NO |

## Stream Impact Summary

| Stream | Affected? | Details |
|--------|-----------|---------|
| **2.1.x** | **YES** | All versions (2.1.0, 2.1.1) ship h2 0.4.5, which is < 0.4.8 |
| **2.2.x** | **NO** | All versions ship h2 >= 0.4.8 (already patched) |

## Notes

- **RHTPA 2.2.2** (build 0.4.9, tag `v0.4.8`): This is a retag of the 2.2.1 backend build. The h2 version carries forward from 2.2.1 as 0.4.8 — not affected.
- The 2.2.x stream has shipped the fix since its first release (2.2.0), meaning the h2 vulnerability was resolved upstream before the 2.2.x stream was cut.
- Mixed impact: only the 2.1.x stream requires remediation.
