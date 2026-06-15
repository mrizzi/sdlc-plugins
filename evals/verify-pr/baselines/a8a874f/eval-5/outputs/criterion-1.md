# Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

## Verdict: PASS

## Reasoning

The PR modifies `modules/fundamental/src/purl/service/mod.rs` to strip qualifiers from the PURL response. Specifically, the service layer now calls `p.without_qualifiers()` before serializing the PURL to string:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

The endpoint handler in `modules/fundamental/src/purl/endpoints/recommend.rs` continues to use the same `PurlService::recommend()` method, so the `GET /api/v2/purl/recommend` endpoint now returns versioned PURLs without qualifiers.

The test `test_recommend_purls_basic` in `tests/api/purl_recommend.rs` confirms this by asserting:
```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This is a versioned PURL (has `@3.12`) without qualifiers (no `?` query parameters).

The new test file `tests/api/purl_simplify.rs` further validates this behavior across multiple PURL types (Maven, npm, pypi) with the `test_simplified_purl_mixed_types` test.

All CI checks pass, confirming these tests execute successfully.
