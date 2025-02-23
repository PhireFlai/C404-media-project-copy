import React from "react";
import { useGetPostsQuery } from "../Api";
import PostItem from "../components/PostItem";
import "./css/home.css";

const HomePage = () => {
  const { data: posts, refetch } = useGetPostsQuery();

  return (
    <div className="recent-posts-container">
      <h1 className="recent-posts-title">Recent Posts</h1>

      <p className="create-post-link">
        <a href="/create">Create a Post</a>
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