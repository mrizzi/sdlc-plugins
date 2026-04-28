# Criterion 5: Response serialization includes the new field in JSON output

## Criterion Text
Response serialization includes the new field in JSON output

## Verdict: PASS

## Reasoning

The `vulnerability_count` field is added as a public field to the `PackageSummary` struct in `modules/fundamental/src/package/model/summary.rs`:

```rust
+    pub vulnerability_count: i64,
```

In the Rust/Axum/SeaORM ecosystem used by this repository, structs returned via `Json<PaginatedResults<PackageSummary>>` are serialized using `serde`. Adding a public field to the struct automatically includes it in the JSON output, provided the struct derives `Serialize` (which is the standard pattern for response types in this codebase).

The endpoint in `modules/fundamental/src/package/endpoints/list.rs` already returns `Json<PaginatedResults<PackageSummary>>`, and the service layer in `modules/fundamental/src/package/service/mod.rs` constructs `PackageSummary` instances that include the new field:

```rust
+            PackageSummary {
+                id: p.id,
+                name: p.name,
+                version: p.version,
+                license: p.license,
+                vulnerability_count: 0, // TODO: implement subquery
+            }
```

The field will appear in the JSON response. While the value is hardcoded to 0 (which is a separate issue covered by Criterion 3), the serialization itself is correct -- the field will be present in the JSON output.

## Evidence

- File: `modules/fundamental/src/package/model/summary.rs` -- field added to struct
- File: `modules/fundamental/src/package/service/mod.rs` -- field populated in service layer
- File: `modules/fundamental/src/package/endpoints/list.rs` -- endpoint returns `Json<PaginatedResults<PackageSummary>>` (unchanged, automatically picks up new field)
- The test file confirms the field is expected in deserialized response: `pkg.vulnerability_count`
