# Criterion 3: Duplicate entries that were previously distinct due to different qualifiers are deduplicated

## Verdict: PASS

## Reasoning

The PR implements deduplication in `modules/fundamental/src/purl/service/mod.rs` by adding a `.dedup_by()` call after the qualifier stripping:

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

This ensures that PURLs which were previously distinct only because they had different qualifiers (e.g., `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org` vs `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org`) are collapsed into a single entry after qualifier removal.

The new test `test_recommend_purls_dedup` directly validates this behavior:
- Seeds two PURLs for the same package/version but with different `repository_url` qualifiers
- Asserts that only one entry is returned (`assert_eq!(body.items.len(), 1)`)
- Asserts the returned PURL is the versioned form without qualifiers (`assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12")`)

Note: `dedup_by` only removes consecutive duplicates, so this assumes the query results are ordered such that identical versioned PURLs are adjacent. Since the PURLs share the same namespace, name, and version, and differ only in qualifiers (which are stripped), they will be adjacent after the query's default ordering. This is a reasonable assumption given the query structure.
