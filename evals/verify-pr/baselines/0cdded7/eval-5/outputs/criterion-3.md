# Criterion 3: Duplicate entries are deduplicated after qualifier removal

## Criterion Text
Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

## Verdict: PASS

## Reasoning

### Implementation

In `modules/fundamental/src/purl/service/mod.rs`, after stripping qualifiers with `without_qualifiers()`, a deduplication step is applied:

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

The `.dedup_by(|a, b| a.purl == b.purl)` call removes consecutive duplicate entries where the PURL string is identical. This addresses the case where two database entries that differed only by qualifiers (e.g., `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar` vs `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar`) would produce the same simplified PURL (`pkg:maven/org.apache/commons-lang3@3.12`).

**Note on dedup_by behavior**: The `dedup_by` method only removes *consecutive* duplicates. This is correct for this use case because the query orders results by the same PURL fields (namespace, name, version), so entries that will become identical after qualifier removal will be adjacent in the result set. However, if the ordering did not guarantee adjacency of duplicates, a `HashSet`-based deduplication would be more robust. Given that the query filters by namespace and name and the remaining ordering is by version, consecutive duplicates are expected to be adjacent.

### Test Evidence

The `test_recommend_purls_dedup` test in `tests/api/purl_recommend.rs` directly validates this behavior:

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

This test seeds two PURLs that differ only in qualifiers, requests recommendations, and asserts that only one entry is returned with the simplified PURL. This directly validates the deduplication behavior.

The criterion is satisfied.
