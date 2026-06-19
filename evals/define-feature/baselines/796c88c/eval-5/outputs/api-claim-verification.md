# External API Claim Verification

## Detected Claim

In **Section 4 — Requirements**, the following claim was identified:

> "PR reviews cannot be updated after initial submission so always create a new review"
> Notes: "The GitHub API does not support modifying a submitted review"

This asserts that the GitHub REST API lacks the capability to update a PR review after it has been submitted.

## Verification Result: INCORRECT

The claim is **incorrect**. The GitHub REST API does support updating a submitted pull request review.

### Evidence

The GitHub REST API provides the following endpoint:

**`PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`**

This endpoint allows updating the body of a submitted pull request review. It accepts the `review_id` of an existing review and a new `body` parameter to replace the review content.

Documentation reference: [GitHub REST API — Update a review for a pull request](https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request)

### Suggested Corrected Language

**Original requirement:** "PR reviews cannot be updated after initial submission so always create a new review"

**Corrected requirement:** "Update the existing PR review when re-running evals on the same PR, rather than creating duplicate reviews"

**Original notes:** "The GitHub API does not support modifying a submitted review"

**Corrected notes:** "Use `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update an existing review in place"
