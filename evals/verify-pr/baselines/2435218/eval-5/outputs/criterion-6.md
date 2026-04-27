# Criterion 6: Update `test_recommend_purls_basic` to assert versioned PURL without qualifiers

## Criterion Text
Update `test_recommend_purls_basic` to assert versioned PURL without qualifiers.

## Evidence from PR Diff

### Base-branch version (`tests/api/purl_recommend.rs`)
The original test asserted the fully qualified PURL including qualifiers:
```rust
/// Verifies that basic PURL recommendations return fully qualified PURLs.
// ...
assert_eq!(
    body.items[0].purl,
    "pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar"
);
```

### PR-branch version (`tests/api/purl_recommend.rs`)
The test was updated with a new doc comment and revised assertions:
```rust
/// Verifies that basic PURL recommendations return versioned PURLs without qualifiers.
// ...
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

### Changes made
1. Doc comment updated from "fully qualified PURLs" to "versioned PURLs without qualifiers"
2. The expected PURL value changed from the full string with `?repository_url=...&type=jar` to the version-only string `@3.12`
3. Two new `assert!(!contains('?'))` assertions were added to verify both items lack qualifiers

## Verdict: PASS

The `test_recommend_purls_basic` function was updated to assert the simplified versioned PURL format without qualifiers. The doc comment, expected value, and additional negative assertions all reflect the new behavior.
