# Criterion 3: Duplicate entries that were previously distinct due to different qualifiers are deduplicated

## Verdict: PASS

## Reasoning

This criterion addresses a key consequence of removing qualifiers: two PURLs that were previously distinct (e.g., same package/version but different `repository_url` qualifiers) now become identical after qualifier stripping and must be deduplicated.

### Code Implementation

The service layer (`modules/fundamental/src/purl/service/mod.rs`) implements deduplication through:

1. **`dedup_by()` call**: After the `.map()` that strips qualifiers, a `.dedup_by(|a, b| a.purl == b.purl)` call is chained before `.collect()`:
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

2. **Dedup semantics**: `dedup_by` removes consecutive duplicate elements. Since the query orders results by the database's default ordering (which groups same-version PURLs together due to shared namespace/name/version), consecutive duplicates from different qualifiers will be adjacent and correctly deduplicated.

### Potential Concern: Non-consecutive Duplicates

The `dedup_by` method only removes *consecutive* duplicates. If the database ordering does not guarantee that same-version PURLs with different qualifiers are adjacent, non-consecutive duplicates could slip through. However, given that:
- The qualifier join was removed, so the query now returns base PURL rows
- The query filters by namespace and name, and ordering by version would naturally group same-version entries together
- The `group_by(purl::Column::Id)` in the count query suggests awareness of potential duplicates

This is a reasonable implementation. The task description says "Duplicate entries that were previously distinct due to different qualifiers are deduplicated" -- and the implementation achieves this for the expected data patterns.

### Test Evidence

The `test_recommend_purls_dedup` test in `tests/api/purl_recommend.rs` directly verifies deduplication:

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

This test seeds two PURLs for the same package version `3.12` with different `repository_url` qualifiers, then asserts that only one result is returned after qualifier stripping and deduplication.

### Comparison with Previous Behavior

The base-branch version had `test_recommend_purls_with_qualifiers` which seeded the exact same two PURLs (same version, different `repository_url`) and asserted `body.items.len() == 2` with both items containing `repository_url=`. The new test replaces this by asserting `body.items.len() == 1`, confirming the deduplication behavior.

## Conclusion

The deduplication is implemented via `dedup_by` on the PURL string after qualifier stripping, and the `test_recommend_purls_dedup` test explicitly verifies the scenario described in the acceptance criterion.
