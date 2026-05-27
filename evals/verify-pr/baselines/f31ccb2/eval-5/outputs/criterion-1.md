## Criterion 1: `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

### Assessment: PASS

**Evidence from the diff:**

The production code in `modules/fundamental/src/purl/service/mod.rs` now calls `p.without_qualifiers()` before serializing the PURL in the response, and the qualifier join has been removed from the query.

The test `test_recommend_purls_basic` in `tests/api/purl_recommend.rs` directly validates this behavior:
- Seeds PURLs with qualifiers (`?repository_url=...&type=jar`)
- Calls `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3`
- Asserts `body.items[0].purl` equals `"pkg:maven/org.apache/commons-lang3@3.12"` (no qualifiers)

The new test file `tests/api/purl_simplify.rs` further validates this for additional PURL types (npm, pypi, versionless maven).

**Conclusion:** The implementation and tests confirm versioned PURLs are returned without qualifiers.
