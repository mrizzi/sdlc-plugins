# Criterion 2: Response PURLs do not contain `?` query parameters

## Criterion Text
Response PURLs do not contain `?` query parameters (no qualifiers present).

## Evidence from PR Diff

### Service layer (`modules/fundamental/src/purl/service/mod.rs`)
The `without_qualifiers()` method is called on each PURL before it is serialized to a string. This method strips all qualifier key-value pairs, which in PURL syntax appear after the `?` character. Since `without_qualifiers()` removes all qualifiers, the resulting string will never contain a `?` separator.

### Test evidence (`tests/api/purl_recommend.rs`)
The `test_recommend_purls_basic` test includes explicit `contains('?')` assertions:
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```
These assertions directly verify that no `?` character appears in any response PURL.

### Additional test evidence (`tests/api/purl_simplify.rs`)
Multiple tests in the new file also assert the absence of `?`:
- `test_simplified_purl_no_version`: `assert!(!body.items[0].purl.contains('?'));`
- `test_simplified_purl_mixed_types`: `assert!(!body.items[0].purl.contains("vcs_url"));`
- `test_simplified_purl_ordering_preserved`: `assert!(!body.items[0].purl.contains('?'));` and `assert!(!body.items[1].purl.contains('?'));`

## Verdict: PASS

The `without_qualifiers()` transformation guarantees no `?` appears in output PURLs, and the test suite explicitly asserts the absence of `?` characters and qualifier-specific keys across multiple test cases.
