# Criterion 3: Deduplication of entries previously distinct due to qualifiers

## Criterion Text
Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response.

## Evidence from PR Diff

### Service layer (`modules/fundamental/src/purl/service/mod.rs`)
After mapping PURLs through `without_qualifiers()`, a deduplication step was added:
```rust
.dedup_by(|a, b| a.purl == b.purl)
```
This removes consecutive duplicate entries that have the same PURL string after qualifier stripping. The `dedup_by` operates on consecutive elements, which is valid here because the database query returns results in a consistent order -- entries for the same package/version will be adjacent.

### Test evidence (`tests/api/purl_recommend.rs`)
The new `test_recommend_purls_dedup` function validates deduplication directly:
```rust
// Given PURLs with different qualifiers for the same package version
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar").await;
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar").await;

// Then only one entry is returned (deduplicated after qualifier removal)
assert_eq!(body.items.len(), 1);
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

Two PURLs that differ only in their `repository_url` qualifier are seeded. After qualifier removal, both become `pkg:maven/org.apache/commons-lang3@3.12`, and the `dedup_by` step collapses them into a single entry.

## Verdict: PASS

The `dedup_by` call in the service layer removes consecutive duplicates by PURL string comparison after qualifier stripping. The test confirms that two entries previously distinct only by qualifiers collapse into one.
