import React, { useState, useEffect } from "react";
import { skipToken } from "@reduxjs/toolkit/query";
import { useParams, Link } from "react-router-dom";
import {
  useGetPostQuery,
  useGetCommentsQuery,
  useCreateCommentMutation,
  useDeletePostMutation,
  useEditPostMutation,
  useAddLikeMutation,
  useGetLikesQuery,
} from "../Api"; // Fetch post & comments
import ReactMarkdown from "react-markdown";
import rehypeRaw from "rehype-raw";
import remarkGfm from "remark-gfm";
import CommentItem from "../components/CommentItem"; // Import CommentItem component
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faHeart as solidHeart } from "@fortawesome/free-solid-svg-icons";
import { faHeart as regularHeart } from "@fortawesome/free-regular-svg-icons";
import { format } from "date-fns";
import "./css/post.css"; // Add styling
import parseId from "../utils/parseId";
const PostPage = () => {
  const { postId } = useParams(); // Get postId from URL
  const { data: post, error, isLoading, refetch: refetchPost } = useGetPostQuery(postId); // Fetch post
  const parsedPostId = post ? parseId(post.id) : null;
  const parsedAuthorId = post?.author ? parseId(post.author.id) : null;
  const {
    data: comments,
    error: commentsError,
    isLoading: commentsLoading,
    refetch: refetchComments,
  } = useGetCommentsQuery(
    post?.author?.id ? {
      userId: parsedAuthorId,
      postId: parsedPostId
    } : skipToken);


  const [createComment] = useCreateCommentMutation(); // Mutation for adding comments
  const [deletePost] = useDeletePostMutation();
  const [editPost] = useEditPostMutation();
  const [addLike] = useAddLikeMutation();
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState("");
  const [editContent, setEditContent] = useState("");
  const [editImage, setEditImage] = useState(null);
  const [editVisibility, setEditVisibility] = useState("");
  const [isLiked, setIsLiked] = useState(false);
  const [newComment, setNewComment] = useState(""); // Store new comment input

  const user = JSON.parse(localStorage.getItem("user")); // Get the logged-in user

  const {
    data: likes,
    error: likesError,
    isLoading: likesLoading,
    refetch: refetchLikes,
  } = useGetLikesQuery(
    { userId: parsedAuthorId, postId: parsedPostId },
    { skip: !user }
  );

  useEffect(() => {
    if (!user || !post || !post.author) {
      // Ensures all required data is available
      return;
    }
    if (likesLoading) {
      console.log("Loading likes...");
    } else if (likesError) {
      console.error("Error fetching likes:", likesError);
    } else if (likes && likes.length > 0) {
      likes.forEach((like) => {
        if (parseId(like.user.id) === user.id) {
          setIsLiked(true);
        }
      });
    }
  }, [likes, likesError, likesLoading, user, post]);

  const handleCommentSubmit = async () => {
    if (!newComment.trim()) return;
    try {
      await createComment({
        userId: user.id,
        postId,
        commentData: { content: newComment },
      }).unwrap();
      setNewComment(""); // Clear input
      refetchComments(); // Refresh comments
    } catch (err) {
      console.error("Error adding comment:", err);
    }
  };

  const handleDelete = async (postId) => {
    await deletePost({ userId: user.id, postId });
    refetchPost(); // Refetch posts after deletion
  };

  const handleEditClick = () => {
    setIsEditing(true);
    setEditTitle(post.title);
    setEditContent(post.content);
    setEditVisibility(post.visibility);
  };

  const handleSaveClick = async () => {
    try {
      await editPost({
        userId: user.id,
        postId: parseId(post.id),
        updatedPost: {
          title: editTitle,
          content: editContent,
          image: editImage,
          visibility: editVisibility,
        },
      }).unwrap();
      refetchPost(); // Refetch posts after editing
      setIsEditing(false);
    } catch (err) {
      console.error("Error updating post:", err);
    }
  };

  const handleCopyLink = () => {
    const postLink = `${window.location.origin}/posts/${parseId(post.id)}`;
    navigator.clipboard.writeText(postLink);
    alert("Post link copied to clipboard!");
  };

  const handleCancelClick = () => {
    setIsEditing(false);
    setEditTitle(post.title);
    setEditContent(post.content);
  };

  const handleLikeToggle = async () => {
    try {
      if (!isLiked) {
        await addLike({ userId: user.id, postId: parseId(post.id) }).unwrap();
        setIsLiked(true);
        refetchPost(); // Refetch posts after liking
        refetchLikes();
      }
    } catch (err) {
      console.error("Error toggling like:", err);
    }
  };

  if (isLoading) return <p>Loading post...</p>;
  if (error) return <p>This post is only shared with friends 😔</p>;
  if (!post) return <p>Post not found.</p>;

  return (
    <div className="post-container">
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
          <h2>{post.title}</h2>
          <Link to={`/${parseId(post.author.id)}`} className="post-author">
            <p>
              <strong>Author:</strong> {post.author.username}
            </p>
          </Link>
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            rehypePlugins={[rehypeRaw]}
          >
            {post.content}
          </ReactMarkdown>
          {post.image && <img src={post.image} alt="Post" className="post-image" />}
          <p>
            <strong>Visibility:</strong> {post.visibility}
          </p>
          <p className="text-muted">
            Last updated: {format(new Date(post.updated_at), "PPPppp")}
          </p>
        </>
      )}

      <div className="post-actions">
        {user && user.id === parseId(post.author.id) && !isEditing && (
          <>
            <button onClick={handleEditClick} className="button-secondary">
              Edit
            </button>
            <button
              onClick={() => handleDelete(parseId(post.id))}
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


        <div className="like-container">
          {user && (
            <button className="like-button" onClick={handleLikeToggle}>
              <FontAwesomeIcon icon={isLiked ? solidHeart : regularHeart} />
            </button>
          )}
          <div className="like-count">Likes: {post.like_count}</div>
        </div>
      </div>



      {/* View Comments Section */}
      <h3>Comments</h3>
      {commentsLoading && <p>Loading comments...</p>}
      {commentsError && <p>Error loading comments.</p>}
      {comments?.length > 0 ? (
        comments.map((comment) => (
          <CommentItem
            key={parseId(comment.id)}
            comment={comment}
            postId={parseId(post.id)}
            userId={user?.id}
            refetchComments={refetchComments}
          />
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