# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Analysis

The acceptance criterion requires that `vulnerability_count` reflects unique advisory counts, de-duplicated across multiple SBOMs. The task's Implementation Notes specify using a correlated subquery with `COUNT(DISTINCT a.id)` to compute the count.

### Evidence from PR Diff

In `modules/fundamental/src/package/service/mod.rs`, the vulnerability count is hardcoded to 0:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

The `// TODO: implement subquery` comment explicitly acknowledges that the subquery has NOT been implemented. There is no database query that joins through `sbom_package`, `sbom_advisory`, and `advisory` tables. The `COUNT(DISTINCT a.id)` logic specified in the Implementation Notes is entirely absent.

### Test Evidence

The test `test_vulnerability_count_deduplicates_across_sboms` in `tests/api/package_vuln_count.rs` seeds a package with 2 shared advisories across 3 SBOMs and asserts:

```rust
assert_eq!(pkg.vulnerability_count, 2);
```

This test would FAIL with the current implementation since all packages return `vulnerability_count: 0`.

Similarly, `test_package_with_vulnerabilities_has_count` seeds 3 advisories and expects:

```rust
assert_eq!(pkg.vulnerability_count, 3);
```

This would also FAIL.

### Conclusion

This criterion is NOT satisfied. The core feature -- computing the actual vulnerability count via a database subquery -- is not implemented. The field exists but always returns 0 regardless of the actual number of advisories. This is a significant functional gap that makes the feature non-functional for its stated purpose.
