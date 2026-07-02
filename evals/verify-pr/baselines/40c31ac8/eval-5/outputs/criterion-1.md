## Criterion 1: `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

### Verdict: PASS

### Reasoning

The diff modifies the service layer in `modules/fundamental/src/purl/service/mod.rs` to strip qualifiers from PURLs before returning them. Specifically:

1. The qualifier join is removed: the line `.join(JoinType::LeftJoin, purl::Relation::PurlQualifier.def())` is deleted from the query.
2. The mapping step now calls `p.without_qualifiers()` on each PURL entity before converting to string:
   ```rust
   .map(|p| {
       let simplified = p.without_qualifiers();
       PurlSummary {
           purl: simplified.to_string(),
       }
   })
   ```

The `without_qualifiers()` method is documented in the task as being available on the `PackageUrl` builder in `common/src/purl.rs`.

The test `test_recommend_purls_basic` in `tests/api/purl_recommend.rs` is updated to verify this behavior:
- Seeds PURLs with qualifiers (`?repository_url=...&type=jar`)
- Asserts the returned PURL is `"pkg:maven/org.apache/commons-lang3@3.12"` (versioned, no qualifiers)
- Asserts `!body.items[0].purl.contains('?')` and `!body.items[1].purl.contains('?')`

Additionally, the new file `tests/api/purl_simplify.rs` contains `test_simplified_purl_no_version` and `test_simplified_purl_mixed_types` which both verify that PURLs are returned without qualifiers across different scenarios.

The implementation correctly strips qualifiers at the service layer, and multiple tests confirm the behavior. This criterion is satisfied.
