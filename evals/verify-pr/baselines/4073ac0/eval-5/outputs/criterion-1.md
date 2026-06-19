# Criterion 1: `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

## Verdict: PASS

## Reasoning

The PR modifies the PURL recommendation pipeline in `modules/fundamental/src/purl/service/mod.rs` to call `p.without_qualifiers()` on each PURL model before constructing the `PurlSummary` response object. This explicitly strips qualifier parameters from the output PURL string.

### Code evidence

In the service layer (`modules/fundamental/src/purl/service/mod.rs`), the `.map()` closure was changed from:
```rust
.map(|p| PurlSummary {
    purl: p.to_string(),
})
```
to:
```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

This ensures that every PURL returned by the recommendation endpoint is serialized without qualifiers.

### Test evidence

The `test_recommend_purls_basic` test in `tests/api/purl_recommend.rs` was updated to assert the new behavior:
```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This asserts a versioned PURL without any qualifier suffix (no `?repository_url=...&type=...`).

Additionally, the endpoint handler in `modules/fundamental/src/purl/endpoints/recommend.rs` removed the `use sea_orm::JoinType;` import and the qualifier join was removed from the service query, confirming the qualifier data path is fully severed.

### Conclusion

The code changes ensure that the recommend endpoint returns versioned PURLs without qualifiers. The criterion is satisfied.
