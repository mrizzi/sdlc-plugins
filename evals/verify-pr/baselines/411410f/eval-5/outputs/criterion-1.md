# Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

## Criterion
`GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers.

## Verdict: PASS

## Reasoning

The PR makes two key changes that satisfy this criterion:

1. **Service layer (`modules/fundamental/src/purl/service/mod.rs`)**: The PURL serialization logic now calls `p.without_qualifiers()` before converting to string. The original code used `p.to_string()` which included qualifiers; the new code uses `simplified.to_string()` where `simplified = p.without_qualifiers()`. This strips all qualifier parameters (e.g., `repository_url`, `type`) from the PURL, producing versioned PURLs like `pkg:maven/org.apache/commons-lang3@3.12` instead of `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar`.

2. **Endpoint layer (`modules/fundamental/src/purl/endpoints/recommend.rs`)**: The qualifier join (`JoinType::LeftJoin` on `purl::Relation::PurlQualifier`) has been removed from the query, and the `sea_orm::JoinType` import was removed. This means the database query no longer fetches qualifier data, which is consistent with not including qualifiers in the response.

3. **Test evidence**: The updated `test_recommend_purls_basic` test now asserts:
   - `body.items[0].purl == "pkg:maven/org.apache/commons-lang3@3.12"` (versioned, no qualifiers)
   - `!body.items[0].purl.contains('?')` (confirms no query parameters)
   - `!body.items[1].purl.contains('?')` (confirms for all items)

The combination of the service-layer `without_qualifiers()` call, the removal of the qualifier join, and the updated test assertions demonstrates that the endpoint now returns versioned PURLs without qualifiers.
