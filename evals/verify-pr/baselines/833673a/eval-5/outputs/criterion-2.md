# Criterion 2: Response PURLs do not contain `?` query parameters (no qualifiers present)

## Verdict: PASS

## Reasoning

The `without_qualifiers()` method strips all qualifier parameters from the PURL before serialization. Since qualifiers are appended after a `?` character in the PURL specification, removing qualifiers means the resulting PURL string will not contain a `?` character.

Multiple tests explicitly verify this negative condition:

In `tests/api/purl_recommend.rs`:
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

In `tests/api/purl_simplify.rs`:
```rust
// test_simplified_purl_no_version
assert!(!body.items[0].purl.contains('?'));

// test_simplified_purl_mixed_types
assert!(!body.items[0].purl.contains("vcs_url"));

// test_simplified_purl_ordering_preserved
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

The test data seeds PURLs that originally contained qualifiers (e.g., `?repository_url=https://repo1.maven.org&type=jar`) and then verifies the response does not contain these qualifier strings.

## Evidence

- `tests/api/purl_recommend.rs`: negative `contains('?')` assertions in `test_recommend_purls_basic`
- `tests/api/purl_simplify.rs`: negative `contains('?')` assertions in three tests
- `modules/fundamental/src/purl/service/mod.rs`: `p.without_qualifiers()` applied to all results before serialization
