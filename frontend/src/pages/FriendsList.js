import React from "react";
import { useParams } from "react-router-dom";
import { useGetFriendsQuery, useUnfollowUserMutation } from "../Api";
import { Link } from "react-router-dom";
import "./css/following.css";

const FriendsList = () => {
  const currentUser = JSON.parse(localStorage.getItem("user"));
  const { userId } = useParams();
  const {
    data: friends,
    isLoading,
    isError,
    error,
    refetch,
  } = useGetFriendsQuery(userId);
  const [unfollowUser] = useUnfollowUserMutation();

  if (isLoading) return <div className="loader">Loading friends...</div>;
  if (isError) return <div>Error loading friends: {error.message}</div>;

  const handleUnfollow = async (followedId) => {
    try {
      await unfollowUser({
        followerId: currentUser.id,
        followedId: followedId,
      }).unwrap();
      refetch(); // Refresh the list after successful removal
    } catch (err) {
      console.error("Failed to remove follower:", err);
    }
  };
  return (
    <div className="following-container">
      <h2>Friends</h2>
      {friends?.length === 0 ? (
        <p>No friends yet</p>
      ) : (
        <ul className="friends-list">
          {friends?.map((friends) => (
            <li key={friends.id}>
              {friends.profilePicture && (
                <img
                  src={friends.profilePicture}
                  alt={friends.username}
                  className="friends-avatar"
                />
              )}
              <div className="friends-info">
                <Link to={`/${friends.id}`} className="friends-name">
                  {friends.username}
                </Link>
              </div>
              {currentUser && currentUser.id === userId && (
                <button
                  onClick={() => handleUnfollow(friends.id)}
                  className="remove-button"
                >
                  Remove
                </button>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default FriendsList;
