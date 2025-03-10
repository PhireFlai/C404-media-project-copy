import React, {useEffect} from "react";
import { useGetUserFeedQuery} from "../Api"; // Import new feed query
import PostItem from "../components/PostItem";
import { useNavigate } from "react-router-dom";
import "./css/home.css";

const HomePage = () => {
  const { data: posts, refetch } = useGetUserFeedQuery(); // Fetch user feed
  // console.log(posts);  // Debugging output
  const navigate = useNavigate(); // Initialize navigation

  // Handle the click event for creating a new post
  const handleCreatePostClick = () => {
    navigate("/create"); // Navigate to the create post page
  };

  useEffect(() => {
    refetch();
  }, [refetch]);

  return (
    <div className="recent-posts-container">
      <h1 className="title">Your Feed</h1>

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
        <p className="text-muted">No posts in your feed yet.</p>
      )}
    </div>
  );
};

export default HomePage;