import React, {useEffect} from "react";
import { useGetPublicFeedQuery} from "../Api"; // Import new feed query
import PostItem from "../components/PostItem";
import { useNavigate } from "react-router-dom";
import "./css/home.css";
import parseId from "../utils/parseId";
const HomePage = () => {
  const { data: posts, refetch } = useGetPublicFeedQuery(); // Fetch user feed
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
        posts.map((post) => {
          // Parse the ID from the URL
          const parsedPost = {
            ...post,
            id: parseId(post.id)  // Transform the ID
          };

          return (
            <PostItem
              key={parsedPost.id}  // Use parsed UUID as the key
              post={parsedPost}    // Pass the modified post object
              refetchPosts={refetch}
            />
          );
        })
      ) : (
        <p className="text-muted">No posts in your feed yet.</p>
      )}
    </div>
  );
};

export default HomePage;