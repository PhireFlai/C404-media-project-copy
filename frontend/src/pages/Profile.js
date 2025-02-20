import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import { useGetUserProfileQuery, useUpdateUsernameMutation } from '../Api';
import ProfilePicUpload from '../components/ProfilePicUpload';
import { useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';

const Profile = () => {
  const { username } = useParams();
  const { data: user, isLoading, error } = useGetUserProfileQuery(username);
  const curUser = useSelector((state) => state.user.user);
  const [isEditing, setIsEditing] = useState(false); // State for editing mode
  const [newUsername, setNewUsername] = useState(''); // State for new username
  const [updateUsername] = useUpdateUsernameMutation(); // Mutation for updating username

  const navigate = useNavigate();


  const handleEditClick = () => {
    setIsEditing(true); // Enable editing mode
    setNewUsername(user.username); // Pre-fill the input with the current username
  };

  const handleSaveClick = async () => {
    try {
      // Call the updateUsername mutation
      await updateUsername({ username, newUsername }).unwrap();
      setIsEditing(false); // Disable editing mode
      navigate(`/${newUsername}`); // Redirect to the new profile URL
    } catch (err) {
      console.error('Failed to update username:', err);
    }
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error.data?.error || 'Failed to fetch profile'}</div>;
  }

  return (
    <div>
      <h1>{user.username}'s Profile</h1>
      <p>Followers: {user.followers.length}</p>
      <p>Friends: {user.friends.length}</p>

      {/* Display the profile picture if available */}
      {user.profile_picture && (
        <img
          src={`http://localhost:8000${user.profile_picture}`}
          alt={`${user.username}'s avatar`}
          style={{ width: '100px', height: '100px', borderRadius: '80%' }}
        />
      )}

      {/* Conditionally render the ProfilePicUpload component */}
      {curUser && curUser.username === user.username && (
        <div>
          <ProfilePicUpload username={curUser.username} />

          {/* Button to toggle editing mode */}
          {!isEditing ? (
            <button onClick={handleEditClick}>Edit Username</button>
          ) : (
            <div>
              <input
                type="text"
                value={newUsername}
                onChange={(e) => setNewUsername(e.target.value)}
                placeholder="Enter new username"
              />
              <button onClick={handleSaveClick}>Save</button>
              <button onClick={() => setIsEditing(false)}>Cancel</button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Profile;