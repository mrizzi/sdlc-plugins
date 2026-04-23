<!-- SYNTHETIC TEST DATA — mock GitHub PR review comments for eval testing; simulates `gh api repos/{owner}/{repo}/pulls/{number}/reviews` and `gh api repos/{owner}/{repo}/pulls/{number}/comments` output -->

## Reviews (`gh api repos/trustify/trustify-backend/pulls/744/reviews`)

```json
[
  {
    "id": 20001,
    "user": {
      "login": "reviewer-a",
      "id": 10001
    },
    "body": "Good approach overall. A few things to address before we can merge.",
    "state": "CHANGES_REQUESTED",
    "submitted_at": "2026-04-20T14:30:00Z"
  }
]
```

## Review Comments (`gh api repos/trustify/trustify-backend/pulls/744/comments`)

```json
[
  {
    "id": 30001,
    "pull_request_review_id": 20001,
    "user": {
      "login": "reviewer-a",
      "id": 10001
    },
    "body": "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.",
    "path": "modules/fundamental/src/sbom/service/sbom.rs",
    "line": 60,
    "side": "RIGHT",
    "created_at": "2026-04-20T14:32:00Z",
    "updated_at": "2026-04-20T14:32:00Z",
    "in_reply_to_id": null
  },
  {
    "id": 30002,
    "pull_request_review_id": 20001,
    "user": {
      "login": "reviewer-a",
      "id": 10001
    },
    "body": "The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:\n\n```sql\nCREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;\n```",
    "path": "migration/src/m0042_sbom_soft_delete/mod.rs",
    "line": 14,
    "side": "RIGHT",
    "created_at": "2026-04-20T14:35:00Z",
    "updated_at": "2026-04-20T14:35:00Z",
    "in_reply_to_id": null
  },
  {
    "id": 30003,
    "pull_request_review_id": 20001,
    "user": {
      "login": "reviewer-a",
      "id": 10001
    },
    "body": "Nit: `context(\"SBOM not found\")` is misleading here because `.context()` wraps the error message for the anyhow chain — it doesn't mean the SBOM wasn't found. The actual 404 is handled by `ok_or(AppError::NotFound(...))` on the next line. Consider changing the context message to something like `\"Failed to fetch SBOM\"` to avoid confusion in error logs.",
    "path": "modules/fundamental/src/sbom/endpoints/mod.rs",
    "line": 18,
    "side": "RIGHT",
    "created_at": "2026-04-20T14:38:00Z",
    "updated_at": "2026-04-20T14:38:00Z",
    "in_reply_to_id": null
  },
  {
    "id": 30004,
    "pull_request_review_id": 20001,
    "user": {
      "login": "reviewer-a",
      "id": 10001
    },
    "body": "Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` — so direct GET still returns deleted SBOMs. Is that intentional?",
    "path": "modules/fundamental/src/sbom/endpoints/get.rs",
    "line": 1,
    "side": "RIGHT",
    "created_at": "2026-04-20T14:40:00Z",
    "updated_at": "2026-04-20T14:40:00Z",
    "in_reply_to_id": null
  }
]
```
