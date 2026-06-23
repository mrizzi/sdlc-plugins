# Criterion 2: Response PURLs do not contain `?` query parameters (no qualifiers present)

## Verdict: PASS

## Reasoning

This criterion is closely related to Criterion 1 but focuses specifically on the absence of the `?` character (which introduces query parameters/qualifiers in PURL format).

1. **Implementation:** The `without_qualifiers()` method is called on each PURL entity in the service layer (`modules/fundamental/src/purl/service/mod.rs`). This method removes all qualifier key-value pairs from the PURL, ensuring the serialized string contains no `?` character.

2. **Test assertions explicitly check for `?` absence:**
   - In `test_recommend_purls_basic`: `assert!(!body.items[0].purl.contains('?'))` and `assert!(!body.items[1].purl.contains('?'))`
   - In `test_simplified_purl_no_version`: `assert!(!body.items[0].purl.contains('?'))`
   - In `test_simplified_purl_mixed_types`: `assert!(!body.items[0].purl.contains("vcs_url"))` -- checks specific qualifier name
   - In `test_simplified_purl_ordering_preserved`: `assert!(!body.items[0].purl.contains('?'))` and `assert!(!body.items[1].purl.contains('?'))`

3. **The qualifier join is removed from the database query**, so qualifiers are not even fetched. Even if `without_qualifiers()` had a bug, the join removal means qualifier data would not be available to serialize.

The combination of the code change and comprehensive test assertions provides strong evidence that response PURLs will not contain `?` query parameters.
