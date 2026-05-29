# Criterion 2: Response PURLs do not contain `?` query parameters (no qualifiers present)

## Verdict: PASS

## Analysis

The PR implements qualifier removal in `modules/fundamental/src/purl/service/mod.rs` by calling `p.without_qualifiers()` before serialization. This strips all query parameters from the PURL string representation.

Two independent verification points in the test code confirm this:

1. In `test_recommend_purls_basic` (modified in `tests/api/purl_recommend.rs`):
   - `assert!(!body.items[0].purl.contains('?'));` -- explicitly checks no `?` in first item
   - `assert!(!body.items[1].purl.contains('?'));` -- explicitly checks no `?` in second item

2. In `test_recommend_purls_dedup` (new in `tests/api/purl_recommend.rs`):
   - `assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");` -- asserts against a string with no `?`

3. In `test_simplified_purl_no_version` (new in `tests/api/purl_simplify.rs`):
   - `assert!(!body.items[0].purl.contains('?'));`

4. In `test_simplified_purl_mixed_types` (new in `tests/api/purl_simplify.rs`):
   - `assert!(!body.items[0].purl.contains("vcs_url"));` -- checks qualifier keys are absent

5. In `test_simplified_purl_ordering_preserved` (new in `tests/api/purl_simplify.rs`):
   - `assert!(!body.items[0].purl.contains('?'));`
   - `assert!(!body.items[1].purl.contains('?'));`

The service layer code change ensures that `without_qualifiers()` is called on every PURL before it is serialized into the `PurlSummary`. This systematically prevents any `?` query parameters from appearing in the response.
