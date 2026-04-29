# Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

**Criterion:** `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

**Verdict:** PASS

## Reasoning

### Service Layer Changes

In `modules/fundamental/src/purl/service/mod.rs`, the diff shows:

1. The `JoinType::LeftJoin` on `purl::Relation::PurlQualifier` has been removed. The query no longer joins the qualifier table, so qualifier data is not fetched.

2. The mapping logic now calls `p.without_qualifiers()` to strip qualifiers from each PURL before serialization:
   ```rust
   .map(|p| {
       let simplified = p.without_qualifiers();
       PurlSummary {
           purl: simplified.to_string(),
       }
   })
   ```

This ensures the returned PURLs contain only the type, namespace, name, and version components -- no qualifier parameters.

### Endpoint Layer Changes

In `modules/fundamental/src/purl/endpoints/recommend.rs`, the `use sea_orm::JoinType;` import was removed (no longer needed since the join was removed from the service layer). The return type remains `Json<PaginatedResults<PurlSummary>>`, preserving the response shape.

### Test Verification

The `test_recommend_purls_basic` test in `tests/api/purl_recommend.rs` seeds PURLs with qualifiers (`?repository_url=...&type=jar`) but asserts that the response contains only the versioned form:
```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This directly validates that the endpoint returns versioned PURLs without qualifiers.

### Conclusion

The service layer strips qualifiers via `without_qualifiers()`, the qualifier join is removed from the query, and the test confirms the response contains versioned PURLs without qualifier parameters. This criterion is satisfied.
