import React from 'react';
import { useParams } from 'react-router-dom';
import { useGetFollowersQuery } from '../Api';
import { Link } from 'react-router-dom';
const FollowersList = () => {
    const { userId } = useParams();
    const { data: followers, isLoading, isError, error } = useGetFollowersQuery(userId);

    if (isLoading) return <div className="loader">Loading followers...</div>;
    if (isError) return <div>Error loading followers: {error.message}</div>;


    return (
        <div className="followers-container">
            <h2>Followers</h2>
            {followers?.length === 0 ? (
                <p>No followers yet</p>
            ) : (
                <ul className="followers-list">
                    {followers?.map((follower) => (
                        <li key={follower.id} className>
                            {follower.profilePicture &&
                                <img
                                    src={follower.profilePicture}
                                    alt={follower.username}
                                    className="follower-avatar"
                                />
                            }
                            <div className="follower-info">
                                <Link to={`/${follower.id}`} className="follower-name">
                                    {follower.username}
                                </Link>
                            </div>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default FollowersList;