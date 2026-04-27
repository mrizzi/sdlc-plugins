# Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

## Criterion Text
`GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

## Verdict: PASS

## Reasoning

The PR implements qualifier removal at the service layer in `modules/fundamental/src/purl/service/mod.rs`. The key change is in the `recommend` method where results are mapped through a new transformation:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

Previously, the code used `p.to_string()` directly, which included qualifiers. Now it calls `p.without_qualifiers()` before serialization, producing versioned PURLs like `pkg:maven/org.apache/commons-lang3@3.12` instead of `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar`.

Additionally, the qualifier join has been removed from the query:
- Removed: `.join(JoinType::LeftJoin, purl::Relation::PurlQualifier.def())`
- Removed: `use sea_orm::JoinType;` import

The endpoint handler in `modules/fundamental/src/purl/endpoints/recommend.rs` continues to serve the same route `GET /api/v2/purl/recommend` with the same `RecommendParams` query extraction, so the API path is unchanged.

The test `test_recommend_purls_basic` confirms the expected behavior by asserting:
```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This verifies that the endpoint returns versioned PURLs without qualifiers.
