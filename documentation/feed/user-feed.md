# URL: /api/authors/feed/

## When the API endpoint should be used
This endpoint should be used when you want to retrieve a personalized feed of posts for the authenticated user. The feed includes:
- The user's own posts (excluding deleted ones).
- Public posts from any author.
- Friends-only posts from mutual friends.
- Unlisted posts from users the authenticated user follows.

## How the API endpoint should be used
Send a **GET** request to `/api/authors/feed/` with a valid authentication token in the `Authorization` header.

## Why the API endpoint should or should not be used
- It should be used to fetch posts tailored to the authenticated user's relationships (friends and followed users).
- It ensures that visibility rules are respected (e.g., friends-only posts are only shown to friends).
- It should not be used to retrieve all posts globally; for that, use the public posts endpoint.

## Example 1: Request
**GET** request to retrieve the user’s feed:

```bash
GET http://nodebbbb/api/authors/feed/
-H "Authorization: Token 993b43e8f2a..."
```

## Example 2: Response
```json
[
    {
        "id": "f0d5318d-a8d2-4788-97c7-6007f69d8a70",
        "author": {
            "id": "3c5a7a19-bcf6-4ad7-bb7a-b98e54159fb5",
            "username": "friend_user"
        },
        "title": "A Friend's Post",
        "content": "This is a post that only friends can see.",
        "visibility": "friends-only",
        "created_at": "2025-03-09T12:34:56Z"
    },
    {
        "id": "da770524-2ea8-493b-9fa5-f59f4cfa61d4",
        "author": {
            "id": "1493e30c-b8a6-467b-b78e-cb76529a040f",
            "username": "admin"
        },
        "title": "Public Post",
        "content": "This post is visible to everyone.",
        "visibility": "public",
        "created_at": "2025-03-08T08:30:00Z"
    }
]
```
