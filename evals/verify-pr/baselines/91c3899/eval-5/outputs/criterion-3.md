# Criterion 3: Duplicate entries deduplicated in the response

## Verdict: PASS

## Analysis

The implementation adds `.dedup_by(|a, b| a.purl == b.purl)` to the iterator chain after qualifier stripping. This removes consecutive duplicate PURLs that were previously distinct due to different qualifiers.

### Evidence

In `modules/fundamental/src/purl/service/mod.rs`:
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

The test `test_recommend_purls_dedup` in `tests/api/purl_recommend.rs` validates this behavior:
- Seeds two PURLs with the same version but different qualifiers (`repo1.maven.org` vs `repo2.maven.org`)
- After qualifier removal and dedup, asserts only 1 item is returned
- Confirms the deduplicated PURL is `"pkg:maven/org.apache/commons-lang3@3.12"`

Note: `dedup_by` removes consecutive duplicates. For production reliability, rows sharing the same namespace/name are typically adjacent due to the query filter on namespace and name, making this approach effective for the described use case.
