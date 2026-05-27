# Criterion 1: `PackageSummary` includes a `vulnerability_count: i64` field

## Verdict: PASS

## Evidence

In the diff for `modules/fundamental/src/package/model/summary.rs`:

```rust
+    /// Number of known vulnerability advisories affecting this package.
+    pub vulnerability_count: i64,
```

The field is added to the `PackageSummary` struct with the correct type `i64` and includes a doc comment explaining its purpose. This matches the acceptance criterion exactly.
