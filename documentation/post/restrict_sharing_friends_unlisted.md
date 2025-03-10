**API Documentation: Restricting Sharing of Friends-Only & Unlisted Content**

### **Endpoint: Get a Single Post**

- **URL:** `GET /api/posts/{post_id}/`
- **Purpose:** Retrieve a post while ensuring sharing restrictions based on visibility.
- **When to Use:** Use this endpoint to fetch a post while respecting its visibility settings.
- **Why Use It:** Prevents unauthorized users from accessing friends-only or unlisted content.
- **Should Not Be Used For:** Listing all posts by an author (use `/api/authors/{author_id}/posts/` instead).

### **Request Example:**

```http
GET /api/posts/4c6798a9-2753-46ce-aebb-5e2a51040c37/
```

### **Response Examples:**

#### **1. Public Post (Accessible by Anyone)**

```json
{
  "id": "4c6798a9-2753-46ce-aebb-5e2a51040c37",
  "title": "Public Post",
  "content": "This post is visible to everyone.",
  "visibility": "public",
  "share_url": "http://localhost:8000/api/posts/4c6798a9-2753-46ce-aebb-5e2a51040c37/"
}
```

#### **2. Friends-Only Post (Restricted to Friends)**

```json
{
  "detail": "You do not have permission to view this post."
}
```

**Response Code:** `403 Forbidden`

#### **3. Unlisted Post (Accessible by Followers, Not Strangers)**

```json
{
  "id": "e13d7c8b-9884-43b2-84e4-7b2d2130b4d8",
  "title": "Unlisted Post",
  "content": "This post is visible to followers only.",
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
- `detail`: A message indicating restricted access (`403 Forbidden` if applicable).

### **Access Rules:**

- **Public posts** are always sharable.
- **Friends-only posts** can only be accessed by mutual friends.
- **Unlisted posts** can be accessed by followers but not by strangers.
- **Unauthorized users get a `403 Forbidden` response.**

### **Additional Notes:**

- This API prevents users from sharing restricted posts with unauthorized viewers.
- If a user has access to an unlisted or friends-only post, they will see a `share_url`.
- If access is denied, they will receive a `403 Forbidden` response.
- To list all accessible posts, use `/api/authors/{userId}/posts/`.
