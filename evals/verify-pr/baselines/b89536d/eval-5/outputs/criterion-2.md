# Criterion 2: Response PURLs do not contain `?` query parameters (no qualifiers present)

## Verdict: PASS

## Reasoning

The PR ensures that response PURLs never contain qualifier parameters by:

1. **Service layer change**: In `modules/fundamental/src/purl/service/mod.rs`, every PURL is passed through `p.without_qualifiers()` before being serialized to string. This method (referenced in the task's Implementation Notes as part of the `PackageUrl` builder in `common/src/purl.rs`) strips all qualifier key-value pairs from the PURL.

2. **Test assertions explicitly verify this**: The modified `test_recommend_purls_basic` includes explicit negative assertions:
   ```rust
   assert!(!body.items[0].purl.contains('?'));
   assert!(!body.items[1].purl.contains('?'));
   ```
   These assertions directly verify that no `?` character (which would introduce qualifier parameters) appears in any returned PURL.

3. **New test file also verifies**: In `tests/api/purl_simplify.rs`, the `test_simplified_purl_no_version` and `test_simplified_purl_ordering_preserved` tests both include `assert!(!body.items[N].purl.contains('?'))` assertions, and `test_simplified_purl_mixed_types` asserts `assert!(!body.items[0].purl.contains("vcs_url"))`.

The combination of the `without_qualifiers()` call in the service layer and the explicit `contains('?')` assertions in tests confirms this criterion is satisfied.
