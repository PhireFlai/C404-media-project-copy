import React, { useState, useEffect } from "react";
import {
  useGetCommentsQuery,
  useCreateCommentMutation,
  useAddCommentLikeMutation,
  useGetCommentLikesQuery,
} from "../Api";
import "./css/button.css";
import "./css/input.css";
import "./css/text.css";
import { Link } from "react-router-dom";

const CommentSection = ({ postId, author }) => {
  const [comment, setComment] = useState(""); // State to manage the comment input
  const user = JSON.parse(localStorage.getItem("user")); // Get the current user from local storage
  const { data: comments, refetch: refetchComments } = useGetCommentsQuery(
    { userId: user.id, postId },
    { skip: !postId }
  ); // Fetch comments using the custom hook
  const [createComment] = useCreateCommentMutation(); // Mutation hook for creating a comment
  const [isLiked, setIsLiked] = useState(false);
  const [addLike] = useAddCommentLikeMutation();
  // const {
  //   data: likes,
  //   error: likesError,
  //   isLoading: likesLoading,
  // } = useGetCommentLikesQuery({
  //   userId: user.id,
  //   postId: postId,
  //   commentId: comment.id,
  // });

  // useEffect(() => {
  //   console.log(comment.like_count);
  //   if (likesLoading) {
  //     console.log("Loading likes...");
  //   } else if (likesError) {
  //     console.error("Error fetching likes:", likesError);
  //   } else if (likes && likes.length > 0) {
  //     console.log("Likes:", likes);
  //     // Check if the post is already liked by the user
  //     console.log("Liked comment, " + comment.content);
  //     setIsLiked(true);
  //   }
  // }, [likes, likesError, likesLoading, user.id]);

  // Handle comment submission
  const handleCommentSubmit = async () => {
    try {
      // Create the comment
      const createResponse = await createComment({
        userId: user.id,
        postId,
        commentData: { content: comment },
      }).unwrap();
      console.log("Comment created:", createResponse);

      refetchComments(); // Refetch comments after submission
    } catch (err) {
      console.error(err);
    }
    setComment(""); // Clear the comment input
  };

  // Handle like toggle
  const handleLikeToggle = async (commentId) => {
    try {
      if (isLiked) {
        // await removeLike({ userId: user.id, postId: post.id }).unwrap();
        console.log("unlike");
      } else {
        console.log("CommentId: " + commentId);
        await addLike({
          userId: user.id,
          postId: postId,
          commentId: commentId,
        }).unwrap();
      }
      setIsLiked(!isLiked);
      refetchComments(); // Refetch posts after liking/unliking
    } catch (err) {
      console.error("Error toggling like:", err);
    }
  };

  return (
    <div className="comment-section">
      <h4>Comments</h4>
      {/* Render the list of comments if there are any, otherwise display a message */}
      {comments?.length > 0 ? (
        comments.map((comment) => (
          <div className="comment-item" key={comment.id}>
            <p>
              <Link to={`/${comment.author?.id}/`}>
                <strong>{comment.author?.username || ""}</strong>
              </Link>
            </p>
            <p>{comment.content}</p>
            <p>
              <small>{comment.created_at}</small>
            </p>
            <label>
              <input
                type="checkbox"
                checked={isLiked}
                onChange={() => handleLikeToggle(comment.id)}
              />
              Likes: {comment.like_count}
            </label>
          </div>
        ))
      ) : (
        <p>No comments yet.</p>
      )}
      <div className="comment-form">
        <input
          type="text"
          value={comment}
          onChange={(e) => setComment(e.target.value)}
          placeholder="Leave a comment..."
        />
        <button onClick={handleCommentSubmit}>Submit</button>
      </div>
    </div>
  );
};

export default CommentSection;
