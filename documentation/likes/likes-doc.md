# Likes API Documentation

## URL: /api/authors/{AUTHOR_SERIAL}/inbox

### Method: POST

### Description: Send a like object to AUTHOR_SERIAL

### When the API endpoint should be used

- Use this endpoint to send a like object to a specific author.

### How the API endpoint should be used

- Send a POST request to `/api/authors/{AUTHOR_SERIAL}/inbox` with the like object in the request body.

### Why the API endpoint should or should not be used

- Use this endpoint to notify an author that their post or comment has been liked.

### Request

- **Method**: POST
- **URL**: `/api/authors/{AUTHOR_SERIAL}/inbox`
- **Headers**:
  - `Content-Type: application/json`
- **Body**:
  ```json
  {
    "type": "like",
    "author": {
      "type": "author",
      "id": "http://nodeaaaa/api/authors/111",
      "displayName": "Greg Johnson",
      "github": "http://github.com/gjohnson",
      "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
    },
    "object": "http://nodebbbb/api/authors/222/posts/249"
  }
  ```

### JSON Fields in Response

- **message**: `string` - A message indicating the result of the request.
  - **Example**: `Like sent successfully`
  - **Purpose**: Informs the client whether the request was successful.

### Example

```bash
POST /api/authors/111/inbox
-H "Content-Type: application/json"
-d '{
      "type": "like",
      "author": {
        "type": "author",
        "id": "http://nodeaaaa/api/authors/111",
        "displayName": "Greg Johnson",
        "github": "http://github.com/gjohnson",
        "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
      },
      "object": "http://nodebbbb/api/authors/222/posts/249"
    }'
```

#### Response

```bash
{
  "message": "Like sent successfully"
}
```

## URL: /api/authors/{AUTHOR_SERIAL}/posts/{POST_SERIAL}/likes

### Method: GET

### Description: Retrieve a list of likes from other authors on AUTHOR_SERIAL's post POST_SERIAL

### When the API endpoint should be used

- Use this endpoint to fetch a list of likes from other authors on a specific post.

### How the API endpoint should be used

- Send a GET request to `/api/authors/{AUTHOR_SERIAL}/posts/{POST_SERIAL}/likes`.

### Why the API endpoint should or should not be used

- Use this endpoint to get a comprehensive list of likes on a specific post.

### Request

- **Method**: GET
- **URL**: `/api/authors/{AUTHOR_SERIAL}/posts/{POST_SERIAL}/likes`
- **Headers**: None required

### JSON Fields in Response

- **id**: `string` (UUID) - The unique identifier of the like.
  - **Example**: `1493e30c-b8a6-467b-b78e-cb76529a040f`
  - **Purpose**: Uniquely identifies the like.
- **user**: `object` - The user who liked the post.
  - **id**: `string` (UUID) - The unique identifier of the user.
    - **Example**: `04f511c8-5cfe-4414-a125-e4a879188d38`
    - **Purpose**: Uniquely identifies the user.
  - **username**: `string` - The username of the user.
    - **Example**: `gregjohnson`
    - **Purpose**: The username of the user.
- **post**: `string` (UUID) - The unique identifier of the liked post.
  - **Example**: `1493e30c-b8a6-467b-b78e-cb76529a040f`
  - **Purpose**: Identifies the liked post.

### Example

```bash
GET /api/authors/111/posts/249/likes
```

### Response

```bash
[
  {
    "id": "1493e30c-b8a6-467b-b78e-cb76529a040f",
    "user": {
      "id": "04f511c8-5cfe-4414-a125-e4a879188d38",
      "username": "gregjohnson"
    },
    "post": "1493e30c-b8a6-467b-b78e-cb76529a040f"
  }
]
```

## URL: /api/posts/{POST_FQID}/likes

### Method: GET

### Description: Retrieve a list of likes from other authors on AUTHOR_SERIAL's post POST_SERIAL

### When the API endpoint should be used

- Use this endpoint to fetch a list of likes from other authors on a specific post.

### How the API endpoint should be used

- Send a GET request to `/api/posts/{POST_FQID}/likes`.

### Why the API endpoint should or should not be used

- Use this endpoint to get a comprehensive list of likes on a specific post.

### Request

- **Method**: GET
- **URL**: `/api/posts/{POST_FQID}/likes`
- **Headers**: None required

### JSON Fields in Response

- **id**: `string` (UUID) - The unique identifier of the like.
  - **Example**: `1493e30c-b8a6-467b-b78e-cb76529a040f`
  - **Purpose**: Uniquely identifies the like.
- **user**: `object` - The user who liked the post.
  - **id**: `string` (UUID) - The unique identifier of the user.
    - **Example**: `04f511c8-5cfe-4414-a125-e4a879188d38`
    - **Purpose**: Uniquely identifies the user.
  - **username**: `string` - The username of the user.
    - **Example**: `gregjohnson`
    - **Purpose**: The username of the user.
- **post**: `string` (UUID) - The unique identifier of the liked post.
  - **Example**: `1493e30c-b8a6-467b-b78e-cb76529a040f`
  - **Purpose**: Identifies the liked post.

### Example

```bash
GET /api/posts/249/likes
```

### Response

```bash
[
  {
    "id": "1493e30c-b8a6-467b-b78e-cb76529a040f",
    "user": {
      "id": "04f511c8-5cfe-4414-a125-e4a879188d38",
      "username": "gregjohnson"
    },
    "post": "1493e30c-b8a6-467b-b78e-cb76529a040f"
  }
]
```

## URL: /api/authors/{AUTHOR_SERIAL}/posts/{POST_SERIAL}/comments/{COMMENT_FQID}/likes

### Method: GET

### Description: Retrieve a list of likes from other authors on AUTHOR_SERIAL's post POST_SERIAL comment COMMENT_FQID

### When the API endpoint should be used

- Use this endpoint to fetch a list of likes from other authors on a specific comment.

### How the API endpoint should be used

- Send a GET request to `/api/authors/{AUTHOR_SERIAL}/posts/{POST_SERIAL}/comments/{COMMENT_FQID}/likes`.

### Why the API endpoint should or should not be used

- Use this endpoint to get a comprehensive list of likes on a specific comment.

### Request

- **Method**: GET
- **URL**: `/api/authors/{AUTHOR_SERIAL}/posts/{POST_SERIAL}/comments/{COMMENT_FQID}/likes`
- **Headers**: None required

### JSON Fields in Response

- **id**: `string` (UUID) - The unique identifier of the like.
  - **Example**: `1493e30c-b8a6-467b-b78e-cb76529a040f`
  - **Purpose**: Uniquely identifies the like.
- **user**: `object` - The user who liked the comment.
  - **id**: `string` (UUID) - The unique identifier of the user.
    - **Example**: `04f511c8-5cfe-4414-a125-e4a879188d38`
    - **Purpose**: Uniquely identifies the user.
  - **username**: `string` - The username of the user.
    - **Example**: `gregjohnson`
    - **Purpose**: The username of the user.
- **comment**: `string` (UUID) - The unique identifier of the liked comment.
  - **Example**: `1493e30c-b8a6-467b-b78e-cb76529a040f`
  - **Purpose**: Identifies the liked comment.

### Example

```bash
GET /api/authors/111/posts/249/comments/333/likes
```

### Response

```bash
[
  {
    "id": "1493e30c-b8a6-467b-b78e-cb76529a040f",
    "user": {
      "id": "04f511c8-5cfe-4414-a125-e4a879188d38",
      "username": "gregjohnson"
    },
    "comment": "1493e30c-b8a6-467b-b78e-cb76529a040f"
  }
]
```
