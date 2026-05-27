# External API Claim Verification

## Claim Detected

**Section:** Requirements (Section 4)

**Claim:** "PR reviews cannot be updated after initial submission" / "The GitHub API does not support modifying a submitted review"

**Requirement context:** The user states that because PR reviews cannot be updated, the system should always create a new review rather than updating an existing one.

## Verification Result

**Status: INCORRECT**

The GitHub REST API **does** support updating a submitted pull request review. The relevant endpoint is:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

**Documentation:** [GitHub REST API - Update a review for a pull request](https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request)

This endpoint accepts a `body` parameter and allows modifying the review body of an already-submitted review. This means the system can update an existing review in place rather than always creating a new one.

## Evidence

- **Endpoint:** `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`
- **Method:** PUT
- **Purpose:** Update the body text of a pull request review that has already been submitted
- **Parameters:** `body` (string, required) - The body text of the review

## Suggested Correction

The requirement "PR reviews cannot be updated after initial submission so always create a new review" should be revised. The corrected language should acknowledge that the GitHub API supports updating submitted reviews and reframe the requirement as a design choice rather than an API limitation.

**Original wording:**
> PR reviews cannot be updated after initial submission so always create a new review | The GitHub API does not support modifying a submitted review

**Suggested corrected wording:**
> Update the existing eval review if one was previously posted; create a new review only on the first run | Use `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update existing reviews
