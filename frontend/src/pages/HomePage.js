import React, { useState } from "react";
import {
  useGetPostsQuery,
  useDeletePostMutation,
  useEditPostMutation, // Fixed import
  useCreateCommentMutation,
  useGetCommentsQuery,
  usePostCommentMutation,
} from "../Api";
import { useSelector } from "react-redux";
import ReactMarkdown from "react-markdown";
import rehypeRaw from "rehype-raw";
import remarkGfm from "remark-gfm";

const HomePage = () => {
  const { data: posts, refetch } = useGetPostsQuery();
  const [deletePost] = useDeletePostMutation();
  const [editPost] = useEditPostMutation();
  const [createComment] = useCreateCommentMutation();
  const [postComment] = usePostCommentMutation();
  const [showCommentBox, setShowCommentBox] = useState(false);
  const [comment, setComment] = useState("");
  const [currentPostId, setCurrentPostId] = useState(null);
  const [isEditing, setIsEditing] = useState(null);
  const [editTitle, setEditTitle] = useState(""); // Editable title
  const [editContent, setEditContent] = useState(""); // Editable content
  const user = useSelector((state) => state.user.user);

  const handleDelete = async (postId) => {
    await deletePost(postId);
    refetch();
  };

  const { data: comments, refetch: refetchComments } = useGetCommentsQuery(
    currentPostId,
    { skip: !currentPostId }
  );

  const handleCommentClick = (postId) => {
    if (currentPostId === postId) {
      setShowCommentBox(false);
      setCurrentPostId(null);
    } else {
      setShowCommentBox(true);
      setCurrentPostId(postId);
    }
  };

  const handleCommentSubmit = async (pk, author) => {
    try {
      const createResponse = await createComment({
        pk,
        commentData: { content: comment },
      }).unwrap();
      console.log("Comment created:", createResponse);
      console.log(author);
      const postResponse = await postComment({
        author,
        commentId: createResponse.id,
      }).unwrap();
      console.log("Comment posted to inbox:", postResponse);
      refetchComments();
    } catch (err) {
      console.error(err);
    }
    setComment("");
  };

  const handleEditClick = (post) => {
    setIsEditing(post.id);
    setEditTitle(post.title); // Set title for editing
    setEditContent(post.content); // Set content for editing
  };

  const handleEditSubmit = async (postId) => {
    try {
      const response = await editPost({
        postId,
        updatedPost: {
          title: editTitle, // Updated title
          content: editContent, // Updated content
        },
      }).unwrap();

      console.log("Updated Post Response:", response); // Debugging log

      refetch(); // Refresh posts to reflect changes
      setIsEditing(null); // Exit edit mode after saving
    } catch (err) {
      console.error("Error updating post:", err);
    }
  };

  return (
    <div>
      <h1>Recent Posts</h1>

      <p style={{ color: "gray", fontSize: "18px", textAlign: "center" }}>
        <a href="/create">Create a Post</a>
      </p>

      {posts && posts.length > 0 ? (
        posts.map((post) => (
          <div
            key={post.id}
            style={{
              border: "1px solid #ddd",
              padding: "10px",
              marginBottom: "10px",
            }}
          >
            {isEditing === post.id ? (
              <div>
                <input
                  type="text"
                  value={editTitle}
                  onChange={(e) => setEditTitle(e.target.value)}
                  style={{ width: "100%", marginBottom: "5px", padding: "5px" }}
                  placeholder="Edit title"
                />
                <textarea
                  value={editContent}
                  onChange={(e) => setEditContent(e.target.value)}
                  rows={5}
                  style={{ width: "100%" }}
                  placeholder="Edit content"
                />
                <button
                  onClick={() => handleEditSubmit(post.id)}
                  style={{
                    background: "green",
                    color: "white",
                    marginRight: "5px",
                  }}
                >
                  Save
                </button>
                <button
                  onClick={() => setIsEditing(null)}
                  style={{ background: "gray", color: "white" }}
                >
                  Cancel
                </button>
              </div>
            ) : (
              <>
                <h3>{post.title}</h3>
                <ReactMarkdown
                  remarkPlugins={[remarkGfm]}
                  rehypePlugins={[rehypeRaw]}
                >
                  {post.content}
                </ReactMarkdown>
              </>
            )}

            {user && user.id === post.author && (
              <button
                onClick={() => handleEditClick(post)}
                style={{
                  background: "blue",
                  color: "white",
                  marginRight: "5px",
                }}
              >
                Edit
              </button>
            )}

            <button onClick={() => handleCommentClick(post.id)}>
              {currentPostId === post.id ? "Close Comments" : " View Comments"}
            </button>
            <button
              onClick={() => handleDelete(post.id)}
              style={{ background: "red", color: "white" }}
            >
              Delete
            </button>

            {showCommentBox && currentPostId === post.id && (
              <div
                style={{
                  marginTop: "10px",
                  paddingLeft: "10px",
                  borderLeft: "2px solid #ddd",
                }}
              >
                <h4>Comments</h4>
                {comments?.length > 0 ? (
                  comments.map((comment) => (
                    <div
                      key={comment.id}
                      style={{ padding: "5px", borderBottom: "1px solid #eee" }}
                    >
                      <p>{comment.content}</p>
                      <p>
                        <small>{comment.created_at}</small>
                      </p>
                    </div>
                  ))
                ) : (
                  <p>No comments yet.</p>
                )}
                <input
                  type="text"
                  value={comment}
                  onChange={(e) => setComment(e.target.value)}
                  placeholder="Leave a comment..."
                />
                <button
                  onClick={() => handleCommentSubmit(post.id, post.author)}
                >
                  Submit
                </button>
              </div>
            )}
          </div>
        ))
      ) : (
        <p style={{ color: "gray", fontSize: "18px", textAlign: "center" }}>
          No posts yet.
        </p>
      )}
    </div>
  );
};

export default HomePage;
