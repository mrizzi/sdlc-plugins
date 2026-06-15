# Criterion 3: Duplicate entries that were previously distinct due to different qualifiers are deduplicated

## Verdict: PASS

## Reasoning

The PR adds deduplication logic in `modules/fundamental/src/purl/service/mod.rs`:
```rust
.dedup_by(|a, b| a.purl == b.purl)
```

This is applied after qualifier stripping (`.map(|p| { let simplified = p.without_qualifiers(); ... })`), so PURLs that were previously distinct only because of different qualifiers (e.g., `?repository_url=https://repo1.maven.org` vs `?repository_url=https://repo2.maven.org`) are now deduplicated.

The new test `test_recommend_purls_dedup` in `tests/api/purl_recommend.rs` explicitly validates this:
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

This test seeds two PURLs identical except for qualifiers and asserts only one result is returned after deduplication. All CI checks pass.
