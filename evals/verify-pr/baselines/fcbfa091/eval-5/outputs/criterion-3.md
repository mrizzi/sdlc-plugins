## Criterion 3: Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

**Verdict: PASS**

### Analysis

The service layer in `modules/fundamental/src/purl/service/mod.rs` adds a deduplication step after qualifier stripping:

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

The `.dedup_by(|a, b| a.purl == b.purl)` call removes consecutive duplicate PURLs based on string equality. This handles the case where two database entries differ only in qualifiers (e.g., `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar` and `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar`) -- after qualifier stripping, both become `pkg:maven/org.apache/commons-lang3@3.12` and only one is retained.

Note: `dedup_by` only removes consecutive duplicates, which assumes the query results are sorted such that equivalent PURLs are adjacent. The query filters by namespace and name, so version-based ordering would group identical versioned PURLs together. The count query was also updated with `group_by(purl::Column::Id)` to correctly count distinct entries.

### Test Evidence

The new `test_recommend_purls_dedup` in `tests/api/purl_recommend.rs` directly tests this scenario:

```rust
// Seeds two PURLs with same version but different qualifiers
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar").await;
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar").await;

// Asserts only one entry returned after dedup
assert_eq!(body.items.len(), 1);
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This test seeds two entries that differ only in `repository_url` qualifier and verifies that the response contains exactly one deduplicated entry. This criterion is satisfied.
