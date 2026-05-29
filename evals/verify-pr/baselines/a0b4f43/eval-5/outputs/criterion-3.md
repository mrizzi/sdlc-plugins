# Criterion 3: Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

## Verdict: PASS

## Reasoning

The PR implements deduplication at the service layer in `modules/fundamental/src/purl/service/mod.rs`:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
.dedup_by(|a, b| a.purl == b.purl)
.collect();
```

After stripping qualifiers with `without_qualifiers()`, the code applies `.dedup_by(|a, b| a.purl == b.purl)` to remove consecutive duplicate PURL strings. This handles the case where two database rows that were previously distinct (e.g., same package version but different `repository_url` qualifiers) now produce identical PURL strings after qualifier removal.

Test evidence in `tests/api/purl_recommend.rs` -- `test_recommend_purls_dedup`:

```rust
// Given PURLs with different qualifiers for the same package version
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar").await;
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar").await;

// Then only one entry is returned (deduplicated after qualifier removal)
assert_eq!(body.items.len(), 1);
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This test seeds two PURLs that differ only in their `repository_url` qualifier, then asserts that only one entry is returned after deduplication. This directly validates the criterion.

**Note:** The `dedup_by` method only removes consecutive duplicates. This works correctly here because the query results are ordered by the database, so identical PURLs (after qualifier removal) from the same namespace/name group will be adjacent. However, if future sorting changes cause non-adjacent duplicates, this could be a latent issue. The current test passes, confirming the behavior works with the current query ordering.
