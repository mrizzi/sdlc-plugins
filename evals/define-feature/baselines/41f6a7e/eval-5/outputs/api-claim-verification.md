# External API Claim Verification

## Detected Claim

In **Section 4 -- Requirements**, the following claim was identified:

> "PR reviews cannot be updated after initial submission so always create a new review"
> Notes: "The GitHub API does not support modifying a submitted review"

This asserts that the GitHub REST API lacks the capability to update a PR review after it has been submitted.

## Verification Result: INCORRECT

The claim is **incorrect**. The GitHub REST API does support updating a submitted pull request review.

### Evidence

The GitHub REST API provides the following endpoint:

**`PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`**

This endpoint updates the body of a previously submitted pull request review. It accepts the `review_id` of the existing review and a new `body` parameter, allowing the review content to be modified after initial submission.

Documentation reference: GitHub REST API > Pull Reviews > Update a review for a pull request.

### Suggested Corrected Language

**Original requirement:**
> PR reviews cannot be updated after initial submission so always create a new review

**Corrected requirement:**
> Update the existing PR review when re-running evals on the same PR, rather than creating a new review each time

**Original notes:**
> The GitHub API does not support modifying a submitted review

**Corrected notes:**
> Use `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update the existing review body with the latest eval results
