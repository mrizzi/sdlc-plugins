# External API Claim Verification

## Detected Claim

**Section:** Requirements (Section 4)

**Claim:** "PR reviews cannot be updated after initial submission" / "The GitHub API does not support modifying a submitted review"

**Requirement context:** The user's requirement states: "PR reviews cannot be updated after initial submission so always create a new review" with the note "The GitHub API does not support modifying a submitted review."

## Verification Result

**Status:** INCORRECT

The GitHub REST API **does** support updating a submitted pull request review. The relevant endpoint is:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

**Documentation:** [GitHub REST API — Update a review for a pull request](https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request)

**Evidence:**
- The `PUT` endpoint accepts a `body` parameter to update the review's body text after submission.
- This endpoint has been part of the GitHub REST API and is documented in the official GitHub API reference.

## Recommended Correction

The requirement should be revised to remove the incorrect claim. Instead of:

> "PR reviews cannot be updated after initial submission so always create a new review"

Suggested corrected language:

> "Update the existing PR review when re-running evals on the same PR, rather than creating a new review"

This leverages the `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` endpoint to update an existing review in place, avoiding duplicate review comments on the PR.
