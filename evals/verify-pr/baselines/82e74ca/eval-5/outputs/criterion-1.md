# Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

## Criterion
`GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers.

## Verification

### Endpoint code changes (recommend.rs)
The endpoint handler in `modules/fundamental/src/purl/endpoints/recommend.rs` was modified to remove the `use sea_orm::JoinType` import. The handler still calls `PurlService::new(&db).recommend(...)`, returning `Json<PaginatedResults<PurlSummary>>`. The qualifier join is no longer imported because it is no longer needed.

### Service layer changes (service/mod.rs)
The service layer in `modules/fundamental/src/purl/service/mod.rs` contains the core logic change:

1. The query no longer joins with `purl::Relation::PurlQualifier` (the `.join(JoinType::LeftJoin, purl::Relation::PurlQualifier.def())` line was removed).
2. The mapping logic was changed from:
   ```rust
   .map(|p| PurlSummary { purl: p.to_string() })
   ```
   to:
   ```rust
   .map(|p| {
       let simplified = p.without_qualifiers();
       PurlSummary { purl: simplified.to_string() }
   })
   ```

This calls `without_qualifiers()` on each PURL before serializing it, which strips qualifier parameters. The task's Implementation Notes confirm that `PackageUrl` builder in `common/src/purl.rs` supports the `without_qualifiers()` method.

### Test evidence
The `test_recommend_purls_basic` test now asserts:
```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```
This confirms the response contains versioned PURLs (with `@3.12`) but without qualifiers (no `?repository_url=...`).

## Result: PASS

The code changes in the service layer explicitly call `without_qualifiers()` before converting to string, and the tests assert on versioned PURLs without qualifier strings. The endpoint correctly returns versioned PURLs without qualifiers.
