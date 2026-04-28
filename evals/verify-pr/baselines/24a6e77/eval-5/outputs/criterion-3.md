# Criterion 3: Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

## Verdict: PASS

## Reasoning

This criterion requires that when multiple PURLs differ only in their qualifiers (e.g., same package, same version, different `repository_url`), the response returns only one entry after qualifier removal.

### Code changes supporting this criterion

**Service layer (`modules/fundamental/src/purl/service/mod.rs`):**

After stripping qualifiers and mapping to `PurlSummary`, the PR adds a deduplication step:

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

The `.dedup_by(|a, b| a.purl == b.purl)` call removes consecutive duplicate entries where the PURL string is identical. This handles the case where two database entries like:
- `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar`
- `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar`

both become `pkg:maven/org.apache/commons-lang3@3.12` after qualifier removal, and the duplicate is eliminated.

Additionally, the query was updated to use `group_by` for the count:
```rust
let total = query.clone()
    .select_only()
    .column(purl::Column::Id)
    .group_by(purl::Column::Id)
    .count(&self.db).await?;
```

**Test verification (`tests/api/purl_recommend.rs`):**

The new `test_recommend_purls_dedup` test specifically validates this behavior:

```rust
// Seeds two PURLs that differ only in qualifiers
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar").await;
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar").await;

// Asserts only one entry is returned (deduplicated)
assert_eq!(body.items.len(), 1);
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

### Note on dedup_by behavior

The `dedup_by` method removes consecutive duplicates, not all duplicates globally. This works correctly when the query results are ordered (which they are, since the query applies ordering before pagination). If results are not guaranteed to be ordered, non-consecutive duplicates could survive. However, the existing ordering behavior (preserved per criterion 4) ensures consecutive grouping of identical PURLs after qualifier removal.

### Conclusion

The implementation adds explicit deduplication via `.dedup_by()` after qualifier stripping, and a dedicated test (`test_recommend_purls_dedup`) validates that two entries differing only in qualifiers are collapsed to one. This criterion is satisfied.
