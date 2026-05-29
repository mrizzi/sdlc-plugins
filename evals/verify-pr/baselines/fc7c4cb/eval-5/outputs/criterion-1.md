## Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

**Verdict: PASS**

### Evidence from the diff

The diff introduces two changes that together ensure the endpoint returns versioned PURLs stripped of qualifiers:

1. **Service layer** (`modules/fundamental/src/purl/service/mod.rs`): The qualifier join is removed entirely. Previously, the query included `.join(JoinType::LeftJoin, purl::Relation::PurlQualifier.def())` to load qualifier data. This join is deleted. Additionally, the mapping step now calls `p.without_qualifiers()` to strip qualifiers before serializing the PURL to a string:

   ```rust
   .map(|p| {
       let simplified = p.without_qualifiers();
       PurlSummary {
           purl: simplified.to_string(),
       }
   })
   ```

2. **Endpoint layer** (`modules/fundamental/src/purl/endpoints/recommend.rs`): The `use sea_orm::JoinType;` import is removed since the join is no longer used in the service layer. The endpoint handler itself is unchanged, correctly delegating to `PurlService::recommend`.

3. **Test evidence** (`tests/api/purl_recommend.rs`): The updated `test_recommend_purls_basic` test seeds fully qualified PURLs with qualifiers but asserts the response contains versioned PURLs without qualifiers:

   ```rust
   assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
   ```

   This directly confirms the endpoint returns `pkg:maven/org.apache/commons-lang3@3.12` (versioned, no qualifiers) instead of the previous fully qualified form with `?repository_url=...&type=jar`.

The implementation correctly uses the existing `without_qualifiers()` method on the `PackageUrl` builder, as recommended in the task's implementation notes.
