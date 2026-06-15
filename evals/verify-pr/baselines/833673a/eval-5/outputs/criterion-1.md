# Criterion 1: `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

## Verdict: PASS

## Reasoning

The PR modifies the service layer in `modules/fundamental/src/purl/service/mod.rs` to call `p.without_qualifiers()` on each PURL result before constructing the `PurlSummary`. The qualifier join (`JoinType::LeftJoin` on `purl::Relation::PurlQualifier.def()`) is removed from the query entirely, and the import of `sea_orm::JoinType` is removed from the endpoint handler in `recommend.rs`.

The transformation pipeline is now:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

This ensures all returned PURLs are versioned (if the original had a version) but without qualifier parameters.

The test `test_recommend_purls_basic` confirms this behavior by asserting:
```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This is a versioned PURL (`@3.12` version present) without any qualifiers (no `?` suffix).

## Evidence

- `modules/fundamental/src/purl/service/mod.rs`: `let simplified = p.without_qualifiers();` followed by `purl: simplified.to_string()`
- `modules/fundamental/src/purl/endpoints/recommend.rs`: removed `use sea_orm::JoinType;`
- `tests/api/purl_recommend.rs`: `assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");`
