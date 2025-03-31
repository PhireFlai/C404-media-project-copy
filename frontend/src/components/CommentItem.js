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
import parseId from "../utils/parseId";
const CommentItem = ({ comment, postId, userId, refetchComments }) => {
  const [isLiked, setIsLiked] = useState(false);
  const [addLike] = useAddCommentLikeMutation();
  const {
    data: likes,
    error: likesError,
    isLoading: likesLoading,
    refetch: refetchLikes,
  } = useGetCommentLikesQuery(
    {
      userId: userId,
      postId: postId,
      commentId: comment.id,
    },
    { skip: !userId }
  );

  const handleLikeToggle = async (commentId) => {
    try {
      if (!isLiked) {
        await addLike({
          userId: parseId(userId),
          postId: parseId(postId),
          commentId: parseId(commentId),
        }).unwrap();
        setIsLiked(true);
        refetchComments(); // Refetch comments after liking
        refetchLikes();
      }
    } catch (err) {
      console.error("Error toggling like:", err);
    }
  };

  useEffect(() => {
    if (likesLoading) {
      // console.log("Loading likes...");
    } else if (likesError) {
      console.error("Error fetching likes:", likesError);
    } else if (likes && likes.length > 0) {
      likes.forEach((like) => {
        if (parseId(like.author?.id) === parseId(userId)) {
          setIsLiked(true);
        }
      });
    }
  }, [likes, likesError, likesLoading, userId]);

  return (
    <div className="comment-item" key={parseId(comment.id)}>
      <div>
        <p>{comment.comment}</p>
        <p>
          <Link to={`/${parseId(comment.author?.id)}/`}>
            <strong>{comment.author?.username || ""}</strong>
          </Link>
        </p>
        <p>
          <small>{comment.published}</small>
        </p>
      </div>
      <div>
        {userId && (
          <button
            className="like-button"
            onClick={() => handleLikeToggle(comment.id)}
          >
            <FontAwesomeIcon icon={isLiked ? solidHeart : regularHeart} />
          </button>
        )}
        <div className="like-count">
          Likes: {likes && likes.length > 0 ? likes.length : 0}
        </div>
      </div>
    </div>
  );
};

export default CommentItem;
