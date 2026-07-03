# Criterion 2: Response PURLs do not contain `?` query parameters (no qualifiers present)

## Verdict: PASS

## Reasoning

This criterion is a specific constraint on the response format: no PURL in the response should contain the `?` character that introduces query parameters (qualifiers).

### Implementation Evidence

The `without_qualifiers()` method called in `modules/fundamental/src/purl/service/mod.rs` strips all qualifier key-value pairs from the PURL. Since qualifiers in the PURL spec are separated from the version by a `?` character (e.g., `pkg:maven/org.apache/commons-lang3@3.12?repository_url=...&type=jar`), removing qualifiers eliminates the `?` and everything after it.

The transformation chain is:
1. Database returns full PURL entity (with qualifiers)
2. `p.without_qualifiers()` creates a new PURL without qualifier parameters
3. `simplified.to_string()` serializes the qualifier-free PURL

### Test Validation

The PR adds explicit negative assertions for the `?` character in multiple test functions:

**In `tests/api/purl_recommend.rs` (`test_recommend_purls_basic`):**
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

These assertions directly verify that no `?` character appears in the response PURLs, even though the seeded database entries contain qualifiers.

**In `tests/api/purl_simplify.rs` (`test_simplified_purl_no_version`):**
```rust
assert!(!body.items[0].purl.contains('?'));
```

**In `tests/api/purl_simplify.rs` (`test_simplified_purl_mixed_types`):**
```rust
assert!(!body.items[0].purl.contains("vcs_url"));
```

This asserts that even qualifier-specific substrings are absent from the response.

**In `tests/api/purl_simplify.rs` (`test_simplified_purl_ordering_preserved`):**
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

### Conclusion

The criterion is fully satisfied. The `without_qualifiers()` method ensures no qualifiers are serialized, and multiple tests explicitly assert the absence of `?` in response PURLs across various scenarios (basic, no-version, mixed types, ordering).
