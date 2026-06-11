# External API Claim Verification

## Detected Claim

**Section:** Requirements (Section 4)

**Claim:** "PR reviews cannot be updated after initial submission" and "The GitHub API does not support modifying a submitted review."

**Requirement row:** "PR reviews cannot be updated after initial submission so always create a new review | The GitHub API does not support modifying a submitted review | Yes"

## Verification

**Status:** INCORRECT

The GitHub REST API does support updating a submitted pull request review. The relevant endpoint is:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows modifying the body of a previously submitted review. It is documented in the official GitHub REST API reference for pull request reviews.

**Evidence:**
- **Method:** `PUT`
- **Endpoint:** `/repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`
- **Documentation:** https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request
- **Capability:** Updates the body text of a submitted review

## Suggested Corrected Language

**Original requirement:**
> PR reviews cannot be updated after initial submission so always create a new review

**Corrected requirement:**
> Update existing PR reviews with latest eval results when a prior review exists for the same run, or create a new review if none exists

**Original notes:**
> The GitHub API does not support modifying a submitted review

**Corrected notes:**
> Use the GitHub REST API `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` endpoint to update an existing review, or `POST` to create a new one
