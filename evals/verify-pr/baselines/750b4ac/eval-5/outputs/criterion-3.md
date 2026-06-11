# Criterion 3: Deduplication of entries previously distinct due to qualifiers

## Criterion Text

Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response.

## Verdict: PASS

## Reasoning

The PR adds deduplication logic in `modules/fundamental/src/purl/service/mod.rs`. After stripping qualifiers with `without_qualifiers()`, the code applies `.dedup_by(|a, b| a.purl == b.purl)` to the iterator before collecting into the final result vector:

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

This ensures that entries which were previously distinct only because they had different qualifier strings (e.g., `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org` vs `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org`) are collapsed into a single entry after qualifier removal.

The new test `test_recommend_purls_dedup` explicitly validates this behavior:
- Seeds two PURLs with the same name/version but different `repository_url` qualifiers
- Asserts that only one entry is returned after deduplication
- Confirms the returned PURL matches the expected simplified form

Note: `dedup_by` removes consecutive duplicates, which is sufficient here because the query results are ordered by the database, so identical PURLs (after qualifier stripping) will be adjacent. The PR also adds `group_by(purl::Column::Id)` to the count query to ensure the total count reflects deduplicated results.

This criterion is satisfied by the code changes.
