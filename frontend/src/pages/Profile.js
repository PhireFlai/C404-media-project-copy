import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import {
  useGetUserProfileQuery,
  useUpdateUsernameMutation,
  useGetUserPostsQuery,
} from "../Api";
import ProfilePicUpload from "../components/ProfilePicUpload";
import UserPosts from "../components/UserPosts";
import { useSelector, useDispatch } from "react-redux";
import { loginUser as loginUserAction } from "../UserContext/userActions";
import "./css/profile.css";

const Profile = () => {
  const { userId } = useParams();
  const { data: user, isLoading, error } = useGetUserProfileQuery(userId);
  const {
    data: posts,
    isLoading: postsLoading,
    error: postsError,
    refetch: refetchPosts,
  } = useGetUserPostsQuery(userId);
  const curUser = useSelector((state) => state.user.user);
  const [isEditing, setIsEditing] = useState(false); // State for editing mode
  const [newUsername, setNewUsername] = useState(""); // State for new username
  const [updateUsername] = useUpdateUsernameMutation(); // Mutation for updating username
  const dispatch = useDispatch();

  useEffect(() => {
    refetchPosts(); // Refetch posts every time the component is rendered
  }, [refetchPosts]);

  const handleEditClick = () => {
    setIsEditing(true);
    setNewUsername(user.username);
  };

  const handleSaveClick = async () => {
    try {
      // Call the updateUsername mutation
      await updateUsername({ userId, newUsername }).unwrap();
      setIsEditing(false); // Disable editing mode
      const updatedUser = { ...curUser, username: newUsername };
      dispatch(loginUserAction(updatedUser));

      window.location.reload(); // Refresh the page to reflect the changes
    } catch (err) {
      console.error("Failed to update username:", err);
    }
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error.data?.error || "Failed to fetch profile"}</div>;
  }

  return (
    <div className="profile-container">
      {/* Profile Header */}
      <div className="profile-header">
        {user.profile_picture && (
          <img
            src={`http://localhost:8000${user.profile_picture}`}
            alt={`${user.username}'s avatar`}
            className="profile-avatar"
          />
        )}
        <h1 className="profile-title">{user.username}</h1>
      </div>

      {/* Profile Stats */}
      <div className="profile-stats">
        <p>
          <strong>Followers:</strong> {user.followers.length}
        </p>
        <p>
          <strong>Friends:</strong> {user.friends.length}
        </p>
      </div>

      {/* Edit Profile Section (Only for Logged-in User) */}
      {curUser && curUser.id === userId && (
        <div className="edit-profile-section">
          <ProfilePicUpload userId={curUser.id} />

          {!isEditing ? (
            <button className="edit-button" onClick={handleEditClick}>
              Edit Username
            </button>
          ) : (
            <div className="username-edit-container">
              <input
                type="text"
                value={newUsername}
                onChange={(e) => setNewUsername(e.target.value)}
                placeholder="Enter new username"
                className="username-edit-input"
              />
              <button className="save-button" onClick={handleSaveClick}>
                Save
              </button>
              <button
                className="cancel-button"
                onClick={() => setIsEditing(false)}
              >
                Cancel
              </button>
            </div>
          )}
        </div>
      )}

      {/* User's Posts Section */}
      {postsLoading ? (
        <div className="loading-message">Loading posts...</div>
      ) : postsError ? (
        postsError.status === 401 ? (
          <></>
        ) : (
          <div className="error-message">
            Error loading posts:{" "}
            {postsError.data?.error || "Failed to fetch posts"} (Status code:{" "}
            {postsError.status})
          </div>
        )
      ) : (
        <>
          <h2 className="user-posts-title">{user.username}'s Posts</h2>
          <UserPosts posts={posts} />
        </>
      )}
    </div>
  );
};

export default Profile;
