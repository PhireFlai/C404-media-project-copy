import React, { useState } from "react";
import { useParams, Link } from "react-router-dom";
import {
  useGetUserProfileQuery,
  useUpdateUsernameMutation,
} from "../Api";
import ProfilePicUpload from "../components/ProfilePicUpload";
import UserPosts from "../components/UserPosts";
import "./css/profile.css";

const Profile = () => {
  const { userId } = useParams();
  const { data: user, isLoading, error } = useGetUserProfileQuery(userId);
  const curUser = JSON.parse(localStorage.getItem("user")); // Get the current user from local storage
  const [isEditing, setIsEditing] = useState(false); // State for editing mode
  const [newUsername, setNewUsername] = useState(""); // State for new username
  const [updateUsername] = useUpdateUsernameMutation(); // Mutation for updating username



  const handleEditClick = () => {
    setIsEditing(true);
    setNewUsername(user.username);
  };

  const handleSaveClick = async () => {
    try {
      // Call the updateUsername mutation
      await updateUsername({ userId, newUsername }).unwrap();
      setIsEditing(false); // Disable editing mode
      const updatedUser = { id: curUser.id, username: newUsername };

      localStorage.setItem('user', JSON.stringify(updatedUser));

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
          <Link to={`/${userId}/followers`}><strong>Followers:</strong> </Link>{user.followers.length}
        </p>
        <p>
          <Link to={`/${userId}/following`}><strong>Following:</strong> </Link> {user.following.length}
        </p>
      </div>

      {/* Edit Profile Section (Only for Logged-in User) */}
      {curUser && curUser.id === userId && (
        <div className="edit-profile-section">
          <ProfilePicUpload userId={curUser.id} />

          {!isEditing ? (
            <button className="button-secondary" onClick={handleEditClick}>
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
              <button className="button-success" onClick={handleSaveClick}>
                Save
              </button>
              <button
                className="button-danger"
                onClick={() => setIsEditing(false)}
              >
                Cancel
              </button>
            </div>
          )}
        </div>
      )}

      {/* User's Posts Section */}

      <h2 className="user-posts-title">{user.username}'s Posts</h2>
      <UserPosts userId={userId} />

    </div>
  );
};

export default Profile;
