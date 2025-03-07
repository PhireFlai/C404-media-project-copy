import React from "react";
import { useParams } from "react-router-dom";
import { useGetFollowingQuery, useUnfollowUserMutation } from "../Api";
import { Link } from "react-router-dom";
import "./css/following.css";

const FollowingList = () => {
  const currentUser = JSON.parse(localStorage.getItem("user"));
  const { userId } = useParams();
  const {
    data: following,
    isLoading,
    isError,
    error,
    refetch,
  } = useGetFollowingQuery(userId);
  const [unfollowUser] = useUnfollowUserMutation();

  if (isLoading) return <div className="loader">Loading following...</div>;
  if (isError) return <div>Error loading following: {error.message}</div>;

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
      <h2>Following</h2>
      {following?.length === 0 ? (
        <p>Not following yet</p>
      ) : (
        <ul className="following-list">
          {following?.map((following) => (
            <li key={following.id} className>
              {following.profilePicture && (
                <img
                  src={following.profilePicture}
                  alt={following.username}
                  className="following-avatar"
                />
              )}
              <div className="following-info">
                <Link to={`/${following.id}`} className="following-name">
                  {following.username}
                </Link>
              </div>
              {currentUser.id === userId && (
                <button
                  onClick={() => handleUnfollow(following.id)}
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

export default FollowingList;
