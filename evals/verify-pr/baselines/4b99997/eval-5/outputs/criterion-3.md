# Criterion 3: Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

## Analysis

The PR adds a deduplication step in `modules/fundamental/src/purl/service/mod.rs`:

```rust
.dedup_by(|a, b| a.purl == b.purl)
```

This is chained after the `.map()` that strips qualifiers, so PURLs that were previously distinct (e.g., same version but different `repository_url` qualifiers) are now deduplicated based on their simplified PURL string.

The service also modifies the count query to use `group_by` to handle the adjusted counting:

```rust
let total = query.clone()
    .select_only()
    .column(purl::Column::Id)
    .group_by(purl::Column::Id)
    .count(&self.db).await?;
```

The new test `test_recommend_purls_dedup` in `tests/api/purl_recommend.rs` directly validates this:

```rust
// Seeds two PURLs with same version but different repository_url qualifiers
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar").await;
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar").await;

// Asserts only one entry is returned (deduplicated)
assert_eq!(body.items.len(), 1);
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

## Result: PASS

The `.dedup_by()` call ensures duplicates created by qualifier stripping are removed, and the `test_recommend_purls_dedup` test directly validates this behavior.
