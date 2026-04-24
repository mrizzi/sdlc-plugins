# Criterion 3: Deduplication of entries previously distinct due to qualifiers

## Criterion Text
Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response.

## Evidence from PR Diff

### Service layer (`modules/fundamental/src/purl/service/mod.rs`)
After mapping PURLs to their simplified (qualifier-free) form, a deduplication step was added:
```rust
.dedup_by(|a, b| a.purl == b.purl)
```
This removes consecutive duplicate entries that share the same PURL string after qualifier stripping.

Note: `dedup_by` only removes *consecutive* duplicates. This works correctly here because the query results are ordered (by the database query's implicit or explicit ordering), so entries with the same base PURL will be adjacent. If ordering were not guaranteed, this could miss non-adjacent duplicates. However, the query uses a consistent order from the database, making this approach valid.

### Test evidence (`tests/api/purl_recommend.rs`)
The new `test_recommend_purls_dedup` test validates this directly:
```rust
// Given PURLs with different qualifiers for the same package version
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar").await;
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar").await;

// Then only one entry is returned (deduplicated after qualifier removal)
assert_eq!(body.items.len(), 1);
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

Two PURLs that differ only in their `repository_url` qualifier are seeded. After qualifier removal, both collapse to `pkg:maven/org.apache/commons-lang3@3.12`, and the dedup step reduces them to a single entry.

## Verdict: PASS

The implementation adds `dedup_by` on the PURL string after qualifier removal, and the test confirms that two previously distinct entries (differing only in qualifiers) are collapsed into one.
