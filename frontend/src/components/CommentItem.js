import React, { useState, useEffect } from "react";
import { useAddCommentLikeMutation, useGetCommentLikesQuery } from "../Api";
import "./css/button.css";
import "./css/input.css";
import "./css/text.css";
import { Link } from "react-router-dom";

const CommentItem = ({ key, comment, postId, userId, refetchComments }) => {
  const [isLiked, setIsLiked] = useState(false);
  const [addLike] = useAddCommentLikeMutation();
  const {
    data: likes,
    error: likesError,
    isLoading: likesLoading,
  } = useGetCommentLikesQuery({
    userId: userId,
    postId: postId,
    commentId: comment.id,
  });

  const handleLikeToggle = async (commentId) => {
    try {
      if (isLiked) {
        // await removeLike({ userId: user.id, postId: post.id }).unwrap();
        console.log("unlike");
      } else {
        console.log("CommentId: " + commentId);
        await addLike({
          userId: userId,
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

  useEffect(() => {
    if (likesLoading) {
      console.log("Loading likes...");
    } else if (likesError) {
      console.error("Error fetching likes:", likesError);
    } else if (likes && likes.length > 0) {
      likes.forEach((like) => {
        if (like.user.id === userId) {
          setIsLiked(true);
        }
      });
    }
  }, [likes, likesError, likesLoading, userId]);

  return (
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
  );
};

export default CommentItem;
