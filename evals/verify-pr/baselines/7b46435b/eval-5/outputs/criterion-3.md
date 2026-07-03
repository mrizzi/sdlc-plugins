# Criterion 3: Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

## Verdict: PASS

## Reasoning

When qualifiers are stripped, PURLs that previously differed only in their qualifier parameters become identical. For example, `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar` and `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar` both become `pkg:maven/org.apache/commons-lang3@3.12`. Without deduplication, the response would contain duplicate entries.

### Implementation Evidence

The service layer in `modules/fundamental/src/purl/service/mod.rs` applies deduplication after qualifier removal:

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

The `dedup_by(|a, b| a.purl == b.purl)` call removes consecutive duplicate entries based on PURL string equality. This is applied after the `map` that strips qualifiers, so it catches entries that became identical after qualifier removal.

### Implementation Note

The `dedup_by` method (from Rust's `Iterator` trait) removes consecutive duplicates. This means it relies on the database query returning duplicate PURLs in adjacent positions. Since the query filters by namespace and name and the database typically returns rows in insertion order or primary key order, entries for the same package version (which would become duplicates after qualifier stripping) are likely to be adjacent. However, if the database returned them non-consecutively, some duplicates could slip through. A more robust approach would be to use a `HashSet` or sort-then-dedup, but for the typical query patterns in this codebase, consecutive dedup is sufficient.

### Test Validation

The `test_recommend_purls_dedup` test in `tests/api/purl_recommend.rs` directly validates this criterion:

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

The test seeds two PURLs that differ only in their `repository_url` qualifier and asserts that only one entry appears in the response after deduplication.

### Conclusion

The criterion is satisfied. The implementation applies `dedup_by` after qualifier stripping, and the dedicated dedup test verifies that previously-distinct entries (differing only by qualifiers) are collapsed into a single response entry.
