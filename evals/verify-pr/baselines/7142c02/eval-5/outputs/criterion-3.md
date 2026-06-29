# Criterion 3: Deduplication of entries after qualifier removal

**Acceptance Criterion:** Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

**Verdict: PASS**

## Evidence

### Production code changes

In `modules/fundamental/src/purl/service/mod.rs`, after the qualifier stripping via `.map()`, a deduplication step is applied:

```rust
.dedup_by(|a, b| a.purl == b.purl)
```

This removes consecutive duplicate entries based on the `purl` string equality. Since qualifiers have been stripped, PURLs that were previously distinct only due to different qualifiers (e.g., different `repository_url` values) now have identical `purl` strings and are collapsed into a single entry.

Note: `dedup_by` only removes **consecutive** duplicates. This works correctly here because the query returns PURLs grouped by namespace, name, and version (the remaining distinguishing fields after qualifier removal), so duplicates from different qualifiers on the same version will be adjacent in the result set.

### Test coverage

The new `test_recommend_purls_dedup` function in `tests/api/purl_recommend.rs` directly tests this behavior:

```rust
// Given PURLs with different qualifiers for the same package version
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar").await;
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar").await;

// ...

// Then only one entry is returned (deduplicated after qualifier removal)
assert_eq!(body.items.len(), 1);
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This test seeds two PURLs that differ only in their `repository_url` qualifier and asserts that the response contains exactly one entry.

### Conclusion

The production code includes a `dedup_by` step, and a dedicated test validates that qualifier-only variants collapse into a single response entry. This criterion is satisfied.
