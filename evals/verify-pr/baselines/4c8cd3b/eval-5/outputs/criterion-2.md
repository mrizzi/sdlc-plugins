# Criterion 2: Response PURLs do not contain `?` query parameters

## Criterion Text
Response PURLs do not contain `?` query parameters (no qualifiers present)

## Verdict: PASS

## Analysis

### Code Implementation

The `without_qualifiers()` method is called on each PURL in the service layer before serialization:
```rust
let simplified = p.without_qualifiers();
PurlSummary {
    purl: simplified.to_string(),
}
```

According to the task's Implementation Notes, the `PackageUrl` builder in `common/src/purl.rs` supports constructing PURLs with or without qualifiers, and `without_qualifiers()` is the designated method for stripping them. Since qualifiers in PURL format are represented as query parameters after the `?` character, calling `without_qualifiers()` ensures no `?` appears in the serialized PURL string.

### Test Verification

The PR adds explicit assertions in the updated `test_recommend_purls_basic` test that verify the absence of the `?` character:
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

These assertions directly test the criterion requirement. If any qualifier leaked through, the `?` character would be present and the assertion would fail.

Additionally, in the new `tests/api/purl_simplify.rs` file:
- `test_simplified_purl_no_version` asserts `!body.items[0].purl.contains('?')`
- `test_simplified_purl_mixed_types` asserts `!body.items[0].purl.contains("vcs_url")` (checking specific qualifier absence)
- `test_simplified_purl_ordering_preserved` asserts `!body.items[0].purl.contains('?')` and `!body.items[1].purl.contains('?')`

The combined coverage across multiple test scenarios (basic, mixed types, ordering) provides strong evidence that `?` query parameters are consistently absent from response PURLs.
