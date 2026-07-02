# External API Claim Verification

## Detected Claim

In **Section 4 — Requirements**, the following claim was identified:

> **Claim:** "PR reviews cannot be updated after initial submission"
> **Supporting statement:** "The GitHub API does not support modifying a submitted review"

This asserts a limitation of the GitHub REST API — that once a pull request review is submitted, it cannot be modified.

## Verification Result: INCORRECT

The claim is **incorrect**. The GitHub REST API does support updating a submitted pull request review.

### Evidence

The GitHub REST API provides the following endpoint for updating a review:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows updating the body of a previously submitted pull request review. It accepts a `body` parameter (string, required) containing the updated text of the review.

**Documentation reference:** [GitHub REST API — Update a review for a pull request](https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request)

### Impact on Feature Description

The requirement row stating "PR reviews cannot be updated after initial submission so always create a new review" is based on an incorrect premise. The design decision to always create a new review instead of updating an existing one may still be valid for other reasons (e.g., preserving review history), but the justification should not claim the API lacks update support.

## Suggested Corrected Language

**Original requirement:**
> PR reviews cannot be updated after initial submission so always create a new review

**Original notes:**
> The GitHub API does not support modifying a submitted review

**Corrected requirement:**
> Create a new review for each eval run rather than updating a previous review

**Corrected notes:**
> Preserves review history so reviewers can compare results across runs. Note: the GitHub API does support updating reviews via `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`, but creating new reviews provides better auditability.
