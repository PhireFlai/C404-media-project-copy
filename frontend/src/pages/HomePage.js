import React from "react";
import { useGetPostsQuery } from "../Api";
import PostItem from "../components/PostItem";
import { useNavigate } from "react-router-dom";
import "./css/home.css";

const HomePage = () => {
  const { data: posts, refetch } = useGetPostsQuery();
  const navigate = useNavigate();

  const handleCreatePostClick = () => {
    navigate("/create");
  };

  return (
    <div className="recent-posts-container">
      <h1 className="recent-posts-title">Recent Posts</h1>

      <p className="create-post-link">
        <button className="create-posts-button" onClick={handleCreatePostClick}>
          Create a Post
        </button>
      </p>

      {posts && posts.length > 0 ? (
        posts.map((post) => (
          <PostItem key={post.id} post={post} refetchPosts={refetch} />
        ))
      ) : (
        <p className="no-posts-message">No posts yet.</p>
      )}
    </div>
  );
};

export default HomePage;
