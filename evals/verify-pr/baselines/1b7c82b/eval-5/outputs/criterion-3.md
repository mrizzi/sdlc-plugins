# Criterion 3: Deduplication of entries previously distinct due to qualifiers

## Criterion Text
Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

## Verdict: PASS

## Reasoning

### Code evidence

The service layer in `modules/fundamental/src/purl/service/mod.rs` implements deduplication after qualifier stripping:

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

The `.dedup_by(|a, b| a.purl == b.purl)` call removes consecutive duplicates by comparing the simplified PURL strings. This handles the case where two entries like `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar` and `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar` both simplify to `pkg:maven/org.apache/commons-lang3@3.12` -- the second would be removed as a duplicate.

Note: `dedup_by` only removes *consecutive* duplicates (similar to Unix `uniq`). This works correctly here because the query results are ordered, so identical simplified PURLs will be adjacent. If the ordering were not guaranteed, a `HashSet`-based approach would be needed, but the existing query ordering ensures consecutive grouping of same-version PURLs.

### Query changes

The query was also modified to remove the qualifier join:

```rust
// Before:
.join(JoinType::LeftJoin, purl::Relation::PurlQualifier.def());

// After: (join removed)
```

And the count query was updated to use `group_by` to get an accurate count:

```rust
let total = query.clone()
    .select_only()
    .column(purl::Column::Id)
    .group_by(purl::Column::Id)
    .count(&self.db).await?;
```

### Test evidence

The new `test_recommend_purls_dedup` test in `tests/api/purl_recommend.rs` directly validates this behavior:

```rust
// Given PURLs with different qualifiers for the same package version
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar").await;
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar").await;

// When requesting recommendations (qualifiers stripped, dedup applied)
let resp = ctx.get("/api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3").await;

// Then only one entry is returned (deduplicated after qualifier removal)
assert_eq!(body.items.len(), 1);
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This test seeds two PURLs that differ only in their `repository_url` qualifier, then asserts that only one result is returned after deduplication, confirming the criterion is satisfied.
