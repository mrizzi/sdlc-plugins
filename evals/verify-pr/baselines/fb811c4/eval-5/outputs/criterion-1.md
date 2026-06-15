# Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

## Verdict: PASS

## Analysis

The service layer in `modules/fundamental/src/purl/service/mod.rs` maps each query result through `p.without_qualifiers()` before constructing the `PurlSummary` response object. The qualifier JOIN (`JoinType::LeftJoin, purl::Relation::PurlQualifier.def()`) has been removed from the query entirely, and the `use sea_orm::JoinType` import was removed from the endpoint file.

## Evidence

In `modules/fundamental/src/purl/service/mod.rs`:
```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

The test `test_recommend_purls_basic` confirms:
```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This returns a versioned PURL without qualifiers, satisfying the criterion.
