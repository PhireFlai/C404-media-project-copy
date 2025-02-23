import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import { useGetUserProfileQuery, useUpdateUsernameMutation, useGetUserPostsQuery } from '../Api';
import ProfilePicUpload from '../components/ProfilePicUpload';
import UserPosts from '../components/UserPosts';
import { useSelector, useDispatch } from 'react-redux';
import { loginUser as loginUserAction } from '../UserContext/userActions';

const Profile = () => {
  const { userId } = useParams();
  const { data: user, isLoading, error } = useGetUserProfileQuery(userId);
  const { data: posts, isLoading: postsLoading, error: postsError } = useGetUserPostsQuery(userId);
  const curUser = useSelector((state) => state.user.user);
  const [isEditing, setIsEditing] = useState(false); // State for editing mode
  const [newUsername, setNewUsername] = useState(''); // State for new username
  const [updateUsername] = useUpdateUsernameMutation(); // Mutation for updating username
  const dispatch = useDispatch();

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
      {curUser && curUser.id === userId && (
        <div>
          <ProfilePicUpload userId={curUser.id} />

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

      {/* Display the user's posts */}
      <h2>{user.username}'s Posts</h2>
      {postsLoading ? (
        <div>Loading posts...</div>
      ) : postsError ? (
        <div>Error loading posts: {postsError.data?.error || 'Failed to fetch posts'}</div>
      ) : (
        <UserPosts posts={posts} />
      )}
    </div>
  );
};

export default Profile;