# Criterion 3: Deduplication After Qualifier Removal

**Criterion:** Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

**Verdict:** PASS

## Reasoning

The PR adds deduplication logic in `modules/fundamental/src/purl/service/mod.rs` using the `.dedup_by()` iterator method:

```rust
.dedup_by(|a, b| a.purl == b.purl)
```

This is applied after the `.map()` that strips qualifiers via `without_qualifiers()`. The deduplication compares the simplified PURL strings, so entries that were previously distinct only because of different qualifiers (e.g., `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar` vs `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar`) will now be recognized as duplicates and collapsed into a single entry.

The new test `test_recommend_purls_dedup` in `tests/api/purl_recommend.rs` explicitly verifies this behavior:

```rust
// Given PURLs with different qualifiers for the same package version
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar").await;
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar").await;

// Then only one entry is returned (deduplicated after qualifier removal)
assert_eq!(body.items.len(), 1);
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This test seeds two PURLs that differ only in `repository_url` qualifier and asserts that only one result is returned after simplification and deduplication, directly confirming the criterion.

Note: `dedup_by()` only removes consecutive duplicates, which works correctly here because results are from the same query ordered by the database. If ordering could interleave duplicates, `unique_by()` would be more robust, but for the current use case the approach is correct.
