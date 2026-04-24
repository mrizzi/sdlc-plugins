# Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

## Acceptance Criterion
`GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers.

## Verdict: PASS

## Reasoning

The PR diff demonstrates this criterion is satisfied through both production code and test changes:

### Production Code Changes

1. **`modules/fundamental/src/purl/service/mod.rs`**: The recommendation query no longer joins `PurlQualifier`. The `JoinType::LeftJoin` on `purl::Relation::PurlQualifier` is removed. Instead, the service maps results through `p.without_qualifiers()` before serializing:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

This ensures every PURL in the response is a versioned PURL without qualifiers.

2. **`modules/fundamental/src/purl/endpoints/recommend.rs`**: The `sea_orm::JoinType` import is removed, consistent with the qualifier join being eliminated from the service layer.

### Test Evidence

In `tests/api/purl_recommend.rs`, the `test_recommend_purls_basic` function is updated to assert the response contains versioned PURLs without qualifiers:

```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

Previously this assertion checked for the fully qualified PURL including `?repository_url=...&type=jar`.

Additionally, the new file `tests/api/purl_simplify.rs` includes `test_simplified_purl_no_version` and `test_simplified_purl_mixed_types` which further verify that qualifiers are stripped across different PURL types.
