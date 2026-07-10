# Criterion 2: Response PURLs do not contain `?` query parameters (no qualifiers present)

## Verdict: PASS

## Analysis

### What the criterion requires

Every PURL string in the response must not contain the `?` character, which would indicate the presence of query-style qualifier parameters.

### Evidence from the PR diff

#### Service layer guarantee (`modules/fundamental/src/purl/service/mod.rs`)

The `without_qualifiers()` method is called on every PURL before serialization. By design, PURLs constructed without qualifiers do not contain `?` in their string representation, since qualifiers are the only component that introduces the `?` separator in the PURL specification.

#### Explicit test assertions (`tests/api/purl_recommend.rs`)

The modified `test_recommend_purls_basic` test includes explicit negative assertions:

```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

These assertions directly verify the criterion's requirement that no `?` character appears in the response PURLs.

#### Additional test coverage (`tests/api/purl_simplify.rs`)

Multiple tests in the new file assert the absence of `?`:

- `test_simplified_purl_no_version`: `assert!(!body.items[0].purl.contains('?'));`
- `test_simplified_purl_ordering_preserved`: `assert!(!body.items[0].purl.contains('?'));` and `assert!(!body.items[1].purl.contains('?'));`
- `test_simplified_purl_mixed_types`: `assert!(!body.items[0].purl.contains("vcs_url"));` (asserts specific qualifier key is absent)

### Conclusion

The service layer strips all qualifiers, and multiple test functions explicitly assert the absence of `?` in response PURLs across different scenarios (basic, dedup, ordering, mixed types). The criterion is satisfied.
