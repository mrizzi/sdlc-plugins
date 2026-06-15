# External API Claim Verification

## Claim Detected

**Section:** Requirements (Section 4)
**Claim:** "PR reviews cannot be updated after initial submission" / "The GitHub API does not support modifying a submitted review"

## Verification Result: INCORRECT

The claim is **incorrect**. The GitHub REST API does support updating a submitted pull request review.

### Evidence

The GitHub REST API provides the following endpoint for updating a pull request review:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

**Documentation:** https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request

This endpoint allows modifying the body of a submitted review after initial submission. The review's state (APPROVED, CHANGES_REQUESTED, COMMENTED) cannot be changed via this endpoint, but the review body text can be updated.

### Suggested Correction

**Original requirement:** "PR reviews cannot be updated after initial submission so always create a new review"
**Original notes:** "The GitHub API does not support modifying a submitted review"

**Corrected requirement:** "Update existing eval review if one already exists; create a new review only on first run"
**Corrected notes:** "Use PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id} to update an existing review"

### Impact

The original design assumed reviews are immutable, leading to a requirement to always create new reviews. Since reviews can be updated, the implementation should update existing reviews instead of creating duplicates, providing a cleaner PR review history.
