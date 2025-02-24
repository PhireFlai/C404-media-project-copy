## Create a Post API

### Endpoint

**POST** `/api/authors/<uuid:userId>/posts/`

### When to Use This API

- Use this endpoint when an **authenticated user** wants to create a new post.
- Users can add text content and optionally include an image.
- Each post is linked to the **authenticated user**.
- Visibility options allow users to control who can see their posts.

---

### How to Use This API

1. **Authentication Required:**

   - The user must be logged in and provide an authentication token.
   - The `userId` in the URL must match the ID of the logged-in user.

2. **Request Body (JSON Format)**
   - Send a JSON object containing the post's `title`, `content`, `visibility`, and optionally an `image`.

---

### Why Use or Avoid This API?

**Use this API**

- When you need to create a new post under the logged-in user's profile.
- When you want to specify visibility settings (`public`, `friends-only`, `unlisted`).
- When you want to add an image to a post.

❌ **Do not use this API**

- If the user is not authenticated (an authentication token is required).
- If trying to create a post on behalf of another user.
- If attempting to delete or update an existing post (use the `PUT` or `DELETE` endpoints instead).

---

### Request Example

```http
POST /api/authors/550e8400-e29b-41d4-a716-446655440000/posts/
Authorization: Token abc123
Content-Type: application/json

{
  "title": "My First Post",
  "content": "This is the content of my first post!",
  "visibility": "public"
}
```

#### Example with an Image Upload (Multipart Form Data)

```http
POST /api/authors/550e8400-e29b-41d4-a716-446655440000/posts/
Authorization: Token abc123
Content-Type: multipart/form-data

{
  "title": "My First Post",
  "content": "This is the content of my first post!",
  "visibility": "public",
  "image": (file upload)
}
```

---

### Request Fields

| Field        | Type   | Example Value                             | Required | Description                                                          |
| ------------ | ------ | ----------------------------------------- | -------- | -------------------------------------------------------------------- |
| `title`      | string | `"My First Post"`                         | Yes      | Title of the post                                                    |
| `content`    | string | `"This is the content of my first post!"` | Yes      | The main text of the post                                            |
| `visibility` | string | `"public"`                                | Yes      | Controls who can see the post (`public`, `friends-only`, `unlisted`) |
| `image`      | file   | (File Upload)                             | No       | Optional image file attached to the post                             |

---

### Response Example (Success)

```json
{
  "id": "b3cdd37d-f7e7-4a69-8a9b-2dc5b0e510c3",
  "author":{
        "type":"author",
        "id":"http://nodeaaaa/api/authors/111",
        "page":"http://nodeaaaa/authors/greg",
        "host":"http://nodeaaaa/api/",
        "displayName":"Greg Johnson",
        "github": "http://github.com/gjohnson",
        "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
  },
  "title": "My First Post",
  "content": "This is the content of my first post!",
  "visibility": "public",
  "image": null,
  "created_at": "2025-02-24T12:00:00Z",
  "updated_at": "2025-02-24T12:00:00Z"
}
```

---

### Response Fields

| Field        | Type   | Example Value                                               | Description                                                  |
| ------------ | ------ | ----------------------------------------------------------- | ------------------------------------------------------------ |
| `id`         | string | `"b3cdd37d-f7e7-4a69-8a9b-2dc5b0e510c3"`                    | Unique identifier for the post                               |
| `author`     | string | `"550e8400-e29b-41d4-a716-446655440000"`                    | ID of the author who created the post                        |
| `title`      | string | `"My First Post"`                                           | Title of the post                                            |
| `content`    | string | `"This is the content of my first post!"`                   | The text content of the post                                 |
| `visibility` | string | `"public"`                                                  | Who can view the post (`public`, `friends-only`, `unlisted`) |
| `image`      | string | `null` or `"https://example.com/media/post_images/abc.jpg"` | URL to the uploaded image (if any)                           |
| `created_at` | string | `"2025-02-24T12:00:00Z"`                                    | Timestamp when the post was created                          |
| `updated_at` | string | `"2025-02-24T12:00:00Z"`                                    | Timestamp when the post was last updated                     |

---

### Response Example (Error)

**1. Unauthorized (Missing or Invalid Token)**

```json
{
  "detail": "Authentication credentials were not provided."
}
```

**2. Forbidden (Trying to Post for Another User)**

```json
{
  "error": "You must be logged in to create a post."
}
```

**3. Bad Request (Missing Required Fields)**

```json
{
  "title": ["This field is required."]
}
```

---

### Additional Notes

- The authentication token is provided to the user upon signing up or logging in.
- This API **does not support pagination**, as it is for creating a single post.
- The **author is automatically assigned** based on the authenticated user.
- If the post should be deleted, use the `DELETE /api/authors/<uuid:userId>/posts/<uuid:pk>/` endpoint.

---

## Post Detail API

### Endpoint

**GET, PUT, DELETE** `/api/authors/<uuid:userId>/posts/<uuid:pk>/`

### When to Use This API

- **GET:** Retrieve the details of a specific post.
- **PUT:** Update an existing post (only allowed for the post's author).
- **DELETE:** Delete a post (only allowed for the post's author).

---

### How to Use This API

1. **Authentication Required:**

   - The user must be logged in and provide an authentication token.
   - The `userId` in the URL must match the logged-in user's ID.

2. **Permissions:**
   - Only the post's author can update or delete the post.

---

### Why Use or Avoid This API?

**Use this API**

- To fetch details of a specific post.
- To edit or delete a post created by the logged-in user.

❌ **Do not use this API**

- If the user is not authenticated.
- If trying to edit or delete another user's post.

---

### Request Examples

#### Retrieve a Post (GET)

```http
GET /api/authors/550e8400-e29b-41d4-a716-446655440000/posts/b3cdd37d-f7e7-4a69-8a9b-2dc5b0e510c3/
Authorization: Token abc123
```

#### Update a Post (PUT)

```http
PUT /api/authors/550e8400-e29b-41d4-a716-446655440000/posts/b3cdd37d-f7e7-4a69-8a9b-2dc5b0e510c3/
Authorization: Token abc123
Content-Type: application/json

{
  "title": "Updated Post Title",
  "content": "Updated post content.",
  "visibility": "friends-only"
}
```

#### Delete a Post (DELETE)

```http
DELETE /api/authors/550e8400-e29b-41d4-a716-446655440000/posts/b3cdd37d-f7e7-4a69-8a9b-2dc5b0e510c3/
Authorization: Token abc123
```

---

### Request Fields for PUT (Update Post)

| Field        | Type   | Example Value             | Required | Description                 |
| ------------ | ------ | ------------------------- | -------- | --------------------------- |
| `title`      | string | `"Updated Post Title"`    | Yes      | Updated title of the post   |
| `content`    | string | `"Updated post content."` | Yes      | Updated content of the post |
| `visibility` | string | `"friends-only"`          | Yes      | Updated visibility setting  |

---

### Response Example (Success)

```json
{
  "id": "b3cdd37d-f7e7-4a69-8a9b-2dc5b0e510c3",
  "author":{
        "type":"author",
        "id":"http://nodeaaaa/api/authors/111",
        "page":"http://nodeaaaa/authors/greg",
        "host":"http://nodeaaaa/api/",
        "displayName":"Greg Johnson",
        "github": "http://github.com/gjohnson",
        "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
  },
  "title": "Updated Post Title",
  "content": "Updated post content.",
  "visibility": "friends-only",
  "image": null,
  "created_at": "2025-02-24T12:00:00Z",
  "updated_at": "2025-02-24T13:00:00Z"
}
```

---

### Response Fields

| Field        | Type   | Example Value                                               | Description                    |
| ------------ | ------ | ----------------------------------------------------------- | ------------------------------ |
| `id`         | string | `"b3cdd37d-f7e7-4a69-8a9b-2dc5b0e510c3"`                    | Unique identifier for the post |
| `author`     | object | `"550e8400-e29b-41d4-a716-446655440000"`                    | Author object                  |
| `title`      | string | `"Updated Post Title"`                                      | Title of the post              |
| `content`    | string | `"Updated post content."`                                   | Content of the post            |
| `visibility` | string | `"friends-only"`                                            | Who can view the post          |
| `image`      | string | `null` or `"https://example.com/media/post_images/abc.jpg"` | URL to the uploaded image      |
| `created_at` | string | `"2025-02-24T12:00:00Z"`                                    | Timestamp of creation          |
| `updated_at` | string | `"2025-02-24T13:00:00Z"`                                    | Timestamp of last update       |

---

### Response Example (Error)

**1. Unauthorized (Missing Token)**

```json
{
  "detail": "Authentication credentials were not provided."
}
```

**2. Forbidden (Editing/Deleting Another User's Post)**

```json
{
  "error": "You can only edit or delete your own posts."
}
```

**3. Not Found (Invalid Post ID)**

```json
{
  "error": "Post not found."
}
```

---

### Additional Notes

- **Only the post’s author can update or delete it.**
- **Authentication is required** for all operations.
- **Visibility changes affect who can see the post.**

---

### Conclusion

The **Post Detail API** allows users to manage their posts by retrieving, updating, or deleting them while maintaining security through authentication and authorization rules.

---

## Public Posts API

### Endpoint

**GET** `/api/public-posts/`

### When to Use This API

- Use this endpoint to retrieve a list of all publicly visible posts.
- No authentication is required; anyone can access public posts.
- Useful for displaying a global feed of posts that are not restricted by privacy settings.

---

### How to Use This API

1. **No Authentication Required:**

   - Any user (logged in or not) can access this endpoint.

2. **Pagination Support:**
   - If there are many posts, pagination may be implemented.

---

### Why Use or Avoid This API?

**Use this API**

- When you need to display a global feed of public posts.
- When you want to allow access to posts without requiring authentication.

❌ **Do not use this API**

- If you need posts with restricted visibility (use the user-specific post endpoint instead).
- If you want to create, edit, or delete posts (use the corresponding endpoints for those actions).

---

### Request Example

```http
GET /api/public-posts/
Content-Type: application/json
```

---

### Response Example (Success)

```json
[
  {
    "id": "b3cdd37d-f7e7-4a69-8a9b-2dc5b0e510c3",
    "author":{
        "type":"author",
        "id":"http://nodeaaaa/api/authors/111",
        "page":"http://nodeaaaa/authors/greg",
        "host":"http://nodeaaaa/api/",
        "displayName":"Greg Johnson",
        "github": "http://github.com/gjohnson",
        "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
  },
    "title": "A Public Post",
    "content": "This post is visible to everyone!",
    "visibility": "public",
    "image": null,
    "created_at": "2025-02-24T12:00:00Z",
    "updated_at": "2025-02-24T12:00:00Z"
  }
]
```

---

### Response Fields

| Field        | Type   | Example Value                                               | Description                        |
| ------------ | ------ | ----------------------------------------------------------- | ---------------------------------- |
| `id`         | string | `"b3cdd37d-f7e7-4a69-8a9b-2dc5b0e510c3"`                    | Unique identifier for the post     |
| `author`     | object | `"550e8400-e29b-41d4-a716-446655440000"`                    | Author object                      |
| `title`      | string | `"A Public Post"`                                           | Title of the post                  |
| `content`    | string | `"This post is visible to everyone!"`                       | Content of the post                |
| `visibility` | string | `"public"`                                                  | Visibility status of the post      |
| `image`      | string | `null` or `"https://example.com/media/post_images/abc.jpg"` | URL to the uploaded image (if any) |
| `created_at` | string | `"2025-02-24T12:00:00Z"`                                    | Timestamp of creation              |
| `updated_at` | string | `"2025-02-24T12:00:00Z"`                                    | Timestamp of last update           |

---

### Response Example (Error)

**1. No Public Posts Available**

```json
{
  "error": "No public posts found."
}
```

---

### Additional Notes

- **Public posts are available to everyone**, including non-authenticated users.
- **If no public posts exist**, an empty list or an error message may be returned.
- **Pagination may be used** if there are many posts (check response headers for pagination details).

---

### Conclusion

The **Public Posts API** provides open access to publicly available posts, making it useful for displaying a global feed of content without requiring authentication.
