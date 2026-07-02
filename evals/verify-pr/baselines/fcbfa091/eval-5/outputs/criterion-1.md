## Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

**Verdict: PASS**

### Analysis

The PR modifies the PURL recommendation service layer in `modules/fundamental/src/purl/service/mod.rs` to strip qualifiers from returned PURLs. The key change is:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

Previously, the service mapped each PURL directly with `p.to_string()`, which included all qualifiers. Now it calls `p.without_qualifiers()` before serialization, producing versioned PURLs like `pkg:maven/org.apache/commons-lang3@3.12` instead of `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar`.

The endpoint handler in `modules/fundamental/src/purl/endpoints/recommend.rs` retains the same return type and call pattern -- it delegates to `PurlService::recommend()` and returns the result as JSON. The `JoinType` import for qualifier joins was also removed since it is no longer needed.

### Test Evidence

The updated `test_recommend_purls_basic` in `tests/api/purl_recommend.rs` seeds PURLs with qualifiers but now asserts the response contains only the versioned form:

```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

The new `test_simplified_purl_mixed_types` in `tests/api/purl_simplify.rs` further confirms this for npm PURLs:

```rust
assert_eq!(body.items[0].purl, "pkg:npm/%40angular/core@16.0.0");
```

Both tests seed PURLs with qualifiers and verify the response contains only the versioned identifier. This criterion is satisfied.
