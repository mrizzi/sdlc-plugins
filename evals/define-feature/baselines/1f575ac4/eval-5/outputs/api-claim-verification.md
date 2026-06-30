# External API Claim Verification

## Detected Claim

In the **Requirements** section (Section 4), the following claim was identified:

> "PR reviews cannot be updated after initial submission" / "The GitHub API does not support modifying a submitted review"

This claim asserts that the GitHub REST API lacks the capability to update or modify a pull request review after it has been submitted, and therefore a new review must always be created.

## Verification Result: INCORRECT

The claim is **incorrect**. The GitHub REST API does support updating a submitted pull request review.

### Evidence

The GitHub REST API provides the following endpoint for updating a pull request review:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows updating the body of a submitted review. It accepts the `review_id` of an existing review and a new `body` parameter to replace the review content.

Documentation reference: GitHub REST API — Pull Request Reviews — "Update a pull request review"

### Suggested Corrected Language

**Original requirement:**
> PR reviews cannot be updated after initial submission so always create a new review

**Original notes:**
> The GitHub API does not support modifying a submitted review

**Corrected requirement:**
> Update existing PR review when re-running evals on the same PR, or create a new review if none exists

**Corrected notes:**
> Use `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update an existing review
