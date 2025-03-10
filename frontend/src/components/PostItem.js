import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import {
  useDeletePostMutation,
  useEditPostMutation,
  useAddLikeMutation,
  useGetLikesQuery,
} from "../Api";
import ReactMarkdown from "react-markdown";
import rehypeRaw from "rehype-raw";
import remarkGfm from "remark-gfm";
import CommentSection from "./CommentSection";
import "../pages/css/home.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faHeart as solidHeart } from "@fortawesome/free-solid-svg-icons";
import { faHeart as regularHeart } from "@fortawesome/free-regular-svg-icons";
import { format } from "date-fns"

const PostItem = ({ post, refetchPosts }) => {
  const [deletePost] = useDeletePostMutation();
  const [editPost] = useEditPostMutation();
  const [addLike] = useAddLikeMutation();
  const [showCommentBox, setShowCommentBox] = useState(false);
  const [currentPostId, setCurrentPostId] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(post.title);
  const [editContent, setEditContent] = useState(post.content);
  const user = JSON.parse(localStorage.getItem("user")); // Get the current user from local storage
  const [editImage, setEditImage] = useState(null);
  const [editVisibility, setEditVisibility] = useState(post.visibility);
  const [isLiked, setIsLiked] = useState(false);

  const {
    data: likes,
    error: likesError,
    isLoading: likesLoading,
    refetch: refetchLikes
  } = useGetLikesQuery(
    { userId: post.author.id, postId: post.id },
    { skip: !user }
  );

  useEffect(() => {
    if (!user || !post || !post.author) {
      // Ensures all required data is available
      return;
    }
    if (likesLoading) {
      // console.log("Loading likes...");
    } else if (likesError) {
      console.error("Error fetching likes:", likesError);
    } else if (likes && likes.length > 0) {
      likes.forEach((like) => {
        if (like.user.id === user.id) {
          setIsLiked(true);
        }
      });
    }
  }, [likes, likesError, likesLoading, user, post]);

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
          image: editImage,
          visibility: editVisibility,
        },
      }).unwrap();
      refetchPosts(); // Refetch posts after editing
      setIsEditing(false);
    } catch (err) {
      console.error("Error updating post:", err);
    }
  };

  const handleCopyLink = () => {
    const postLink = `${window.location.origin}/posts/${post.id}`;
    navigator.clipboard.writeText(postLink);
    alert("Post link copied to clipboard!");
  };

  // Handle cancel button click
  const handleCancelClick = () => {
    setIsEditing(false);
    setEditTitle(post.title);
    setEditContent(post.content);
  };

  // Handle like toggle
  const handleLikeToggle = async () => {
    try {
      if (!isLiked) {
        await addLike({ userId: user.id, postId: post.id }).unwrap();
        setIsLiked(true);
        refetchPosts(); // Refetch posts after liking
        refetchLikes();
      }
    } catch (err) {
      console.error("Error toggling like:", err);
    }
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

          <textarea
            value={editContent}
            onChange={(e) => setEditContent(e.target.value)}
            rows={5}
            className="post-title-textarea"
            placeholder="Edit content"
          />

          {/* Visibility Dropdown */}
          <label>Select a visibility option:</label>
          <select
            value={editVisibility}
            onChange={(e) => setEditVisibility(e.target.value)}
            className="post-visibility-select"
          >
            <option value="public">Public</option>
            <option value="friends-only">Friends Only</option>
            <option value="unlisted">Unlisted</option>
          </select>

          {/* image upload input */}
          <input
            type="file"
            accept="image/*"
            onChange={(e) => setEditImage(e.target.files[0])}
            className="post-image-input"
          />

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
          <p className="text-muted">
            Last updated: {format(new Date(post.updated_at), "PPPppp")}
          </p>

          <Link to={`/${post.author.id}`}>
            <p>Author: {post.author.username}</p>
          </Link>
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
        {/* Copy Link Button */}
        <button onClick={handleCopyLink} className="button-secondary">
          Copy Link
        </button>

        {user && (
          <button
            className="button-secondary"
            onClick={() => handleCommentClick(post.id)}
          >
            {currentPostId === post.id ? "Close Comments" : "View Comments"}
          </button>
        )}

        <div className="like-container">
          {user && (
            <button className="like-button" onClick={handleLikeToggle}>
              <FontAwesomeIcon icon={isLiked ? solidHeart : regularHeart} />
            </button>
          )}
          <div className="like-count">Likes: {post.like_count}</div>
        </div>
      </div>

      {user && showCommentBox && currentPostId === post.id && (
        <CommentSection postId={post.id} author={post.author.id} />
      )}
    </div>
  );
};

export default PostItem;
