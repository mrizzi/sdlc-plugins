# Criterion 2: Response PURLs do not contain `?` query parameters

## Criterion Text
Response PURLs do not contain `?` query parameters (no qualifiers present)

## Verdict: PASS

## Reasoning

The PR ensures qualifier-free PURLs through two mechanisms:

1. **Service layer transformation**: In `modules/fundamental/src/purl/service/mod.rs`, every PURL in the response is processed through `without_qualifiers()` before being serialized to a string. This method (documented in the task's Implementation Notes as being available on the `PackageUrl` builder in `common/src/purl.rs`) strips all qualifier key-value pairs from the PURL representation.

2. **Test assertions**: The updated `test_recommend_purls_basic` in `tests/api/purl_recommend.rs` includes explicit assertions that response PURLs do not contain the `?` character:
   ```rust
   assert!(!body.items[0].purl.contains('?'));
   assert!(!body.items[1].purl.contains('?'));
   ```

3. **New test file**: The `tests/api/purl_simplify.rs` file also validates qualifier absence across multiple scenarios:
   - `test_simplified_purl_no_version`: `assert!(!body.items[0].purl.contains('?'));`
   - `test_simplified_purl_mixed_types`: `assert!(!body.items[0].purl.contains("vcs_url"));`
   - `test_simplified_purl_ordering_preserved`: `assert!(!body.items[0].purl.contains('?'));` and `assert!(!body.items[1].purl.contains('?'));`

The combination of the `without_qualifiers()` call in the service layer and the multiple test assertions across different PURL types (Maven, npm, PyPI) provides strong evidence that response PURLs will not contain `?` query parameters.
