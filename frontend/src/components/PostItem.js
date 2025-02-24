import React, { useState } from "react";
import { useDeletePostMutation, useEditPostMutation, useGetUserProfileQuery } from "../Api";
import ReactMarkdown from "react-markdown";
import rehypeRaw from "rehype-raw";
import remarkGfm from "remark-gfm";
import CommentSection from "./CommentSection";
import { useSelector } from "react-redux";
import "../pages/css/home.css";

const PostItem = ({ post, refetchPosts }) => {
  const [deletePost] = useDeletePostMutation();
  const [editPost] = useEditPostMutation();
  const [showCommentBox, setShowCommentBox] = useState(false);
  const [currentPostId, setCurrentPostId] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(post.title);
  const [editContent, setEditContent] = useState(post.content);
  const user = useSelector((state) => state.user.user); // Get the current user from the Redux store


  // Fetch the author's profile
  const { data: authorProfile } = useGetUserProfileQuery(post.author);

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
          <button className="save-button" onClick={handleSaveClick}>
            Save
          </button>
          <button className="delete-button" onClick={handleCancelClick}>
            Cancel
          </button>
        </div>
      ) : (
        <>
          <h3 className="post-title">{post.title}</h3>
          <p className="post-visibility">Visibility: {post.visibility}</p>
          <p className="post-author">Author: {authorProfile ? authorProfile.username : ""}</p>
          <div className="post-content">
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
              rehypePlugins={[rehypeRaw]}
            >
              {post.content}
            </ReactMarkdown>
          </div>
        </>
      )}

      <div className="post-actions">
        {user && user.id === post.author && !isEditing && (
          <>
            <button onClick={handleEditClick} className="edit-post-button">
              Edit
            </button>
            <button
              onClick={() => handleDelete(post.id)}
              className="delete-button"
            >
              Delete
            </button>
          </>
        )}
        <button onClick={() => handleCommentClick(post.id)}>
          {currentPostId === post.id ? "Close Comments" : "View Comments"}
        </button>
      </div>

      {showCommentBox && currentPostId === post.id && (
        <CommentSection postId={post.id} author={post.author} />
      )}
    </div>
  );
};

export default PostItem;
