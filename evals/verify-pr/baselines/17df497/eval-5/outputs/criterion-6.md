# Criterion 6 (Test Requirement): Update `test_recommend_purls_basic` to assert versioned PURL without qualifiers

## Criterion Text
Update `test_recommend_purls_basic` to assert versioned PURL without qualifiers.

## Evidence from PR Diff

### Base-branch version
In the base branch, `test_recommend_purls_basic` asserted a fully qualified PURL with qualifiers:
```rust
assert_eq!(
    body.items[0].purl,
    "pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar"
);
```

### PR version (`tests/api/purl_recommend.rs`)
The assertion was changed to check for a versioned PURL without qualifiers:
```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

The doc comment was also updated:
- Base: `/// Verifies that basic PURL recommendations return fully qualified PURLs.`
- PR: `/// Verifies that basic PURL recommendations return versioned PURLs without qualifiers.`

The assertion comment was updated similarly:
- Base: `// Then recommendations are returned with fully qualified PURLs`
- PR: `// Then recommendations are returned with versioned PURLs without qualifiers`

## Verdict: PASS

The test was updated to assert the new simplified format (versioned PURL without qualifiers), including explicit `!contains('?')` checks and updated documentation comments.
