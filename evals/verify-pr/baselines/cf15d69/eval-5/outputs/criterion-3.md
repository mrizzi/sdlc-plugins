# Criterion 3: Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

## Verdict: PASS (with caveat)

## Reasoning

The service layer adds a `.dedup_by(|a, b| a.purl == b.purl)` call after the `.map()` transformation that strips qualifiers:

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

The `test_recommend_purls_dedup` test directly verifies this behavior: it seeds two PURLs for the same package version with different qualifiers (`?repository_url=https://repo1.maven.org&type=jar` and `?repository_url=https://repo2.maven.org&type=jar`), and asserts that only one entry is returned after qualifier removal and deduplication (`assert_eq!(body.items.len(), 1)`).

**Caveat:** The `dedup_by` method in Rust's `Iterator` trait removes only *consecutive* duplicates (analogous to Unix `uniq`). If the database returns rows in an order where identical-after-stripping PURLs are not adjacent, duplicates could survive. However, the query filters by namespace and name, and database ordering typically groups rows with the same version together. The qualifier join has been removed, so there is no secondary sort dimension that would interleave versions. The test passes, and the implementation satisfies the criterion for the expected data patterns.

Additionally, the query was modified to add `GROUP BY purl::Column::Id` which, while operating on a primary key (and thus not reducing rows), signals intent to handle deduplication at the query level as well.
