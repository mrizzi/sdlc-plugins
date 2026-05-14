# Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

## Criterion Text
`GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

## Verdict: PASS

## Analysis

The PR modifies the PURL recommendation endpoint in two layers to achieve this:

### Service Layer Change (`modules/fundamental/src/purl/service/mod.rs`)

The service layer now strips qualifiers from PURLs before returning them. The diff shows:

1. The `JoinType::LeftJoin` on `purl::Relation::PurlQualifier` has been removed from the query, meaning qualifier data is no longer fetched from the database.
2. The mapping function has been changed from:
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
   This explicitly calls `without_qualifiers()` on each PURL before converting to string, ensuring qualifiers are stripped from the response.

### Endpoint Layer Change (`modules/fundamental/src/purl/endpoints/recommend.rs`)

The `use sea_orm::JoinType;` import was removed since the join is no longer needed. The endpoint handler itself continues to call `PurlService::recommend()` and return the results unchanged, confirming the response flows through the simplified service.

### Test Verification

The updated `test_recommend_purls_basic` test seeds PURLs with qualifiers (`?repository_url=...&type=jar`) but asserts that the response contains only the versioned PURL without qualifiers:
```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This directly confirms the criterion is met. The endpoint returns versioned PURLs (with `@3.12` version) but without qualifier query parameters.
