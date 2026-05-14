# External API Claim Verification

## Detected Claim

**Section:** Requirements (Section 4)

**Claim text:** "PR reviews cannot be updated after initial submission" / "The GitHub API does not support modifying a submitted review"

**Context:** The user's requirement states: "PR reviews cannot be updated after initial submission so always create a new review" with the note "The GitHub API does not support modifying a submitted review". This asserts that the GitHub REST API lacks the capability to update a PR review once it has been submitted.

## Verification

**API checked:** GitHub REST API

**Finding:** The claim is **incorrect**. The GitHub REST API does support updating a submitted pull request review.

**Evidence:**

- **Endpoint:** `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`
- **Method:** PUT
- **Purpose:** Update the body (top-level comment) of an existing pull request review
- **Documentation:** [GitHub REST API - Update a pull request review](https://docs.github.com/en/rest/pulls/reviews#update-a-pull-request-review)

The `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` endpoint accepts a `body` parameter and updates the specified review on the given pull request. This means submitted reviews can be modified after initial submission.

## Verification Result

**Status:** INCORRECT -- the API does support the claimed-absent capability.

## Suggested Corrected Language

**Original requirement:** "PR reviews cannot be updated after initial submission so always create a new review"

**Original note:** "The GitHub API does not support modifying a submitted review"

**Corrected requirement:** "Update the existing PR review when re-running evals on the same PR, or create a new review if none exists"

**Corrected note:** "Use PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id} to update an existing review"
