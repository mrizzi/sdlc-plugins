# File 3: Test Verification (Out-of-Scope File -- Requires User Approval)

## Action: WOULD CREATE or MODIFY (pending user approval per Step 9 scope containment)

## Purpose

The task's **Test Requirements** specify three tests:
1. Test that the migration runs successfully against a test database
2. Test that the rollback (down) re-adds the column
3. Verify that existing advisory queries still work after the column is dropped

However, no test file is listed in **Files to Modify** or **Files to Create**. Per Step 9's scope containment rules, any file outside those lists is out-of-scope and requires explicit user approval before proceeding.

## Proposed Location

Based on the repository structure, migration tests could be added to:
- `tests/api/advisory.rs` -- if migration tests are co-located with advisory endpoint tests
- A new `tests/migration/` directory -- if the project separates migration tests
- Within `migration/src/m0002_drop_advisory_status/mod.rs` as inline `#[cfg(test)]` tests

The most likely location following project conventions would be inline `#[cfg(test)]` tests within the migration module itself, or in the existing `tests/api/advisory.rs` file.

## Proposed Test Content

```rust
/// Verifies that the m0002 migration successfully drops the status column.
#[tokio::test]
async fn test_migration_drop_status_column() {
    // Given a database with the advisory table containing a status column
    let db = setup_test_database().await;
    
    // When the migration is applied
    let result = Migration.up(&SchemaManager::new(&db)).await;
    
    // Then the migration should succeed
    assert!(result.is_ok());
    // And the status column should no longer exist on the advisory table
    // (verify by attempting to query the column and expecting an error)
}

/// Verifies that the m0002 rollback re-adds the status column as a nullable string.
#[tokio::test]
async fn test_migration_rollback_readds_status_column() {
    // Given a database where the status column has been dropped
    let db = setup_test_database().await;
    Migration.up(&SchemaManager::new(&db)).await.unwrap();
    
    // When the rollback is applied
    let result = Migration.down(&SchemaManager::new(&db)).await;
    
    // Then the rollback should succeed
    assert!(result.is_ok());
    // And the status column should be re-added as a nullable string
}

/// Verifies that existing advisory queries function correctly after the status column is dropped.
#[tokio::test]
async fn test_advisory_queries_work_after_migration() {
    // Given a database with the migration applied
    let db = setup_test_database().await;
    Migration.up(&SchemaManager::new(&db)).await.unwrap();
    
    // When querying advisories using the standard service methods
    let advisories = AdvisoryService::list(&db, Default::default()).await;
    
    // Then the queries should succeed without errors
    assert!(advisories.is_ok());
}
```

## Conventions Applied

- **Doc comments:** Every test function has a `///` doc comment explaining what it verifies
- **Given-When-Then:** Non-trivial tests use section comments for structure
- **Assertion style:** Uses `assert!` and `assert_eq!` consistent with the project's testing patterns
- **Async tests:** Uses `#[tokio::test]` for async database operations
- **Test naming:** Follows `test_<subject>_<scenario>` pattern

## Note

The exact test implementation depends on the project's test infrastructure (database setup, fixtures, etc.), which would be discovered during Step 4's code inspection. The above is a representative structure following the discovered conventions.
