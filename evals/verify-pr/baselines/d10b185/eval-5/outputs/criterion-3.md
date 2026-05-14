# Criterion 3: Duplicate entries are deduplicated after qualifier removal

**Criterion:** Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

**Result:** PASS

## Evidence

### Implementation changes

In `modules/fundamental/src/purl/service/mod.rs`, a deduplication step was added after qualifier stripping:

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

The `.dedup_by(|a, b| a.purl == b.purl)` call removes consecutive duplicate entries based on the PURL string, which handles the case where two PURLs that were distinct only due to different qualifiers become identical after qualifier removal.

Additionally, the query was updated to include grouping for accurate total counts:

```rust
let total = query.clone()
    .select_only()
    .column(purl::Column::Id)
    .group_by(purl::Column::Id)
    .count(&self.db).await?;
```

### Test confirmation

The new `test_recommend_purls_dedup` in `tests/api/purl_recommend.rs` directly validates this behavior:

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

Two PURLs that differ only in `repository_url` qualifier result in a single response entry after qualifier removal and deduplication.

### Reasoning

The implementation adds `.dedup_by()` after the qualifier stripping step, and the test seeds two PURLs differing only in qualifiers, asserting that only one entry is returned. This criterion is satisfied.
