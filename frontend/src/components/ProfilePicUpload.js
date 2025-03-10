import React from "react";
import { useUpdateProfilePictureMutation } from "../Api";
import "../pages/css/profile.css";

const ProfilePictureUpload = ({ userId, refetch }) => {
  const [updateProfilePicture, { isLoading, error }] =
    useUpdateProfilePictureMutation();

  const handleUploadClick = async (e) => {
    e.preventDefault();
    const fileInput = document.createElement("input");
    fileInput.type = "file";
    fileInput.accept = "image/*";
    fileInput.onchange = async (e) => {
      const file = e.target.files[0];
      if (file) {
        try {
          await updateProfilePicture({ userId, profilePicture: file }).unwrap();
          alert("Profile picture updated successfully!");
          refetch(); // Refetch the user data to reflect the changes
        } catch (err) {
          console.error("Failed to update profile picture:", err);
        }
      }
    };
    fileInput.click();
  };

  return (
    <form onSubmit={handleUploadClick}>
      <button className="button-secondary" type="submit" disabled={isLoading}>
        {isLoading ? "Uploading..." : "Upload Profile Picture"}
      </button>
      {error && (
        <p>Error: {error.data?.error || "Failed to upload profile picture"}</p>
      )}
    </form>
  );
};

export default ProfilePictureUpload;