import React from "react";
import { useGetPostsQuery } from "../Api";
import PostItem from "../components/PostItem";
import { useNavigate } from "react-router-dom";
import "./css/home.css";

const HomePage = () => {
  const { data: posts, refetch } = useGetPostsQuery(); // Fetch posts using the custom hook and destructure the data and refetch function
  const navigate = useNavigate(); // Initialize the navigate function for navigation

  // Handle the click event for creating a new post
  const handleCreatePostClick = () => {
    navigate("/create"); // Navigate to the create post page
  };

  return (
    <div className="recent-posts-container">
      <h1 className="title">Recent Posts</h1>

      <button
        className="button-primary create-post"
        onClick={handleCreatePostClick}
      >
        Create a Post
      </button>

      {/* Render the list of posts if there are any, otherwise display a message */}
      {posts && posts.length > 0 ? (
        posts.map((post) => (
          <PostItem key={post.id} post={post} refetchPosts={refetch} />
        ))
      ) : (
        <p className="text-muted">No posts yet.</p>
      )}
    </div>
  );
};

export default HomePage;
