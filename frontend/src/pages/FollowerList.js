import React from "react";
import { useParams } from "react-router-dom";
import { useGetFollowersQuery, useRemoveFollowerMutation } from "../Api";
import { Link } from "react-router-dom";
import FollowRequests from "../components/FollowRequests";
import "./css/followers.css";

const FollowersList = () => {
  const currentUser = JSON.parse(localStorage.getItem("user"));
  const { userId } = useParams();
  const {
    data: followers,
    isLoading,
    isError,
    error,
    refetch,
  } = useGetFollowersQuery(userId);
  const [removeFollower] = useRemoveFollowerMutation();

  if (isLoading) return <div className="loader">Loading followers...</div>;
  if (isError) return <div>Error loading followers: {error.message}</div>;

  const handleRemoveFollower = async (followerId) => {
    try {
      await removeFollower({
        followedId: currentUser.id,
        followerId: followerId,
      }).unwrap();
      refetch();
    } catch (err) {
      console.error("Failed to remove follower:", err);
    }
  };

  return (
    <div className="followers-container">
      <h2>Followers</h2>
      {followers?.length === 0 ? (
        <p>No followers yet</p>
      ) : (
        <ul className="followers-list">
          {followers?.map((follower) => (
            <li key={follower.id}>
              {follower.profilePicture && (
                <img
                  src={follower.profilePicture}
                  alt={follower.username}
                  className="follower-avatar"
                />
              )}
              <div className="follower-info">
                <Link to={`/${follower.id}`} className="follower-name">
                  {follower.username}
                </Link>
              </div>
              {currentUser && currentUser.id === userId && (
                <button
                  onClick={() => handleRemoveFollower(follower.id)}
                  className="remove-button"
                >
                  Remove
                </button>
              )}
            </li>
          ))}
        </ul>
      )}
      {currentUser && currentUser.id === userId && (
        <FollowRequests userId={userId} onFollowChange={refetch} allowChange={"valid"} />
      )}
    </div>
  );
};

export default FollowersList;
