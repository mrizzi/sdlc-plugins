# Jira Comment

## API Call: Add Comment

**Endpoint:** `/rest/api/3/issue/{issueKey}/comment`

**Request Body:**

```json
{
  "body": {
    "version": 1,
    "type": "doc",
    "content": [
      {
        "type": "paragraph",
        "content": [
          {
            "type": "text",
            "text": "This feature was defined using the "
          },
          {
            "type": "text",
            "text": "sdlc-workflow/define-feature",
            "marks": [{ "type": "code" }]
          },
          {
            "type": "text",
            "text": " skill (v0.9.1) from "
          },
          {
            "type": "text",
            "text": "https://github.com/mrizzi/sdlc-plugins",
            "marks": [
              {
                "type": "link",
                "attrs": {
                  "href": "https://github.com/mrizzi/sdlc-plugins"
                }
              }
            ]
          },
          {
            "type": "text",
            "text": "."
          }
        ]
      }
    ]
  }
}
```
