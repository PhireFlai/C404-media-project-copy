# Friends API Documentation

## How to Check if Two Users Are Friends
You can determine whether two users are friends by checking if they mutually follow each other.

## Logic for Friendship (Implemented in Backend)
When User B accepts a follow request from User A:

- User A is added to User B's followers.
- The system checks if User A already follows User B.
- If they mutually follow each other, they are added as friends.
- This process is handled in the Accept Follow Request API:
```python
if follow_request.actor.followers.filter(id=follow_request.object.id).exists():
    follow_request.actor.friends.add(follow_request.object)
    follow_request.object.friends.add(follow_request.actor)
```

## Result
- If both users follow each other, they are automatically added to each other's friends list.
- Friends-only posts will now be visible to each other.


## Endpoints

---

## URL: /api/authors/{userId}/friends-posts/
### Method: GET
### Description: Retrieve a list of posts made by users who are mutual friends with the given author.

### When to Use This Endpoint
- Use this endpoint when you need to fetch **only** the posts made by authors who are friends (i.e., mutually connected) with a given user.
- This endpoint is useful when a client application needs to display content that is exclusively shared among friends.

### How to Use This Endpoint
- Send a **GET** request to `/api/authors/{userId}/friends-posts/` with a valid authentication token in the `Authorization` header.

### Why Use This Endpoint
- It filters posts so that only those authored by users who are mutual friends of the specified user are returned.
- This ensures that the user sees posts that are intended to be shared among friends, as opposed to the general public feed.

### Request
- **Method:** `GET`
- **URL:** `/api/authors/{userId}/friends-posts/`
- **Headers:** 
  - `Authorization: Token <your-auth-token>`

### JSON Response Format
The endpoint returns a JSON array of post objects. Each post object contains details such as:

- **id:** UUID of the post.
- **author:** An object containing the friend's details:
  - **id:** UUID of the friend.
  - **username:** Friend’s username.
- **title:** Title of the post.
- **content:** Content of the post.
- **visibility:** The visibility level (typically `"friends-only"` for this endpoint).
- **created_at:** Timestamp when the post was created.

#### Example Response
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
        "title": "Another Friend's Post",
        "content": "Only my friends can view this.",
        "visibility": "friends-only",
        "created_at": "2025-03-08T08:30:00Z"
    }
]
```

### Example
```bash
GET /api/authors/1493e30c-b8a6-467b-b78e-cb76529a040f/friends-posts/
-H "Authorization: Token 993b43e8f2a..."
```
