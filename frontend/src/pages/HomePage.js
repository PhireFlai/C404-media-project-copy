// import React, { useState } from "react";
// import {
//   useGetPostsQuery,
//   useDeletePostMutation,
//   useEditPostMutation,
// } from "../Api";
// import ReactMarkdown from "react-markdown";

// const HomePage = () => {
//   const { data: posts, refetch } = useGetPostsQuery();
//   const [deletePost] = useDeletePostMutation();
//   const [editPost] = useEditPostMutation();

//   const [editingPost, setEditingPost] = useState(null);
//   const [updatedTitle, setUpdatedTitle] = useState("");
//   const [updatedContent, setUpdatedContent] = useState("");

//   const handleDelete = async (postId) => {
//     await deletePost(postId);
//     refetch();
//   };

//   const handleEdit = (post) => {
//     setEditingPost(post.id);
//     setUpdatedTitle(post.title);
//     setUpdatedContent(post.content);
//   };

//   const handleUpdate = async (postId) => {
//     await editPost({
//       postId,
//       updatedPost: { title: updatedTitle, content: updatedContent },
//     });
//     setEditingPost(null);
//     refetch();
//   };

//   return (
//     <div>
//       <h1>Recent Posts</h1>
//       <p style={{ color: "gray", fontSize: "18px", textAlign: "center" }}>
//         <a href="/create">Create a Post</a>
//       </p>

//       {!posts || posts.length === 0 ? (
//         <p style={{ color: "gray", fontSize: "18px", textAlign: "center" }}>
//           No posts yet.
//         </p>
//       ) : (
//         posts.map((post) => (
//           <div
//             key={post.id}
//             style={{
//               border: "1px solid #ddd",
//               padding: "10px",
//               marginBottom: "10px",
//             }}
//           >
//             {editingPost === post.id ? (
//               <>
//                 <input
//                   type="text"
//                   value={updatedTitle}
//                   onChange={(e) => setUpdatedTitle(e.target.value)}
//                   style={{
//                     display: "block",
//                     width: "100%",
//                     marginBottom: "10px",
//                   }}
//                 />
//                 <textarea
//                   value={updatedContent}
//                   onChange={(e) => setUpdatedContent(e.target.value)}
//                   style={{ display: "block", width: "100%", height: "100px" }}
//                 />
//                 <button
//                   onClick={() => handleUpdate(post.id)}
//                   style={{
//                     background: "blue",
//                     color: "white",
//                     marginRight: "5px",
//                   }}
//                 >
//                   Save
//                 </button>
//                 <button
//                   onClick={() => setEditingPost(null)}
//                   style={{ background: "gray", color: "white" }}
//                 >
//                   Cancel
//                 </button>
//               </>
//             ) : (
//               <>
//                 <h3>{post.title}</h3>
//                 <ReactMarkdown>{post.content}</ReactMarkdown>
//                 <button
//                   onClick={() => handleEdit(post)}
//                   style={{
//                     background: "green",
//                     color: "white",
//                     marginRight: "5px",
//                   }}
//                 >
//                   Edit
//                 </button>
//                 <button
//                   onClick={() => handleDelete(post.id)}
//                   style={{ background: "red", color: "white" }}
//                 >
//                   Delete
//                 </button>
//               </>
//             )}
//           </div>
//         ))
//       )}
//     </div>
//   );
// };

// export default HomePage;

import React, { useState } from "react";
import { useGetPostsQuery, useDeletePostMutation, useCreateCommentMutation, useGetCommentsQuery } from "../Api";
import ReactMarkdown from "react-markdown";
import rehypeRaw from "rehype-raw"; // Allow rendering HTML inside Markdown
import remarkGfm from "remark-gfm"; // Support GitHub Flavored Markdown (tables, strikethroughs, etc.)

const HomePage = () => {
  const { data: posts, refetch } = useGetPostsQuery();
  const [deletePost] = useDeletePostMutation();
  const [createComment] = useCreateCommentMutation();
  const [showCommentBox, setShowCommentBox] = useState(false);
  const [comment, setComment] = useState("");
  const [currentPostId, setCurrentPostId] = useState(null);

  const handleDelete = async (postId) => {
    await deletePost(postId);
    refetch();
  };

  const { data: comments, refetch: refetchComments } = useGetCommentsQuery(currentPostId, { skip: !currentPostId });

  const handleCommentClick = (postId) => {
    if (currentPostId === postId) {
      setShowCommentBox(false);
      setCurrentPostId(null); // Close the comment box
    } else {
      setShowCommentBox(true);
      setCurrentPostId(postId); // Open the comment box
    }
  };

  const handleCommentSubmit = async (pk) => {
    try {
      const response = await createComment({ pk, commentData: { content: comment } }).unwrap();
      console.log("Comment created:", response);
      refetchComments();
    } catch (err){
      console.error(err);
    }
    setComment("");
  };

  return (
    <div>
      <h1>Recent Posts</h1>
      {!posts || posts.length === 0 ? (
        <p style={{ color: "gray", fontSize: "18px", textAlign: "center" }}>
          No posts yet. <a href="/create">Create one!</a>
        </p>
      ) : (
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
            
            {/* Display Comments */}
            {showCommentBox && currentPostId === post.id && (
              <div style={{ marginTop: "10px", paddingLeft: "10px", borderLeft: "2px solid #ddd" }}>
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
                <button onClick={() => handleCommentSubmit(post.id)}>Submit</button>
              </div>
            )}
            <button
              onClick={() => handleCommentClick(post.id)}
              >
                {currentPostId === post.id ? "Close Comments" : " View Comments"}
            </button>
            <button
              onClick={() => handleDelete(post.id)}
              style={{ background: "red", color: "white" }}
            >
              Delete
            </button>
          </div>
        ))
      )}
    </div>
  );
};

export default HomePage;
