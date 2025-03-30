import React, { useEffect } from "react";
import { useGetFriendsFeedQuery } from "../Api"; // Import API hook for friends feed
import PostItem from "../components/PostItem";
import { useNavigate } from "react-router-dom";
import "./css/home.css";

const FriendsFeedPage = () => {
  const { data: posts, refetch } = useGetFriendsFeedQuery(); // Fetch friends' posts
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
      <h1 className="title">Friends' Feed</h1>

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
        <p className="text-muted">No posts from your friends yet.</p>
      )}
    </div>
  );
};

export default FriendsFeedPage;