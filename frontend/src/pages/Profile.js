import React from 'react';
import { useParams } from 'react-router-dom';
import { useGetUserProfileQuery } from '../Api';
import ProfilePicUpload from '../components/ProfilePicUpload';
import { useSelector } from 'react-redux';

const Profile = () => {
  const { username } = useParams();
  const { data: user, isLoading, error } = useGetUserProfileQuery(username);
  const curUser = useSelector((state) => state.user.user);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error.data?.error || 'Failed to fetch profile'}</div>;
  }

  return (
    <div>
      {/* Display the current user's username if available */}
      {/* {curUser && <h1>Current User: {curUser.username}</h1>} */}

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
        <ProfilePicUpload username={curUser.username} />
      )}
    </div>
  );
};

export default Profile;