import React, { useState } from "react";
import { useGetCommentsQuery, useCreateCommentMutation, usePostCommentMutation } from "../Api";
import { useSelector } from "react-redux";

const CommentSection = ({ postId, author }) => {
  const [comment, setComment] = useState("");
  const user = useSelector((state) => state.user.user);
  const { data: comments, refetch: refetchComments } = useGetCommentsQuery({ userId: user.id, postId }, { skip: !postId });
  const [createComment] = useCreateCommentMutation();
  const [postComment] = usePostCommentMutation();

  const handleCommentSubmit = async () => {
    try {
      const createResponse = await createComment({
        userId: user.id,
        postId,
        commentData: { content: comment },
      }).unwrap();
      console.log("Comment created:", createResponse);
      console.log(author);
      const postResponse = await postComment({
        author,
        commentId: createResponse.id,
      }).unwrap();
      console.log("Comment posted to inbox:", postResponse);
      refetchComments();
    } catch (err) {
      console.error(err);
    }
    setComment("");
  };

  return (
    <div className="comment-section">
      <h4>Comments</h4>
      {comments?.length > 0 ? (
        comments.map((comment) => (
          <div className="comment-item" key={comment.id}>
            <p>{comment.content}</p>
            <p>
              <small>{comment.created_at}</small>
            </p>
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