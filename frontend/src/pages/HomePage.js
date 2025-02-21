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
    <div>
      <h1>Recent Posts</h1>

      {/* Keep "Create a Post" message always visible */}
      <p style={{ color: "gray", fontSize: "18px", textAlign: "center" }}>
        <a href="/create">Create a Post</a>
      </p>

      {posts && posts.length > 0 ? (
        posts.map((post) => (
          <div
            key={post.id}
            style={{
              border: "1px solid #ddd",
              padding: "10px",
              marginBottom: "10px",
            }}
          >
            <h3>{post.title}</h3>
            {/* Enable rendering of images in markdown */}
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
              rehypePlugins={[rehypeRaw]}
            >
              {post.content}
            </ReactMarkdown>

            {/* Show Edit button only for post owner */}
            {user && user.id === post.author && (
              <button
                style={{
                  background: "blue",
                  color: "white",
                  marginRight: "5px",
                }}
              >
                Edit
              </button>
            )}

            <button onClick={() => handleCommentClick(post.id)}>
              {currentPostId === post.id ? "Close Comments" : " View Comments"}
            </button>
            <button
              onClick={() => handleDelete(post.id)}
              style={{ background: "red", color: "white" }}
            >
              Delete
            </button>

            {/* Display Comments */}
            {showCommentBox && currentPostId === post.id && (
              <div
                style={{
                  marginTop: "10px",
                  paddingLeft: "10px",
                  borderLeft: "2px solid #ddd",
                }}
              >
                <h4>Comments</h4>
                {comments?.length > 0 ? (
                    comments.map((comment) => (
                      <div key={comment.id} style={{ padding: "5px", borderBottom: "1px solid #eee" }}>
                        <p>{comment.content}</p>
                        <p><small>{comment.created_at}</small></p>
                      </div>
                    ))
                  ) : (
                    <p>No comments yet.</p>
                )}
                <input
                  type="text"
                  value={comment}
                  onChange={(e) => setComment(e.target.value)}
                  placeholder="Leave a comment..."
                />
                <button onClick={() => handleCommentSubmit(post.id, post.author)}>Submit</button>
              </div>
            )}
          </div>
        ))
      ) : (
        <p style={{ color: "gray", fontSize: "18px", textAlign: "center" }}>
          No posts yet.
        </p>
      )}
    </div>
  );
};

export default HomePage;
