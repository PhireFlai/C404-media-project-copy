import React, { useState } from "react";
import { skipToken } from "@reduxjs/toolkit/query";
import { useParams } from "react-router-dom";
import {
  useGetPostQuery,
  useGetCommentsQuery,
  useCreateCommentMutation,
} from "../Api"; // Fetch post & comments
import "./css/post.css"; // Add styling

const PostPage = () => {
  const { postId } = useParams(); // Get postId from URL
  const { data: post, error, isLoading } = useGetPostQuery(postId); // Fetch post
  const {
    data: comments,
    error: commentsError,
    isLoading: commentsLoading,
    refetch,
  } = useGetCommentsQuery(
    post?.author?.id ? { userId: post.author.id, postId } : skipToken
  );
  // Fetch comments
  const [createComment] = useCreateCommentMutation(); // Mutation for adding comments
  const [newComment, setNewComment] = useState(""); // Store new comment input

  const user = JSON.parse(localStorage.getItem("user")); // Get the logged-in user

  const handleCommentSubmit = async () => {
    if (!newComment.trim()) return;
    try {
      await createComment({
        userId: user.id,
        postId,
        commentData: { content: newComment },
      }).unwrap();
      setNewComment(""); // Clear input
      refetch(); // Refresh comments
    } catch (err) {
      console.error("Error adding comment:", err);
    }
  };

  if (isLoading) return <p>Loading post...</p>;
  if (error) return <p>Error loading post.</p>;
  if (!post) return <p>Post not found.</p>;

  return (
    <div className="post-container">
      <h2>{post.title}</h2>
      <p>
        <strong>Author:</strong> {post.author.username}
      </p>
      <p>{post.content}</p>
      {post.image && <img src={post.image} alt="Post" className="post-image" />}
      <p>
        <strong>Visibility:</strong> {post.visibility}
      </p>

      {/* View Comments Section */}
      <h3>Comments</h3>
      {commentsLoading && <p>Loading comments...</p>}
      {commentsError && <p>Error loading comments.</p>}
      {comments?.length > 0 ? (
        comments.map((comment) => (
          <div key={comment.id} className="comment-item">
            <p>
              <strong>{comment.author?.username}:</strong> {comment.content}
            </p>
          </div>
        ))
      ) : (
        <p>No comments yet.</p>
      )}

      {/* 🔹 Add Comment Section (Only for Logged-in Users) */}
      {user && (
        <div className="comment-form">
          <input
            type="text"
            value={newComment}
            onChange={(e) => setNewComment(e.target.value)}
            placeholder="Write a comment..."
          />
          <button onClick={handleCommentSubmit}>Submit</button>
        </div>
      )}
    </div>
  );
};

export default PostPage;
