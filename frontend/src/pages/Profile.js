import React from 'react';
import { useParams } from 'react-router-dom';
import { useGetUserProfileQuery } from '../Api'; // Import the hook

const Profile = () => {
  const { username } = useParams(); // Extract the username from the URL
  const { data: user, isLoading, error } = useGetUserProfileQuery(username); // Fetch profile data

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error.data?.error || 'Failed to fetch profile'}</div>;
  }

  return (
    <div>
      <h1>{user.username}'s Profile</h1>
      {/* Display user github when implemented */}
      <p>github: {user.github}</p>
      <p>Followers: {user.followers.length}</p>
      <p>Friends: {user.friends.length}</p>
    </div>
  );
};

export default Profile;