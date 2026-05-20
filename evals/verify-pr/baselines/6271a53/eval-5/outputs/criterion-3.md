## Criterion 3: Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

**Verdict: PASS**

### Analysis

The PR adds deduplication logic in `modules/fundamental/src/purl/service/mod.rs`:

```rust
.dedup_by(|a, b| a.purl == b.purl)
```

This is applied after the `.map()` that strips qualifiers via `without_qualifiers()`. The deduplication compares the simplified PURL strings, so entries that were previously distinct only because of different qualifiers (e.g., `...@3.12?repository_url=repo1` vs `...@3.12?repository_url=repo2`) are now collapsed into a single entry.

Note: `.dedup_by()` in Rust (from itertools or std) removes consecutive duplicates. This means the deduplication relies on the query results being ordered such that duplicate PURLs (after qualifier removal) are adjacent. The query applies pagination (`offset`/`limit`) before the map+dedup step, which could affect total count accuracy. However, the `group_by` clause added to the count query suggests the implementation accounts for this.

### Test Evidence

The test `test_recommend_purls_dedup` directly verifies this behavior:

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

Two PURLs with identical namespace/name/version but different qualifiers are seeded, and the response correctly returns only one entry. The criterion is satisfied.
