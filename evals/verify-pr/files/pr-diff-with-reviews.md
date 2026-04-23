<!-- SYNTHETIC TEST DATA — mock PR diff for eval testing; simulates `gh pr diff` output for a PR with review comments -->

```diff
diff --git a/entity/src/sbom.rs b/entity/src/sbom.rs
index 4e5f6a7..b8c9d0e 100644
--- a/entity/src/sbom.rs
+++ b/entity/src/sbom.rs
@@ -12,6 +12,7 @@ pub struct Model {
     pub name: String,
     pub sha256: String,
     pub published: DateTimeWithTimeZone,
+    pub deleted_at: Option<DateTimeWithTimeZone>,
 }

 #[derive(Copy, Clone, Debug, EnumIter, DeriveRelation)]
diff --git a/migration/src/m0042_sbom_soft_delete/mod.rs b/migration/src/m0042_sbom_soft_delete/mod.rs
new file mode 100644
index 0000000..1a2b3c4
--- /dev/null
+++ b/migration/src/m0042_sbom_soft_delete/mod.rs
@@ -0,0 +1,22 @@
+use sea_orm_migration::prelude::*;
+
+#[derive(DeriveMigrationName)]
+pub struct Migration;
+
+#[async_trait::async_trait]
+impl MigrationTrait for Migration {
+    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
+        manager
+            .alter_table(
+                Table::alter()
+                    .table(Sbom::Table)
+                    .add_column(ColumnDef::new(Sbom::DeletedAt).timestamp_with_time_zone().null())
+                    .to_owned(),
+            )
+            .await
+    }
+
+    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
+        manager
+            .alter_table(
+                Table::alter()
+                    .table(Sbom::Table)
+                    .drop_column(Sbom::DeletedAt)
+                    .to_owned(),
+            )
+            .await
+    }
+}
diff --git a/modules/fundamental/src/sbom/endpoints/mod.rs b/modules/fundamental/src/sbom/endpoints/mod.rs
index 5f6a7b8..c9d0e1f 100644
--- a/modules/fundamental/src/sbom/endpoints/mod.rs
+++ b/modules/fundamental/src/sbom/endpoints/mod.rs
@@ -8,6 +8,7 @@ pub fn router() -> Router {
     Router::new()
         .route("/api/v2/sbom", get(list::list_sboms))
         .route("/api/v2/sbom/:id", get(get::get_sbom))
+        .route("/api/v2/sbom/:id", delete(delete_sbom))
 }

+/// Handles DELETE /api/v2/sbom/{id} by setting deleted_at timestamp.
+pub async fn delete_sbom(
+    db: DatabaseConnection,
+    Path(sbom_id): Path<SbomId>,
+) -> Result<StatusCode, AppError> {
+    let sbom = SbomService::new(&db)
+        .fetch(sbom_id.id)
+        .await
+        .context("SBOM not found")?
+        .ok_or(AppError::NotFound("SBOM not found".into()))?;
+
+    if sbom.deleted_at.is_some() {
+        return Err(AppError::Conflict("SBOM is already deleted".into()));
+    }
+
+    SbomService::new(&db)
+        .soft_delete(sbom_id.id)
+        .await
+        .context("Failed to soft-delete SBOM")?;
+
+    Ok(StatusCode::NO_CONTENT)
+}
diff --git a/modules/fundamental/src/sbom/endpoints/list.rs b/modules/fundamental/src/sbom/endpoints/list.rs
index 6a7b8c9..d0e1f2a 100644
--- a/modules/fundamental/src/sbom/endpoints/list.rs
+++ b/modules/fundamental/src/sbom/endpoints/list.rs
@@ -6,14 +6,22 @@ use common::model::paginated::PaginatedResults;
 #[derive(Debug, Deserialize)]
 pub struct SbomListParams {
     pub offset: Option<i64>,
     pub limit: Option<i64>,
+    pub include_deleted: Option<bool>,
 }

 pub async fn list_sboms(
     db: DatabaseConnection,
     Query(params): Query<SbomListParams>,
 ) -> Result<Json<PaginatedResults<SbomSummary>>, AppError> {
+    let include_deleted = params.include_deleted.unwrap_or(false);
+
     let results = SbomService::new(&db)
-        .list(params.offset, params.limit)
+        .list(params.offset, params.limit, include_deleted)
         .await
         .context("Failed to list SBOMs")?;

diff --git a/modules/fundamental/src/sbom/service/sbom.rs b/modules/fundamental/src/sbom/service/sbom.rs
index 7b8c9d0..e1f2a3b 100644
--- a/modules/fundamental/src/sbom/service/sbom.rs
+++ b/modules/fundamental/src/sbom/service/sbom.rs
@@ -18,8 +18,12 @@ impl SbomService {
     }

-    pub async fn list(&self, offset: Option<i64>, limit: Option<i64>) -> Result<PaginatedResults<SbomSummary>> {
-        let query = Sbom::find();
+    pub async fn list(
+        &self,
+        offset: Option<i64>,
+        limit: Option<i64>,
+        include_deleted: bool,
+    ) -> Result<PaginatedResults<SbomSummary>> {
+        let mut query = Sbom::find();
+        if !include_deleted {
+            query = query.filter(sbom::Column::DeletedAt.is_null());
+        }

         let total = query.clone().count(&self.db).await?;
@@ -40,4 +44,22 @@ impl SbomService {
             items,
         })
     }
+
+    /// Soft-deletes an SBOM and its related join table entries.
+    pub async fn soft_delete(&self, id: i64) -> Result<()> {
+        let now = chrono::Utc::now();
+
+        sbom::Entity::update_many()
+            .filter(sbom::Column::Id.eq(id))
+            .col_expr(sbom::Column::DeletedAt, Expr::value(now))
+            .exec(&self.db)
+            .await?;
+
+        sbom_package::Entity::update_many()
+            .filter(sbom_package::Column::SbomId.eq(id))
+            .col_expr(sbom_package::Column::DeletedAt, Expr::value(now))
+            .exec(&self.db)
+            .await?;
+
+        sbom_advisory::Entity::update_many()
+            .filter(sbom_advisory::Column::SbomId.eq(id))
+            .col_expr(sbom_advisory::Column::DeletedAt, Expr::value(now))
+            .exec(&self.db)
+            .await?;
+
+        Ok(())
+    }
 }
diff --git a/tests/api/sbom_delete.rs b/tests/api/sbom_delete.rs
new file mode 100644
index 0000000..2b3c4d5
--- /dev/null
+++ b/tests/api/sbom_delete.rs
@@ -0,0 +1,62 @@
+use crate::common::TestContext;
+use axum::http::StatusCode;
+
+/// Verifies that deleting an SBOM returns 204 and excludes it from list results.
+#[test_context(TestContext)]
+#[tokio::test]
+async fn test_delete_sbom_returns_204(ctx: &TestContext) {
+    // Given an existing SBOM
+    let sbom_id = ctx.seed_sbom("test-sbom-1").await;
+
+    // When deleting the SBOM
+    let resp = ctx.delete(&format!("/api/v2/sbom/{}", sbom_id)).await;
+
+    // Then 204 No Content is returned
+    assert_eq!(resp.status(), StatusCode::NO_CONTENT);
+
+    // And the SBOM is excluded from default list
+    let list_resp = ctx.get("/api/v2/sbom").await;
+    let body: PaginatedResults<SbomSummary> = list_resp.json().await;
+    assert!(body.items.iter().all(|s| s.id != sbom_id));
+}
+
+/// Verifies that deleting a non-existent SBOM returns 404.
+#[test_context(TestContext)]
+#[tokio::test]
+async fn test_delete_nonexistent_sbom_returns_404(ctx: &TestContext) {
+    let resp = ctx.delete("/api/v2/sbom/999999").await;
+    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
+}
+
+/// Verifies that deleting an already-deleted SBOM returns 409 Conflict.
+#[test_context(TestContext)]
+#[tokio::test]
+async fn test_delete_already_deleted_sbom_returns_409(ctx: &TestContext) {
+    // Given a soft-deleted SBOM
+    let sbom_id = ctx.seed_sbom("test-sbom-2").await;
+    ctx.delete(&format!("/api/v2/sbom/{}", sbom_id)).await;
+
+    // When deleting again
+    let resp = ctx.delete(&format!("/api/v2/sbom/{}", sbom_id)).await;
+
+    // Then 409 Conflict is returned
+    assert_eq!(resp.status(), StatusCode::CONFLICT);
+}
+
+/// Verifies that include_deleted=true returns soft-deleted SBOMs in the list.
+#[test_context(TestContext)]
+#[tokio::test]
+async fn test_list_sboms_include_deleted(ctx: &TestContext) {
+    // Given a deleted SBOM
+    let sbom_id = ctx.seed_sbom("test-sbom-3").await;
+    ctx.delete(&format!("/api/v2/sbom/{}", sbom_id)).await;
+
+    // When listing with include_deleted=true
+    let resp = ctx.get("/api/v2/sbom?include_deleted=true").await;
+
+    // Then the deleted SBOM appears in results
+    let body: PaginatedResults<SbomSummary> = resp.json().await;
+    assert!(body.items.iter().any(|s| s.id == sbom_id));
+}
+
+/// Verifies that deleting an SBOM cascades to related join table rows.
+#[test_context(TestContext)]
+#[tokio::test]
+async fn test_delete_sbom_cascades_to_join_tables(ctx: &TestContext) {
+    let sbom_id = ctx.seed_sbom_with_relations("test-sbom-4").await;
+    ctx.delete(&format!("/api/v2/sbom/{}", sbom_id)).await;
+
+    let packages = ctx.query_sbom_packages(sbom_id).await;
+    assert!(packages.iter().all(|p| p.deleted_at.is_some()));
+}
```
