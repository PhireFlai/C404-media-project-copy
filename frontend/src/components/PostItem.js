import React, { useState } from "react";
import { useDeletePostMutation, useEditPostMutation } from "../Api";
import ReactMarkdown from "react-markdown";
import rehypeRaw from "rehype-raw";
import remarkGfm from "remark-gfm";
import CommentSection from "./CommentSection";
import "../pages/css/home.css";

const PostItem = ({ post, refetchPosts }) => {
  const [deletePost] = useDeletePostMutation();
  const [editPost] = useEditPostMutation();
  const [showCommentBox, setShowCommentBox] = useState(false);
  const [currentPostId, setCurrentPostId] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(post.title);
  const [editContent, setEditContent] = useState(post.content);
  const user = JSON.parse(localStorage.getItem('user')); // Get the current user from local storage

  console.log(post);

  // Handle post deletion
  const handleDelete = async (postId) => {
    await deletePost({ userId: user.id, postId });
    refetchPosts(); // Refetch posts after deletion
  };

  // Handle comment section toggle
  const handleCommentClick = (postId) => {
    if (currentPostId === postId) {
      setShowCommentBox(false);
      setCurrentPostId(null);
    } else {
      setShowCommentBox(true);
      setCurrentPostId(postId);
    }
  };

  // Handle edit button click
  const handleEditClick = () => {
    setIsEditing(true);
  };

  // Handle save button click
  const handleSaveClick = async () => {
    try {
      await editPost({
        userId: user.id,
        postId: post.id,
        updatedPost: {
          title: editTitle,
          content: editContent,
        },
      }).unwrap();
      refetchPosts(); // Refetch posts after editing
      setIsEditing(false);
    } catch (err) {
      console.error("Error updating post:", err);
    }
  };

  // Handle cancel button click
  const handleCancelClick = () => {
    setIsEditing(false);
    setEditTitle(post.title);
    setEditContent(post.content);
  };

  return (
    <div className="post-item" key={post.id}>
      {isEditing ? (
        <div>
          <input
            type="text"
            value={editTitle}
            onChange={(e) => setEditTitle(e.target.value)}
            className="post-title-input"
            placeholder="Edit title"
          />
          <br />
          <textarea
            value={editContent}
            onChange={(e) => setEditContent(e.target.value)}
            rows={5}
            className="post-title-textarea"
            placeholder="Edit content"
          />
          <br />
          <button className="button-success" onClick={handleSaveClick}>
            Save
          </button>
          <button className="button-danger" onClick={handleCancelClick}>
            Cancel
          </button>
        </div>
      ) : (
        <>
          <h3 className="sub-title">{post.title}</h3>
          <p className="text-muted">Visibility: {post.visibility}</p>
          <p>Author: {post.author.username}</p>
          <div>
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
              rehypePlugins={[rehypeRaw]}
            >
              {post.content}
            </ReactMarkdown>
          </div>
          <div className="post-image">
            {post.image && <img src={`${post.image}`} alt="Post" />}
          </div>
        </>
      )}
      <div className="post-actions">
        {user && user.id === post.author.id && !isEditing && (
          <>
            <button onClick={handleEditClick} className="button-secondary">
              Edit
            </button>
            <button
              onClick={() => handleDelete(post.id)}
              className="button-danger"
            >
              Delete
            </button>
          </>
        )}
        <button
          className="button-secondary"
          onClick={() => handleCommentClick(post.id)}
        >
          {currentPostId === post.id ? "Close Comments" : "View Comments"}
        </button>
      </div>

      {showCommentBox && currentPostId === post.id && (
        <CommentSection postId={post.id} author={post.author.id} />
      )}
    </div>
  );
};

export default PostItem;
