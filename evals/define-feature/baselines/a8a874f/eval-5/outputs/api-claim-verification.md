# External API Claim Verification

## Detected Claim

In **Section 4 -- Requirements**, the following claim was identified:

> "PR reviews cannot be updated after initial submission so always create a new review"
> Notes: "The GitHub API does not support modifying a submitted review"

This asserts that the GitHub REST API lacks the capability to update a PR review after it has been submitted.

## Verification Result: INCORRECT

The claim is **incorrect**. The GitHub REST API does support updating a submitted pull request review.

### Evidence

The GitHub REST API provides the following endpoint for updating a review:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows modifying the body of a previously submitted pull request review. It accepts a JSON payload with the updated `body` field and returns the updated review object.

Documentation reference: GitHub REST API -- Pull Request Reviews -- Update a pull request review.

### Suggested Corrected Language

**Original requirement:**
> PR reviews cannot be updated after initial submission so always create a new review

**Corrected requirement:**
> Update existing PR review when re-running evals on the same pull request

**Original notes:**
> The GitHub API does not support modifying a submitted review

**Corrected notes:**
> Use `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update an existing review instead of creating duplicate reviews
