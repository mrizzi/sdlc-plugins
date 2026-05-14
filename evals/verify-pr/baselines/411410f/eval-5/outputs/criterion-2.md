# Criterion 2: Response PURLs do not contain `?` query parameters

## Criterion
Response PURLs do not contain `?` query parameters (no qualifiers present).

## Verdict: PASS

## Reasoning

This criterion is closely related to criterion 1 but focuses specifically on the absence of the `?` character that delimits qualifiers in PURL syntax.

1. **Code change**: In `modules/fundamental/src/purl/service/mod.rs`, the mapping function now calls `p.without_qualifiers()` before serializing the PURL to a string. The `without_qualifiers()` method on the `PackageUrl` builder (referenced in the task's Implementation Notes as existing in `common/src/purl.rs`) produces a PURL that contains only the type, namespace, name, and version components -- no qualifier section. Since the `?` character only appears in PURLs to introduce the qualifier section, removing qualifiers guarantees the absence of `?`.

2. **Test assertions**: Multiple test functions explicitly assert the absence of `?`:
   - `test_recommend_purls_basic`: `assert!(!body.items[0].purl.contains('?'))` and `assert!(!body.items[1].purl.contains('?'))`
   - `test_simplified_purl_no_version`: `assert!(!body.items[0].purl.contains('?'))`
   - `test_simplified_purl_mixed_types`: `assert!(!body.items[0].purl.contains("vcs_url"))` (checks for absence of specific qualifier content)
   - `test_simplified_purl_ordering_preserved`: `assert!(!body.items[0].purl.contains('?'))` and `assert!(!body.items[1].purl.contains('?'))`

3. **Qualifier join removal**: The removal of the `LeftJoin` on `PurlQualifier` in the service layer means qualifier data is never fetched from the database, providing a second layer of assurance that qualifiers cannot appear in the response.

The code changes eliminate qualifiers at both the query level (no join) and the serialization level (`without_qualifiers()`), and tests explicitly verify the absence of `?` characters. This criterion is satisfied.
