# External API Claim Verification

## Claim Detected

**Section:** Requirements (Section 4), Requirement #4

**Claim:** "PR reviews cannot be updated after initial submission" / "The GitHub API does not support modifying a submitted review"

**Category:** API limitation claim -- asserts that an external API lacks a specific capability.

## Verification Process

The claim was verified against the GitHub REST API official documentation.

**Search target:** GitHub REST API endpoints for pull request reviews, specifically update/modify operations on submitted reviews.

**Finding:** The GitHub REST API **does** support updating a submitted pull request review via:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows modifying the body of a previously submitted review. It is documented in the official GitHub REST API reference under "Pull request reviews."

**Documentation reference:** https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request

## Verification Result

**Status: INCORRECT**

The claim is factually wrong. The GitHub REST API does support modifying a submitted review using the `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` endpoint. The review body can be updated after initial submission.

## Recommended Correction

The original requirement stated:

> "PR reviews cannot be updated after initial submission so always create a new review" with the note "The GitHub API does not support modifying a submitted review"

**Corrected language:**

- **Requirement:** "Update existing PR review when re-running evals on the same PR, or create a new review if none exists"
- **Notes:** "Use the GitHub REST API `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` endpoint to update an existing review body"

This correction reflects the actual API capability and avoids creating duplicate reviews on repeated eval runs.
