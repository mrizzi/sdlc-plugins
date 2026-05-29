# Criterion 3: Duplicate entries are deduplicated after qualifier removal

## Criterion Text
Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response.

## Verdict: PASS

## Reasoning

The PR adds deduplication logic in `modules/fundamental/src/purl/service/mod.rs`. After stripping qualifiers and collecting items, the code applies `dedup_by`:

```rust
.dedup_by(|a, b| a.purl == b.purl)
.collect();
```

This ensures that PURLs which were previously distinct due to different qualifiers (e.g., same package version but different `repository_url` values) are collapsed into a single entry when the qualifiers are removed and the base PURLs match.

The behavior is explicitly tested by `test_recommend_purls_dedup` in `tests/api/purl_recommend.rs`:

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

This test seeds two PURLs that differ only in qualifiers, calls the recommend endpoint, and asserts that only one entry is returned -- confirming deduplication works as expected.

This criterion is satisfied.
