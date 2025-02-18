import React, { useState } from "react";
import {
  useGetPostsQuery,
  useDeletePostMutation,
  useEditPostMutation,
} from "../Api";
import ReactMarkdown from "react-markdown";

const HomePage = () => {
  const { data: posts, refetch } = useGetPostsQuery();
  const [deletePost] = useDeletePostMutation();
  const [editPost] = useEditPostMutation();

  const [editingPost, setEditingPost] = useState(null);
  const [updatedTitle, setUpdatedTitle] = useState("");
  const [updatedContent, setUpdatedContent] = useState("");

  const handleDelete = async (postId) => {
    await deletePost(postId);
    refetch();
  };

  const handleEdit = (post) => {
    setEditingPost(post.id);
    setUpdatedTitle(post.title);
    setUpdatedContent(post.content);
  };

  const handleUpdate = async (postId) => {
    await editPost({
      postId,
      updatedPost: { title: updatedTitle, content: updatedContent },
    });
    setEditingPost(null);
    refetch();
  };

  return (
    <div>
      <h1>Recent Posts</h1>
      <p style={{ color: "gray", fontSize: "18px", textAlign: "center" }}>
        <a href="/create">Create a Post</a>
      </p>

      {!posts || posts.length === 0 ? (
        <p style={{ color: "gray", fontSize: "18px", textAlign: "center" }}>
          No posts yet.
        </p>
      ) : (
        posts.map((post) => (
          <div
            key={post.id}
            style={{
              border: "1px solid #ddd",
              padding: "10px",
              marginBottom: "10px",
            }}
          >
            {editingPost === post.id ? (
              <>
                <input
                  type="text"
                  value={updatedTitle}
                  onChange={(e) => setUpdatedTitle(e.target.value)}
                  style={{
                    display: "block",
                    width: "100%",
                    marginBottom: "10px",
                  }}
                />
                <textarea
                  value={updatedContent}
                  onChange={(e) => setUpdatedContent(e.target.value)}
                  style={{ display: "block", width: "100%", height: "100px" }}
                />
                <button
                  onClick={() => handleUpdate(post.id)}
                  style={{
                    background: "blue",
                    color: "white",
                    marginRight: "5px",
                  }}
                >
                  Save
                </button>
                <button
                  onClick={() => setEditingPost(null)}
                  style={{ background: "gray", color: "white" }}
                >
                  Cancel
                </button>
              </>
            ) : (
              <>
                <h3>{post.title}</h3>
                <ReactMarkdown>{post.content}</ReactMarkdown>
                <button
                  onClick={() => handleEdit(post)}
                  style={{
                    background: "green",
                    color: "white",
                    marginRight: "5px",
                  }}
                >
                  Edit
                </button>
                <button
                  onClick={() => handleDelete(post.id)}
                  style={{ background: "red", color: "white" }}
                >
                  Delete
                </button>
              </>
            )}
          </div>
        ))
      )}
    </div>
  );
};

export default HomePage;
