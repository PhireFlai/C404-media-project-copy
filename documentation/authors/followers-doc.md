# Follower API Documentation

## Endpoints

---

## URL: /api/authors/{userId}/followers/
### Method: GET
### Description: Retrieve a list of all followers for a given userId of a author.

### When the API endpoint should be used
- Use this endpoint when you need to fetch a list of all authors that follow a given author

### How the API endpoint should be used
- Send a GET request to `/api/authors/{userId}/followers/`.

### Why the API endpoint should or should not be used
- Use this endpoint to get a comprehensive list of all followers, including their basic information such as username, email, profile picture, followers, and friends.

### Request
- **Method**: GET
- **URL**: `/api/authors/{userId}/followers/`
- **Headers**: None required

### JSON Fields in Response
- **Followers**: `List` authors that follow the user
  - **Example**: {
        "id": "d2d7dea6-5708-40a5-b89a-324b89b226d9",
        "username": "Testuser",
        "profile_picture": null,
        "followers": [],
        "friends": ["1493e30c-b8a6-467b-b78e-cb76529a040f"]
    },
  - **Purpose**: List of all authors that follows the author

### Example
```bash
GET /api/authors/1493e30c-b8a6-467b-b78e-cb76529a040f/followers/
```
### Response
```bash
[
    {
        "id": "d2d7dea6-5708-40a5-b89a-324b89b226d9",
        "username": "Testuser",
        "profile_picture": null,
        "followers": [],
        "friends": ["1493e30c-b8a6-467b-b78e-cb76529a040f"]
    },
    {
        "id": "1493e30c-b8a6-467b-b78e-cb76529a040f",
        "username": "admin",
        "profile_picture": "http://127.0.0.1:8000/media/profile_pictures/1493e30c-b8a6-467b-b78e-cb76529a040f.png",
        "followers": ["d2d7dea6-5708-40a5-b89a-324b89b226d9","d575ab72-2909-445b-8af9-e18173cb5adc"],
        "friends": ["d2d7dea6-5708-40a5-b89a-324b89b226d9"]
    },
    # ... More user objects
]
```

## URL: /api/authors/{userId}/following/
### Method: GET
### Description: Retrieve a list of all users that userId follows

### When the API endpoint should be used
- Use this endpoint when you need to fetch a list of all authors that a given author follows

### How the API endpoint should be used
- Send a GET request to `/api/authors/{userId}/following/`.

### Why the API endpoint should or should not be used
- Use this endpoint to get a comprehensive list of all following authors, including their basic information such as username, email, profile picture, followers, and friends.

### Request
- **Method**: GET
- **URL**: `/api/authors/{userId}/following/`
- **Headers**: None required

### JSON Fields in Response
- **Followers**: `List` authors that follow the user
  - **Example**: {
        "id": "d2d7dea6-5708-40a5-b89a-324b89b226d9",
        "username": "Testuser",
        "profile_picture": null,
        "followers": [],
        "friends": ["1493e30c-b8a6-467b-b78e-cb76529a040f"]
    },
  - **Purpose**: List of all authors that follows the author

### Example
```bash
GET /api/authors/1493e30c-b8a6-467b-b78e-cb76529a040f/following/
```
### Response
```bash
[
    {
        "id": "d2d7dea6-5708-40a5-b89a-324b89b226d9",
        "username": "Testuser",
        "profile_picture": null,
        "followers": [],
        "friends": ["1493e30c-b8a6-467b-b78e-cb76529a040f"]
    },
    {
        "id": "1493e30c-b8a6-467b-b78e-cb76529a040f",
        "username": "admin",
        "profile_picture": "http://127.0.0.1:8000/media/profile_pictures/1493e30c-b8a6-467b-b78e-cb76529a040f.png",
        "followers": ["d2d7dea6-5708-40a5-b89a-324b89b226d9","d575ab72-2909-445b-8af9-e18173cb5adc"],
        "friends": ["d2d7dea6-5708-40a5-b89a-324b89b226d9"]
    },
    # ... More user objects
]
```

## URL: /api/authors/{objectId}/accept-follow-request/authors/{actorId}/
### Method: POST
### Description: Approve or deny a follow request.

### When the API endpoint should be used
- Use this endpoint to approve or deny a follow request sent by actorId to objectId

### How the API endpoint should be used
- Send a POST request to `/api/authors/{objectId}/accept-follow-request/authors/{actorId}`.

### Why the API endpoint should or should not be used
- Use this endpoint to approve or deny a follow request to add a follower to a user upon consent

### Request
- **Method**: POST
- **URL**: `/api/authors/{objectId}/accept-follow-request/authors/{actorId}/`
- **Headers**: 
  - Authorization: Token 993b43e8f2a...
- **Body**: None

### JSON Fields in Response
- **message**: `string` response on successfulness
  - **Example**: 
  {
  "message": "Follower request accepted successfully"
  }
  - **Purpose**: Result of successfulness

### Example
```bash
POST /api/authors/1493e30c.../accept-follow-request/authors/d2d7dea6.../?action=accept
-H "Authorization: Token 993b43e8f2a..."
```
### Response
```bash
{
  "message": "Follow request accepted successfully"
}
```


## URL: /api/authors/{followerId}/unfollow/authors/{followedId}/
### Method: POST
### Description: Approve or deny a follow request.

### When the API endpoint should be used
- Use this endpoint to unfollow followedId from followerId

### How the API endpoint should be used
- Send a POST request to `/api/authors/{followerId}/unfollow/authors/{followedId}`.

### Why the API endpoint should or should not be used
- Use this unfollow id followedId from user followerId

### Request
- **Method**: POST
- **URL**: `/api/authors/{followerId}/unfollow/authors/{followedId}/`
- **Headers**: 
  - Authorization: Token 993b43e8f2a...
- **Body**: None

### JSON Fields in Response
- **message**: `string` response on successfulness
  - **Example**: 
{
  "message": "Unfollowed successfully"
}
  - **Purpose**: Result of successfulness

### Example
```bash
POST /api/authors/1493e30c.../unfollow/authors/d2d7dea6.../
-H "Authorization: Token 993b43e8f2a..."
```
### Response
```bash
{
  "message": "Unfollowed successfully"
}
```


## URL: /api/authors/{followedId}/remove-follower/authors/{followerId}/
### Method: POST
### Description: Approve or deny a follow request.

### When the API endpoint should be used
- Use this endpoint to remove follower followerId from followedId

### How the API endpoint should be used
- Send a POST request to `/api/authors/{followedId}/remove-follower/authors/{followerId}`.

### Why the API endpoint should or should not be used
- Use this remove a follower with id followerId from user followedId

### Request
- **Method**: POST
- **URL**: `/api/authors/{followedId}/remove-follower/authors/{followerId}/`
- **Headers**: 
  - Authorization: Token 993b43e8f2a...
- **Body**: None

### JSON Fields in Response
- **message**: `string` response on successfulness
  - **Example**: 
{
  "message": "Follower removed successfully"
}
  - **Purpose**: Result of successfulness

### Example
```bash
POST /api/authors/1493e30c.../remove-follower/authors/d2d7dea6.../
-H "Authorization: Token 993b43e8f2a..."
```
### Response
```bash
{
  "message": "Follower removed successfully"
}
```