import React, { useState } from "react";
import {
  useGetCommentsQuery,
  useCreateCommentMutation,
  usePostCommentMutation,
} from "../Api";
import { useSelector } from "react-redux";
import "./css/button.css";
import "./css/input.css";
import "./css/text.css";

const CommentSection = ({ postId, author }) => {
  const [comment, setComment] = useState(""); // State to manage the comment input
  const user = useSelector((state) => state.user.user); // Get the current user from the Redux store
  const { data: comments, refetch: refetchComments } = useGetCommentsQuery(
    { userId: user.id, postId },
    { skip: !postId }
  ); // Fetch comments using the custom hook
  const [postComment] = usePostCommentMutation(); // Mutation hook for posting a comment to the author's inbox

  // Handle comment submission
  const handleCommentSubmit = async () => {
    try {
      // Create the comment
      const response = await postComment({
        type: "Comment",
        receiver: user.id,
        pk: postId,
        content: comment,
      }).unwrap();
      console.log("Comment created:", response);

      refetchComments(); // Refetch comments after submission
    } catch (err) {
      console.error(err);
    }
    setComment(""); // Clear the comment input
  };

  return (
    <div className="comment-section">
      <p className="sub-title text-bold">Comments</p>
      {/* Render the list of comments if there are any, otherwise display a message */}
      {comments?.length > 0 ? (
        comments.map((comment) => (
          <div className="comment-item" key={comment.id}>
            <p>{comment.content}</p>
            <p className="text-muted">
              <small>{comment.created_at}</small>
            </p>
          </div>
        ))
      ) : (
        <p className="text-muted">No comments yet.</p>
      )}
      <div className="comment-form">
        <input
          type="text"
          value={comment}
          onChange={(e) => setComment(e.target.value)}
          placeholder="Leave a comment..."
        />
        <button className="button-primary" onClick={handleCommentSubmit}>
          Submit
        </button>
      </div>
    </div>
  );
};

export default CommentSection;
