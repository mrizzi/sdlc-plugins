# Criterion 1

**Text:** `PackageSummary` includes a `vulnerability_count: i64` field

**Classification:** LEGITIMATE

## Evidence

In the diff for `modules/fundamental/src/package/model/summary.rs`:

```rust
+    /// Number of known vulnerability advisories affecting this package.
+    pub vulnerability_count: i64,
```

The field is added to the `PackageSummary` struct with the correct type `i64` and includes a documentation comment. The field is also populated (albeit with a hardcoded value) in the service layer mapping in `modules/fundamental/src/package/service/mod.rs`.

## Verdict: PASS

The struct-level requirement is satisfied. The field exists with the correct name and type.
