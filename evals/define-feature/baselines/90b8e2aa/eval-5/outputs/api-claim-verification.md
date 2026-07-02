# External API Claim Verification

## Claim Detected

**Section:** Requirements (Section 4)
**Requirement:** "PR reviews cannot be updated after initial submission so always create a new review"
**Note:** "The GitHub API does not support modifying a submitted review"

## Verification Result: INCORRECT

The claim that the GitHub API does not support modifying a submitted review is **incorrect**.

The GitHub REST API provides the following endpoint for updating a pull request review:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows updating the body of a submitted review after initial submission. It is documented in the official GitHub REST API reference under Pull Request Reviews.

**Documentation reference:** https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request

## Suggested Correction

The requirement should be revised to reflect the actual API capability. Instead of always creating a new review, the feature can update an existing eval review on subsequent CI runs for the same PR.

**Original requirement:** "PR reviews cannot be updated after initial submission so always create a new review"
**Original note:** "The GitHub API does not support modifying a submitted review"

**Corrected requirement:** "Update the existing eval review on subsequent runs rather than creating duplicate reviews"
**Corrected note:** "Use `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update an existing review"
