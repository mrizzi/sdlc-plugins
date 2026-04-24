# Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

## Criterion
`GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers.

## Result: PASS

## Detailed Reasoning

The PR implements qualifier removal in the service layer at `modules/fundamental/src/purl/service/mod.rs`. The diff shows that the mapping step now calls `p.without_qualifiers()` on each PURL before serializing:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

This replaces the previous implementation that directly serialized the full PURL including qualifiers:

```rust
.map(|p| PurlSummary {
    purl: p.to_string(),
})
```

Additionally, the qualifier join has been removed from the query. The old code included:
```rust
.join(JoinType::LeftJoin, purl::Relation::PurlQualifier.def());
```
This join is no longer present in the PR version, confirming that qualifier data is no longer fetched from the database.

The endpoint handler in `recommend.rs` still calls `PurlService::new(&db).recommend(...)`, so the endpoint path and behavior are preserved -- only the response content changes.

The test `test_recommend_purls_basic` now asserts:
```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This confirms the response contains versioned PURLs (`@3.12`) without qualifiers (no `?` or query parameters).

The criterion is satisfied by both the implementation change (using `without_qualifiers()`) and the test assertions confirming the expected format.
