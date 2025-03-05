import React from 'react';
import { useParams } from 'react-router-dom';
import { useGetFollowingQuery } from '../Api';
import { Link } from 'react-router-dom';
const FollowingList = () => {
    const { userId } = useParams();
    const { data: following, isLoading, isError, error } = useGetFollowingQuery(userId);

    if (isLoading) return <div className="loader">Loading following...</div>;
    if (isError) return <div>Error loading following: {error.message}</div>;


    return (
        <div className="following-container">
            <h2>Following</h2>
            {following?.length === 0 ? (
                <p>Not following yet</p>
            ) : (
                <ul className="following-list">
                    {following?.map((following) => (
                        <li key={following.id} className>
                            {following.profilePicture &&
                                <img
                                    src={following.profilePicture}
                                    alt={following.username}
                                    className="following-avatar"
                                />
                            }
                            <div className="following-info">
                                <Link to={`/${following.id}`} className="following-name">
                                    {following.username}
                                </Link>
                            </div>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default FollowingList;