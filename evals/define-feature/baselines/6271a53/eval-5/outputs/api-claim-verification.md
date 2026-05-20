# External API Claim Verification

## Detected Claim

The following claim was found in **Section 4 — Requirements**, row 4:

> "PR reviews cannot be updated after initial submission so always create a new review"

With the supporting note:

> "The GitHub API does not support modifying a submitted review"

## Verification Result: INCORRECT

The claim that PR reviews cannot be updated after initial submission is **factually incorrect**. The GitHub REST API provides the following endpoint for updating a submitted pull request review:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows updating the body of a previously submitted review. It accepts the `review_id` of an existing review and a new `body` parameter, enabling modifications after the review has been submitted.

**Reference**: [GitHub REST API — Update a pull request review](https://docs.github.com/en/rest/pulls/reviews#update-a-pull-request-review)

## Impact on Requirements

The incorrect claim led to a requirement that always creates a new review instead of updating an existing one. This would result in duplicate review comments on PRs when evals are re-run (e.g., after a force-push or additional commits), creating unnecessary noise for reviewers.

## Suggested Corrected Language

**Original requirement row:**

| Requirement | Notes | Is MVP? |
|---|---|---|
| PR reviews cannot be updated after initial submission so always create a new review | The GitHub API does not support modifying a submitted review | Yes |

**Corrected requirement row:**

| Requirement | Notes | Is MVP? |
|---|---|---|
| Update an existing eval review when re-running on the same PR, or create a new review if none exists | Use `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update an existing review; fall back to creating a new review if no prior eval review is found | Yes |
