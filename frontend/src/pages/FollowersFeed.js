import React, { useEffect } from "react";
import { useGetFollowersFeedQuery } from "../Api"; // Import API hook for followers feed
import PostItem from "../components/PostItem";
import { useNavigate } from "react-router-dom";
import "./css/home.css";

const FollowersFeedPage = () => {
  const { data: posts, refetch } = useGetFollowersFeedQuery(); // Fetch followers' posts
  const navigate = useNavigate(); // Initialize navigation

  // Handle navigation to create post page
  const handleCreatePostClick = () => {
    navigate("/create");
  };

  useEffect(() => {
    refetch();
  }, [refetch]);

  return (
    <div className="recent-posts-container">
      <h1 className="title">Followers' Feed</h1>

      <button
        className="button-primary create-post"
        onClick={handleCreatePostClick}
      >
        Create a Post
      </button>

      {/* Render posts if available, otherwise display a message */}
      {posts && posts.length > 0 ? (
        posts.map((post) => (
          <PostItem key={post.id} post={post} refetchPosts={refetch} />
        ))
      ) : (
        <p className="text-muted">No posts from your followers yet.</p>
      )}
    </div>
  );
};

export default FollowersFeedPage;