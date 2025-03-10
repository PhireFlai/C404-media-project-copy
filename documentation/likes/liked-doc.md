# Liked API Documentation

## URL: /api/authors/{AUTHOR_SERIAL}/liked

### Method: GET

### Description: Retrieve a list of likes by AUTHOR_SERIAL

### When the API endpoint should be used

- Use this endpoint to fetch a list of likes by a specific author.

### How the API endpoint should be used

- Send a GET request to `/api/authors/{AUTHOR_SERIAL}/liked`.

### Why the API endpoint should or should not be used

- Use this endpoint to get a comprehensive list of things liked by a specific author.

### Request

- **Method**: GET
- **URL**: `/api/authors/{AUTHOR_SERIAL}/liked`
- **Headers**: None required

### JSON Fields in Response

- **id**: `string` (UUID) - The unique identifier of the like.
  - **Example**: `1493e30c-b8a6-467b-b78e-cb76529a040f`
  - **Purpose**: Uniquely identifies the like.
- **user**: `object` - The user who liked the post or comment.
  - **id**: `string` (UUID) - The unique identifier of the user.
    - **Example**: `04f511c8-5cfe-4414-a125-e4a879188d38`
    - **Purpose**: Uniquely identifies the user.
  - **username**: `string` - The username of the user.
    - **Example**: `gregjohnson`
    - **Purpose**: The username of the user.
- **object**: `string` - The URL of the liked post or comment.
  - **Example**: `http://nodebbbb/api/authors/222/posts/249`
  - **Purpose**: Identifies the liked post or comment.

### Example

```bash
GET /api/authors/111/liked
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
    "object": "http://nodebbbb/api/authors/222/posts/249"
  }
]
```

## URL: /api/authors/{AUTHOR_SERIAL}/liked/{LIKE_SERIAL}

### Method: GET

### Description: Retrieve a single like by AUTHOR_SERIAL

### When the API endpoint should be used

- Use this endpoint to fetch a single like by a specific author.

### How the API endpoint should be used

- Send a GET request to `/api/authors/{AUTHOR_SERIAL}/liked/{LIKE_SERIAL}`.

### Why the API endpoint should or should not be used

- Use this endpoint to get details of a specific like by a specific author.

### Request

- **Method**: GET
- **URL**: `/api/authors/{AUTHOR_SERIAL}/liked/{LIKE_SERIAL}`
- **Headers**: None required

### JSON Fields in Response

- **id**: `string` (UUID) - The unique identifier of the like.
  - **Example**: `1493e30c-b8a6-467b-b78e-cb76529a040f`
  - **Purpose**: Uniquely identifies the like.
- **user**: `object` - The user who liked the post or comment.
  - **id**: `string` (UUID) - The unique identifier of the user.
    - **Example**: `04f511c8-5cfe-4414-a125-e4a879188d38`
    - **Purpose**: Uniquely identifies the user.
  - **username**: `string` - The username of the user.
    - **Example**: `gregjohnson`
    - **Purpose**: The username of the user.
- **object**: `string` - The URL of the liked post or comment.
  - **Example**: `http://nodebbbb/api/authors/222/posts/249`
  - **Purpose**: Identifies the liked post or comment.

### Example

```bash
GET /api/authors/111/liked/1493e30c-b8a6-467b-b78e-cb76529a040f
```

### Response

```bash
{
  "id": "1493e30c-b8a6-467b-b78e-cb76529a040f",
  "user": {
    "id": "04f511c8-5cfe-4414-a125-e4a879188d38",
    "username": "gregjohnson"
  },
  "object": "http://nodebbbb/api/authors/222/posts/249"
}
```

## URL: /api/authors/{AUTHOR_FQID}/liked

### Method: GET

### Description: Retrieve a list of likes by AUTHOR_FQID

### When the API endpoint should be used

- Use this endpoint to fetch a list of likes by a specific author.

### How the API endpoint should be used

- Send a GET request to `/api/authors/{AUTHOR_FQID}/liked`.

### Why the API endpoint should or should not be used

- Use this endpoint to get a comprehensive list of things liked by a specific author.

### Request

- **Method**: GET
- **URL**: `/api/authors/{AUTHOR_FQID}/liked`
- **Headers**: None required

### JSON Fields in Response

- **id**: `string` (UUID) - The unique identifier of the like.
  - **Example**: `1493e30c-b8a6-467b-b78e-cb76529a040f`
  - **Purpose**: Uniquely identifies the like.
- **user**: `object` - The user who liked the post or comment.
  - **id**: `string` (UUID) - The unique identifier of the user.
    - **Example**: `04f511c8-5cfe-4414-a125-e4a879188d38`
    - **Purpose**: Uniquely identifies the user.
  - **username**: `string` - The username of the user.
    - **Example**: `gregjohnson`
    - **Purpose**: The username of the user.
- **object**: `string` - The URL of the liked post or comment.
  - **Example**: `http://nodebbbb/api/authors/222/posts/249`
  - **Purpose**: Identifies the liked post or comment.

### Example

```bash
GET /api/authors/111/liked
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
    "object": "http://nodebbbb/api/authors/222/posts/249"
  }
]
```

## URL: /api/liked/{LIKE_FQID}

### Method: GET

### Description: Retrieve a single like by LIKE_FQID

### When the API endpoint should be used

- Use this endpoint to fetch a single like by its unique identifier.

### How the API endpoint should be used

- Send a GET request to `/api/liked/{LIKE_FQID}`.

### Why the API endpoint should or should not be used

- Use this endpoint to get details of a specific like.

### Request

- **Method**: GET
- **URL**: `/api/liked/{LIKE_FQID}`
- **Headers**: None required

### JSON Fields in Response

- **id**: `string` (UUID) - The unique identifier of the like.
  - **Example**: `1493e30c-b8a6-467b-b78e-cb76529a040f`
  - **Purpose**: Uniquely identifies the like.
- **user**: `object` - The user who liked the post or comment.
  - **id**: `string` (UUID) - The unique identifier of the user.
    - **Example**: `04f511c8-5cfe-4414-a125-e4a879188d38`
    - **Purpose**: Uniquely identifies the user.
  - **username**: `string` - The username of the user.
    - **Example**: `gregjohnson`
    - **Purpose**: The username of the user.
- **object**: `string` - The URL of the liked post or comment.
  - **Example**: `http://nodebbbb/api/authors/222/posts/249`
  - **Purpose**: Identifies the liked post or comment.

### Example

```bash
GET /api/liked/1493e30c-b8a6-467b-b78e-cb76529a040f
```

### Response

```bash
{
  "id": "1493e30c-b8a6-467b-b78e-cb76529a040f",
  "user": {
    "id": "04f511c8-5cfe-4414-a125-e4a879188d38",
    "username": "gregjohnson"
  },
  "object": "http://nodebbbb/api/authors/222/posts/249"
}
```
