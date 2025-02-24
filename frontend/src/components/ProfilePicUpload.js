import React, { useState } from "react";
import { useUpdateProfilePictureMutation } from "../Api";
import "../pages/css/profile.css";

const ProfilePictureUpload = ({ userId }) => {
  const [profilePicture, setProfilePicture] = useState(null);
  const [updateProfilePicture, { isLoading, error }] =
    useUpdateProfilePictureMutation();

  const handleFileChange = (e) => {
    setProfilePicture(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (profilePicture) {
      try {
        await updateProfilePicture({ userId, profilePicture }).unwrap();
        alert("Profile picture updated successfully!");
        window.location.reload(); // Refresh the page to reflect the changes
      } catch (err) {
        console.error("Failed to update profile picture:", err);
      }
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="file" accept="image/*" onChange={handleFileChange} />
      <button className="edit-button" type="submit" disabled={isLoading}>
        {isLoading ? "Uploading..." : "Upload Profile Picture"}
      </button>
      {error && (
        <p>Error: {error.data?.error || "Failed to upload profile picture"}</p>
      )}
    </form>
  );
};

export default ProfilePictureUpload;
