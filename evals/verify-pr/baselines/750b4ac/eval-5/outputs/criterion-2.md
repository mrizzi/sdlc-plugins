# Criterion 2: Response PURLs do not contain `?` query parameters

## Criterion Text

Response PURLs do not contain `?` query parameters (no qualifiers present).

## Verdict: PASS

## Reasoning

The `without_qualifiers()` method, applied in the service layer's `.map()` closure, strips all qualifier parameters from the PURL string representation. Since qualifiers in PURL syntax follow the `?` character (e.g., `?repository_url=...&type=jar`), removing qualifiers eliminates the `?` and everything after it from the serialized PURL.

The PR adds explicit assertions in the test suite that verify this property:

In `test_recommend_purls_basic`:
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

In `test_simplified_purl_no_version`:
```rust
assert!(!body.items[0].purl.contains('?'));
```

In `test_simplified_purl_mixed_types`:
```rust
assert!(!body.items[0].purl.contains("vcs_url"));
```

In `test_simplified_purl_ordering_preserved`:
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

The code change that removes the qualifier join from the query (`JoinType::LeftJoin, purl::Relation::PurlQualifier.def()` is removed) and the application of `without_qualifiers()` on each result item together ensure that no qualifier data flows into the response PURLs.

This criterion is satisfied by the code changes.
