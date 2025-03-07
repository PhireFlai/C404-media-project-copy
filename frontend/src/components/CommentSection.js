import React, { useState } from "react";
import { useGetCommentsQuery, useCreateCommentMutation } from "../Api";
import "./css/button.css";
import "./css/input.css";
import "./css/text.css";
import CommentItem from "./CommentItem";

const CommentSection = ({ postId, author }) => {
  const [comment, setComment] = useState(""); // State to manage the comment input
  const user = JSON.parse(localStorage.getItem("user")); // Get the current user from local storage
  const { data: comments, refetch: refetchComments } = useGetCommentsQuery(
    { userId: user.id, postId },
    { skip: !postId }
  ); // Fetch comments using the custom hook
  const [createComment] = useCreateCommentMutation(); // Mutation hook for creating a comment

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

  return (
    <div className="comment-section">
      <h4>Comments</h4>
      {/* Render the list of comments if there are any, otherwise display a message */}
      {comments?.length > 0 ? (
        comments.map((comment) => (
          <CommentItem
            comment={comment}
            postId={postId}
            userId={user.id}
            refetchComments={refetchComments}
          />
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
