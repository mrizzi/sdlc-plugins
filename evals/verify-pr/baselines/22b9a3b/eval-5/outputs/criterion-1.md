# Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

**Criterion:** `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

**Verdict: PASS**

## Reasoning

### Service Layer Changes

The PR modifies `modules/fundamental/src/purl/service/mod.rs` to strip qualifiers from the PURL before serialization:

1. The `JoinType::LeftJoin` on `purl::Relation::PurlQualifier` is removed, so qualifier data is no longer fetched from the database.
2. The mapping pipeline now calls `p.without_qualifiers()` to produce a simplified PURL, then calls `.to_string()` on the result. This ensures the serialized PURL contains only the scheme, type, namespace, name, and version -- no qualifiers.

Before (base branch):
```rust
.map(|p| PurlSummary {
    purl: p.to_string(),
})
```

After (PR branch):
```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

### Test Verification

The updated `test_recommend_purls_basic` in `tests/api/purl_recommend.rs` confirms this behavior:

- Seeds PURLs with qualifiers (`?repository_url=https://repo1.maven.org&type=jar`)
- Asserts the response contains `"pkg:maven/org.apache/commons-lang3@3.12"` (versioned, no qualifiers)
- Explicitly asserts `!body.items[0].purl.contains('?')` and `!body.items[1].purl.contains('?')`

The endpoint signature in `recommend.rs` is unchanged -- it still accepts `purl` as a query parameter and the base PURL triggers the recommendation lookup. The simplification happens entirely in the service layer's response mapping.

### Endpoint Layer

The endpoint in `modules/fundamental/src/purl/endpoints/recommend.rs` removes the unused `use sea_orm::JoinType;` import since the qualifier join is no longer needed. The function signature and return type remain identical, confirming the endpoint path and parameters are unchanged.

All evidence confirms versioned PURLs without qualifiers are returned.
