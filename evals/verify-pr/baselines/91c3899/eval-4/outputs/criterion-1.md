# Criterion 1: `PackageSummary` includes a `vulnerability_count: i64` field

## Verdict: PASS

## Reasoning

The PR diff in `modules/fundamental/src/package/model/summary.rs` adds the following lines to the `PackageSummary` struct:

```rust
/// Number of known vulnerability advisories affecting this package.
pub vulnerability_count: i64,
```

This directly satisfies the criterion. The field is public, has the correct type (`i64`), and includes a documentation comment explaining its purpose.

## Evidence

- File: `modules/fundamental/src/package/model/summary.rs`
- Added lines: `/// Number of known vulnerability advisories affecting this package.` and `pub vulnerability_count: i64,`
- The field is added within the `PackageSummary` struct definition alongside existing fields (`name`, `version`, `license`).
