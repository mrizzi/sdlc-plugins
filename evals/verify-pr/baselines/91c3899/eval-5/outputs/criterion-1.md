# Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

## Verdict: PASS

## Analysis

The implementation calls `p.without_qualifiers()` on each database row before constructing the `PurlSummary`, which strips qualifier parameters while preserving type, namespace, name, and version.

### Evidence

In `modules/fundamental/src/purl/service/mod.rs`, the map closure:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

This transforms fully qualified PURLs like `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar` into versioned PURLs without qualifiers like `pkg:maven/org.apache/commons-lang3@3.12`.

The test `test_recommend_purls_basic` in `tests/api/purl_recommend.rs` confirms this by asserting:
```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

The new test file `tests/api/purl_simplify.rs` further validates this across multiple PURL types (Maven, npm, PyPI).
