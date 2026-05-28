# External API Claim Verification

## Detected Claim

In **Section 4 -- Requirements**, the following claim was identified:

> "PR reviews cannot be updated after initial submission so always create a new review"
> Notes: "The GitHub API does not support modifying a submitted review"

This asserts that the GitHub REST API lacks the capability to update or modify a pull request review after it has been submitted.

## Verification Result: INCORRECT

The claim is **incorrect**. The GitHub REST API does support updating a submitted pull request review.

### Evidence

The GitHub REST API provides the following endpoint for updating a review:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows updating the body of a submitted pull request review. It accepts a `body` parameter and returns the updated review object. This directly contradicts the claim that "PR reviews cannot be updated after initial submission" and that "The GitHub API does not support modifying a submitted review."

Reference: GitHub REST API documentation -- Pull Request Reviews -- Update a pull request review.

## Suggested Corrected Language

**Original requirement:**
> PR reviews cannot be updated after initial submission so always create a new review

**Corrected requirement:**
> Update the existing PR review when re-running evals on the same PR; create a new review only on the first run

**Original notes:**
> The GitHub API does not support modifying a submitted review

**Corrected notes:**
> Use `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update an existing review's body with the latest eval results

## Action Taken

The incorrect claim was flagged to the user with evidence from the GitHub REST API documentation. The corrected language was incorporated into the Feature description preview and the Jira issue.
