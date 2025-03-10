**API Documentation: Post Author Profile Links**

### **Endpoint: Get a Single Post**

- **URL:** `GET /api/posts/{post_id}/`
- **Purpose:** Retrieve a post along with a link to the author's profile.
- **When to Use:** Use this endpoint to fetch a specific post and access the author's profile link.
- **Why Use It:** Helps users discover authors by clicking on the profile link in each post.
- **Should Not Be Used For:** Listing all posts by an author (use `/api/authors/{author_id}/posts/` instead).

### **Request Example:**

```http
GET /api/posts/4c6798a9-2753-46ce-aebb-5e2a51040c37/
```

### **Response Example:**

```json
{
  "id": "4c6798a9-2753-46ce-aebb-5e2a51040c37",
  "title": "My First Post",
  "content": "This is an example post.",
  "author": {
    "id": "77ff716b-ab0f-44bc-b390-7865dd2f49a1",
    "username": "alim",
    "profile_url": "http://localhost:8000/api/authors/77ff716b-ab0f-44bc-b390-7865dd2f49a1/"
  },
  "created_at": "2025-03-10T18:25:12.557Z",
  "updated_at": "2025-03-10T18:25:12.557Z"
}
```

### **Field Explanation:**

- `id`: A unique identifier for the post.
- `title`: The title of the post.
- `content`: The main content of the post.
- `author.id`: The unique identifier of the post's author.
- `author.username`: The author's username.
- `author.profile_url`: A direct link to the author's profile.
- `created_at`: The timestamp when the post was created.
- `updated_at`: The timestamp when the post was last updated.

### **Additional Notes:**

- The `profile_url` field provides direct access to the author's profile.
- If you need a list of an author's posts, use `/api/authors/{author_id}/posts/` instead.
