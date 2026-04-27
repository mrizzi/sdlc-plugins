# Criterion 3: Deduplication of entries previously distinct due to qualifiers

## Criterion Text
Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response.

## Evidence from PR Diff

### Service layer (`modules/fundamental/src/purl/service/mod.rs`)
After mapping PURLs through `without_qualifiers()`, a deduplication step was added to the iterator pipeline:
```rust
.dedup_by(|a, b| a.purl == b.purl)
```
This removes consecutive duplicate entries that share the same PURL string after qualifier stripping. The `dedup_by` method operates on consecutive elements, which is valid here because the query results are ordered by the database, so PURLs with the same namespace/name/version will be adjacent in the result set.

### Query change
The qualifier join (`JoinType::LeftJoin, purl::Relation::PurlQualifier.def()`) was removed from the query. Previously, the left join on qualifiers could produce multiple rows for the same base PURL (one per qualifier combination). With the join removed and `dedup_by` added, entries that were previously distinct solely due to different qualifier values are now collapsed.

### Test evidence (`tests/api/purl_recommend.rs`)
The new `test_recommend_purls_dedup` test directly validates this behavior:
```rust
// Given PURLs with different qualifiers for the same package version
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar").await;
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar").await;

// Then only one entry is returned (deduplicated after qualifier removal)
assert_eq!(body.items.len(), 1);
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```
Two PURLs identical except for `repository_url` qualifier are seeded. After qualifier removal, both resolve to the same PURL string, and `dedup_by` collapses them to a single entry. The test asserts exactly 1 item is returned.

## Verdict: PASS

The implementation adds `dedup_by` on the PURL string after qualifier removal, and the dedicated deduplication test confirms that two previously distinct entries (differing only in qualifiers) are collapsed into one.
