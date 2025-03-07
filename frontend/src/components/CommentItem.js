import React, { useState, useEffect } from "react";
import { useAddCommentLikeMutation, useGetCommentLikesQuery } from "../Api";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faHeart as solidHeart } from "@fortawesome/free-solid-svg-icons";
import { faHeart as regularHeart } from "@fortawesome/free-regular-svg-icons";
import { Link } from "react-router-dom";
import "./css/button.css";
import "./css/input.css";
import "./css/text.css";
import "../pages/css/home.css";

const CommentItem = ({ comment, postId, userId, refetchComments }) => {
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
      if (!isLiked) {
        await addLike({
          userId: userId,
          postId: postId,
          commentId: commentId,
        }).unwrap();
        setIsLiked(true);
        refetchComments(); // Refetch comments after liking
      }
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
      <div>
        <p>{comment.content}</p>
        <p>
          <Link to={`/${comment.author?.id}/`}>
            <strong>{comment.author?.username || ""}</strong>
          </Link>
        </p>
        <p>
          <small>{comment.created_at}</small>
        </p>
      </div>
      <div>
        <button
          className="like-button"
          onClick={() => handleLikeToggle(comment.id)}
        >
          <FontAwesomeIcon icon={isLiked ? solidHeart : regularHeart} />
        </button>
        <div className="like-count">Likes: {comment.like_count}</div>
      </div>
    </div>
  );
};

export default CommentItem;
