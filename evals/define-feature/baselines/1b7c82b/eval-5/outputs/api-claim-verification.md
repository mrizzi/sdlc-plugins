# External API Claim Verification

## Detected Claim

In the Requirements section (Section 4), the following claim was made:

> "PR reviews cannot be updated after initial submission so always create a new review"

With the supporting note:

> "The GitHub API does not support modifying a submitted review"

## Verification Finding

This claim is **INCORRECT**. The GitHub REST API **does** support updating a submitted pull request review. The endpoint is:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint accepts a `body` parameter and allows the review body to be updated after submission. The review's state (APPROVED, CHANGES_REQUESTED, COMMENT) is preserved, and the body content is replaced with the new value.

Reference: GitHub REST API documentation for Pull Request Reviews.

## Suggested Corrected Language

**Original requirement:**
> PR reviews cannot be updated after initial submission so always create a new review

**Corrected requirement:**
> Update the existing PR review when re-running evals on the same PR, using the GitHub REST API `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` endpoint; create a new review only on the first eval run

**Original note:**
> The GitHub API does not support modifying a submitted review

**Corrected note:**
> The GitHub REST API supports updating a submitted review via `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`; store the review ID from the initial POST to enable subsequent updates
