# Step 2 -- Version Impact Analysis: TC-8004

## Vulnerability Details

- **CVE**: CVE-2026-33501
- **Library**: h2
- **Affected range**: < 0.4.8
- **Fixed version**: 0.4.8

## Version Impact Table

Since the issue is **unscoped** (no stream suffix), ALL versions across ALL configured streams are analyzed.

| Stream | Version | Build Tag | h2 Version (from Cargo.lock) | Affected? | Evidence |
|--------|---------|-----------|------------------------------|-----------|----------|
| 2.1.x | 2.1.0 | `v0.3.8` | 0.4.5 | **YES** | 0.4.5 < 0.4.8 -- within vulnerable range |
| 2.1.x | 2.1.1 | `v0.3.12` | 0.4.5 | **YES** | 0.4.5 < 0.4.8 -- within vulnerable range |
| 2.2.x | 2.2.0 | `v0.4.5` | 0.4.8 | NO | 0.4.8 >= 0.4.8 -- ships the fixed version |
| 2.2.x | 2.2.1 | `v0.4.8` | 0.4.8 | NO | 0.4.8 >= 0.4.8 -- ships the fixed version |
| 2.2.x | 2.2.2 | `v0.4.9` | _(retag of v0.4.8)_ | NO | Same as 2.2.1 (retag) -- not affected |
| 2.2.x | 2.2.3 | `v0.4.11` | 0.4.9 | NO | 0.4.9 >= 0.4.8 -- ships a version past the fix |
| 2.2.x | 2.2.4 | `v0.4.12` | 0.4.9 | NO | 0.4.9 >= 0.4.8 -- ships a version past the fix |

## Impact Summary

- **Affected streams**: 2.1.x only
- **Affected versions**: RHTPA 2.1.0, RHTPA 2.1.1
- **Not affected streams**: 2.2.x (all versions ship h2 >= 0.4.8)
- **Mixed impact**: YES -- 2.1.x versions are affected while 2.2.x versions are not

The 2.1.x stream ships h2 0.4.5, which is within the vulnerable range (< 0.4.8). The 2.2.x stream ships h2 0.4.8 or later, which includes the fix. This is a clear split: only the older 2.1.x stream requires remediation.

## Lock File Evidence

### 2.1.x stream (rhtpa-release.0.3.z)

**v0.3.8 (RHTPA 2.1.0)**:
```
git show v0.3.8:Cargo.lock | grep -A2 'name = "h2"'
name = "h2"
version = "0.4.5"
```

**v0.3.12 (RHTPA 2.1.1)**:
```
git show v0.3.12:Cargo.lock | grep -A2 'name = "h2"'
name = "h2"
version = "0.4.5"
```

### 2.2.x stream (rhtpa-release.0.4.z)

**v0.4.5 (RHTPA 2.2.0)**:
```
git show v0.4.5:Cargo.lock | grep -A2 'name = "h2"'
name = "h2"
version = "0.4.8"
```

**v0.4.8 (RHTPA 2.2.1)**:
```
git show v0.4.8:Cargo.lock | grep -A2 'name = "h2"'
name = "h2"
version = "0.4.8"
```

**v0.4.9 (RHTPA 2.2.2)**: retag of v0.4.8 -- same as RHTPA 2.2.1 (h2 0.4.8, not affected)

**v0.4.11 (RHTPA 2.2.3)**:
```
git show v0.4.11:Cargo.lock | grep -A2 'name = "h2"'
name = "h2"
version = "0.4.9"
```

**v0.4.12 (RHTPA 2.2.4)**:
```
git show v0.4.12:Cargo.lock | grep -A2 'name = "h2"'
name = "h2"
version = "0.4.9"
```

## Upstream Fix Status

- **Upstream fix PR**: [hyperium/h2#812](https://github.com/hyperium/h2/pull/812)
- The fix was included in h2 0.4.8, which adds a configurable maximum header list size (defaulting to 16 KiB) to prevent memory exhaustion via CONTINUATION frames.
- The 2.2.x stream already ships h2 >= 0.4.8, confirming the fix is present in that stream.
- The 2.1.x stream ships h2 0.4.5, which does not include the fix.
