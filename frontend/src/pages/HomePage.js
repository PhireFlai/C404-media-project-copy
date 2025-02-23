import React, { useState } from "react";
import {
  useGetPostsQuery,
  useDeletePostMutation,
  useCreateCommentMutation,
  useGetCommentsQuery,
  usePostCommentMutation,
} from "../Api";
import { useSelector } from "react-redux"; // Import Redux selector
import ReactMarkdown from "react-markdown";
import rehypeRaw from "rehype-raw"; // Allow rendering HTML inside Markdown
import remarkGfm from "remark-gfm"; // Support GitHub Flavored Markdown (tables, strikethroughs, etc.)
import "./css/home.css";

const HomePage = () => {
  const { data: posts, refetch } = useGetPostsQuery();
  const [deletePost] = useDeletePostMutation();
  const [createComment] = useCreateCommentMutation();
  const [postComment] = usePostCommentMutation();
  const [showCommentBox, setShowCommentBox] = useState(false);
  const [comment, setComment] = useState("");
  const [currentPostId, setCurrentPostId] = useState(null);
  const user = useSelector((state) => state.user.user); // Get logged-in user

  const handleDelete = async (postId) => {
    await deletePost(postId);
    refetch();
  };

  const { data: comments, refetch: refetchComments } = useGetCommentsQuery(
    currentPostId,
    { skip: !currentPostId }
  );

  const handleCommentClick = (postId) => {
    if (currentPostId === postId) {
      setShowCommentBox(false);
      setCurrentPostId(null);
    } else {
      setShowCommentBox(true);
      setCurrentPostId(postId);
    }
  };

  const handleCommentSubmit = async (pk, author) => {
    try {
      const createResponse = await createComment({
        pk,
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
    <div class="recent-posts-container">
      <h1 class="recent-posts-title">Recent Posts</h1>

      <p class="create-post-link">
        <a href="/create">Create a Post</a>
      </p>

      {posts && posts.length > 0 ? (
        posts.map((post) => (
          <div class="post-item" key={post.id}>
            <h3 class="post-title">{post.title}</h3>
            <p class="post-visibility">Visibility: {post.visibility}</p>

            <div class="post-content">
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                rehypePlugins={[rehypeRaw]}
              >
                {post.content}
              </ReactMarkdown>
            </div>

            <div class="post-actions">
              {user && user.id === post.author && (
                <button class="edit-button">Edit</button>
              )}
              <button onClick={() => handleCommentClick(post.id)}>
                {currentPostId === post.id
                  ? "Close Comments"
                  : " View Comments"}
              </button>
              <button
                onClick={() => handleDelete(post.id)}
                class="delete-button"
              >
                Delete
              </button>
            </div>

            {showCommentBox && currentPostId === post.id && (
              <div class="comment-section">
                <h4>Comments</h4>
                {comments?.length > 0 ? (
                  comments.map((comment) => (
                    <div class="comment-item" key={comment.id}>
                      <p>{comment.content}</p>
                      <p>
                        <small>{comment.created_at}</small>
                      </p>
                    </div>
                  ))
                ) : (
                  <p>No comments yet.</p>
                )}
                <div class="comment-form">
                  <input
                    type="text"
                    value={comment}
                    onChange={(e) => setComment(e.target.value)}
                    placeholder="Leave a comment..."
                  />
                  <button
                    onClick={() => handleCommentSubmit(post.id, post.author)}
                  >
                    Submit
                  </button>
                </div>
              </div>
            )}
          </div>
        ))
      ) : (
        <p class="no-posts-message">No posts yet.</p>
      )}
    </div>
  );
};

export default HomePage;
