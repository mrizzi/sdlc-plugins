# External API Claim Verification

## Detected Claim

In **Section 4 — Requirements**, the following claim was identified:

> "PR reviews cannot be updated after initial submission so always create a new review"
>
> Notes: "The GitHub API does not support modifying a submitted review"

This asserts that the GitHub REST API lacks the capability to update a PR review after it has been submitted.

## Verification Result: INCORRECT

The claim is **incorrect**. The GitHub REST API does support updating a submitted pull request review.

### Evidence

The GitHub REST API provides the following endpoint for updating a review:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint accepts a `body` parameter to update the review's text content after submission. It is documented in the official GitHub REST API reference under the "Pull Request Reviews" section.

This means it is not necessary to always create a new review — an existing submitted review can be updated in place using this endpoint.

## Suggested Corrected Language

**Original requirement:**
> PR reviews cannot be updated after initial submission so always create a new review

**Corrected requirement:**
> Update an existing PR review when re-running evals on the same PR, rather than creating duplicate reviews

**Original notes:**
> The GitHub API does not support modifying a submitted review

**Corrected notes:**
> Use `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update an existing review in place
