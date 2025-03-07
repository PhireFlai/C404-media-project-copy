import React from "react";
import { useGetFriendsPostsQuery } from "../Api"; // Custom hook for friends-only posts
import PostItem from "../components/PostItem";
import { useNavigate } from "react-router-dom";
import "./css/home.css";

const FriendsOnlyPosts = () => {
  const curUser = JSON.parse(localStorage.getItem("user")); // Get the current user from local storage
  const { data: posts, refetch } = useGetFriendsPostsQuery(curUser.id); // Fetch friends-only posts
  const navigate = useNavigate();

  const handleCreatePostClick = () => {
    navigate("/create"); // Navigate to the create post page
  };

  return (
    <div className="recent-posts-container">
      <h1 className="title">Friends Only Posts</h1>
      <button className="button-primary" onClick={handleCreatePostClick}>
        Create a Post
      </button>
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

export default FriendsOnlyPosts;
