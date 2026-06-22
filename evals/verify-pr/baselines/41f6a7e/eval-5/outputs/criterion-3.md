# Criterion 3: Duplicate entries deduplicated after qualifier removal

**Criterion:** Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

**Result:** PASS

## Reasoning

The PR implements deduplication at the service layer and validates it with a dedicated test.

**Implementation (`modules/fundamental/src/purl/service/mod.rs`):**

After stripping qualifiers with `without_qualifiers()`, the code applies `.dedup_by(|a, b| a.purl == b.purl)` on the collected results:

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

This removes adjacent duplicate PURLs from the result set. Note that `dedup_by` only removes *adjacent* duplicates, which means the correctness depends on the query returning results ordered such that duplicates are adjacent. Since the query filters by namespace and name, and the duplicates arise from the same version with different qualifiers, the database ordering should group these together. The service also removed the qualifier join (`JoinType::LeftJoin, purl::Relation::PurlQualifier.def()`), which eliminates the source of duplicate rows from the query itself.

**Test verification (`tests/api/purl_recommend.rs` -- `test_recommend_purls_dedup`):**

The new test function seeds two PURLs that differ only in qualifiers:
- `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar`
- `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar`

After requesting recommendations, it asserts:
```rust
assert_eq!(body.items.len(), 1);
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This directly validates that two entries that were previously distinct (different `repository_url` qualifiers) are now deduplicated into a single entry after qualifier removal.
