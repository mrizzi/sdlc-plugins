# Criterion 2: Packages with no vulnerabilities show `vulnerability_count: 0`

## Criterion Text
Packages with no vulnerabilities show `vulnerability_count: 0`

## Verdict: FAIL

## Reasoning

While the diff does show that `vulnerability_count` is hardcoded to `0` in the service layer (`modules/fundamental/src/package/service/mod.rs`):

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

This is problematic for two reasons:

1. The value is **hardcoded to 0 for ALL packages**, not just packages with no vulnerabilities. The `// TODO: implement subquery` comment explicitly acknowledges that the actual computation has not been implemented yet.

2. The task requires that packages with no vulnerabilities show `vulnerability_count: 0` as part of a working system where the count is **computed** from the database. A hardcoded zero does technically show zero for packages without vulnerabilities, but it also shows zero for packages **with** vulnerabilities, which means the system is not actually functional.

The intent of this criterion is that the vulnerability count computation works correctly and produces `0` when there are no vulnerabilities. Since the computation is not implemented (hardcoded to 0 with a TODO), this criterion cannot be considered met in a meaningful way. It only appears to pass because the entire feature is non-functional.

This criterion FAILS because the underlying computation is not implemented -- the hardcoded `0` is a placeholder, not a correct computation result.
