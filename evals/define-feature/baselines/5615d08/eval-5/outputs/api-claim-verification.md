# External API Claim Verification

## Detected Claim

In the **Requirements** section (Section 4), the following claim was identified:

> "PR reviews cannot be updated after initial submission"
> "The GitHub API does not support modifying a submitted review"

This asserts that the GitHub REST API lacks the capability to update a pull request review once it has been submitted.

## Verification Result: INCORRECT

The claim is **incorrect**. The GitHub REST API **does** support updating a submitted pull request review.

### Evidence

The GitHub REST API provides the following endpoint for updating a review:

**`PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`**

This endpoint allows updating the body of a submitted pull request review. It accepts the `review_id` of an existing submitted review and a new `body` parameter to replace the review content.

Documentation reference: [GitHub REST API - Update a pull request review](https://docs.github.com/en/rest/pulls/reviews#update-a-pull-request-review)

## Suggested Corrected Language

The requirement row currently reads:

| Requirement | Notes | Is MVP? |
|---|---|---|
| PR reviews cannot be updated after initial submission so always create a new review | The GitHub API does not support modifying a submitted review | Yes |

Suggested correction:

| Requirement | Notes | Is MVP? |
|---|---|---|
| Update existing eval review when a new run completes, or create a new review if none exists | Use `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update an existing review | Yes |

This correction reflects the actual API capability and avoids creating duplicate reviews on successive eval runs.
