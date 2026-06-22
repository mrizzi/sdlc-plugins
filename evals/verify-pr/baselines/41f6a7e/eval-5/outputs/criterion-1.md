# Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

**Criterion:** `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

**Result:** PASS

## Reasoning

The PR implements this criterion through two coordinated changes:

1. **Service layer (`modules/fundamental/src/purl/service/mod.rs`):** The recommendation query results are mapped through `p.without_qualifiers()` before constructing the `PurlSummary`. This strips all qualifier parameters from the PURL before serialization:

   ```rust
   .map(|p| {
       let simplified = p.without_qualifiers();
       PurlSummary {
           purl: simplified.to_string(),
       }
   })
   ```

2. **Endpoint layer (`modules/fundamental/src/purl/endpoints/recommend.rs`):** The unused `sea_orm::JoinType` import was removed since the qualifier join is no longer performed. The endpoint return type remains `Result<Json<PaginatedResults<PurlSummary>>, AppError>`, confirming the response shape is preserved.

3. **Test verification (`tests/api/purl_recommend.rs`):** The `test_recommend_purls_basic` test seeds fully-qualified PURLs (with `repository_url` and `type` qualifiers) and asserts that the response contains only the versioned form:

   ```rust
   assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
   ```

   This directly validates that the endpoint returns versioned PURLs without qualifiers for the exact query parameter specified in the criterion.

The implementation correctly uses the existing `without_qualifiers()` method on the `PackageUrl` builder (referenced in the task's Implementation Notes) to strip qualifiers at the service layer, ensuring all downstream consumers receive simplified PURLs.
