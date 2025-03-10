**API Documentation: Generating Shareable Links for Posts**

### **Endpoint: Get a Single Post with Shareable Link**

- **URL:** `GET /api/posts/{post_id}/`
- **Purpose:** Retrieve a post and generate a shareable link based on its visibility settings.
- **When to Use:** Use this endpoint to fetch a post and obtain a valid shareable link.
- **Why Use It:** Enables users to share posts while respecting visibility rules.
- **Should Not Be Used For:** Fetching all posts by an author (use `/api/authors/{author_id}/posts/`).

### **Request Example:**

```http
GET /api/posts/4c6798a9-2753-46ce-aebb-5e2a51040c37/
```

### **Response Examples:**

#### **1. Public Post (Sharable by Anyone)**

```json
{
  "id": "4c6798a9-2753-46ce-aebb-5e2a51040c37",
  "title": "Public Post",
  "content": "This post is visible to everyone.",
  "visibility": "public",
  "share_url": "http://localhost:8000/api/posts/4c6798a9-2753-46ce-aebb-5e2a51040c37/"
}
```

#### **2. Friends-Only Post (Sharable Only Among Friends)**

```json
{
  "id": "a29d4c8b-12df-4e7e-85b1-7d9f87c5f29e",
  "title": "Friends-Only Post",
  "content": "This post can only be shared among friends.",
  "visibility": "friends",
  "share_url": "http://localhost:8000/api/posts/a29d4c8b-12df-4e7e-85b1-7d9f87c5f29e/"
}
```

#### **3. Unlisted Post (Sharable Only with Followers)**

```json
{
  "id": "e13d7c8b-9884-43b2-84e4-7b2d2130b4d8",
  "title": "Unlisted Post",
  "content": "This post is visible only to followers.",
  "visibility": "unlisted",
  "share_url": "http://localhost:8000/api/posts/e13d7c8b-9884-43b2-84e4-7b2d2130b4d8/"
}
```

### **Field Explanation:**

- `id`: A unique identifier for the post.
- `title`: The title of the post.
- `content`: The main content of the post.
- `visibility`: Defines who can see the post (`public`, `friends`, or `unlisted`).
- `share_url`: A direct link to the post (only present if the user has access).

### **Access Rules for Shareable Links:**

- **Public posts** can be shared with anyone.
- **Friends-only posts** can only be shared with mutual friends.
- **Unlisted posts** can only be shared with followers, not strangers.
- **Unauthorized users will not see a `share_url`.**

### **Additional Notes:**

- The `share_url` field is only included in the response if the user has permission to access the post.
- If a user tries to access a restricted post, they will receive a `403 Forbidden` response.
- To list all accessible posts, use `/api/authors/{userId}/posts/`.
