# Criterion 2: Response PURLs do not contain `?` query parameters (no qualifiers present)

## Verdict: PASS

## Reasoning

The `without_qualifiers()` call in the service layer strips all qualifier parameters from PURLs before they are serialized into the response. Since qualifiers are appended to PURLs after a `?` character (e.g., `?repository_url=...&type=jar`), removing qualifiers removes the `?` and everything following it.

Multiple tests in the PR explicitly verify this property with negative assertions:

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

These assertions confirm that no response PURL contains the `?` character, which is the delimiter that introduces qualifier parameters in the PURL specification. The coverage spans multiple PURL ecosystems (Maven, npm, PyPI) and edge cases (no version, mixed types, multiple versions).
