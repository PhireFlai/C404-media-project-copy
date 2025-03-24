import React from "react";
import {
    useGetFollowRequestsQuery,
    useAcceptFollowRequestMutation
} from "../Api";
import { Link } from "react-router-dom";
import parseId from "../utils/parseId";
const FollowRequests = ({ userId, onFollowChange, allowChange }) => {
    const { data: requests, isLoading, isError, error, refetch: refetchRequests } = useGetFollowRequestsQuery(
        userId
    );
    const [acceptFollowRequest] = useAcceptFollowRequestMutation();
    
    if (isLoading) return <div className="loader">Loading requests...</div>;
    if (isError) return <div>Error loading requests: {error.message}</div>;

    const handleApproveOrReject = async (objectId, actorId, action) => {
        try {
            const response = await acceptFollowRequest({
                objectId: parseId(objectId),
                actorId: parseId(actorId),
                action: action,
            }).unwrap();
            console.log("Follow Request Sent:", response);
            // Call the parent's function to update
            refetchRequests();
            if (onFollowChange) onFollowChange();
        } catch (err) {
            console.error("Failed to accept or reject request:", err);
        }
    };

    return (
        <div className="request-container">
            <h2>Impending Requests</h2>
            {requests?.length === 0 ? (
                <p>No follow requests yet</p>
            ) : (
                <ul className="follower-request-list">
                    {requests.map((request) => (
                        <li key={parseId(request.actor.id)}>
                            <div className="requester-info">
                                <Link to={`/${parseId(request.actor.id)}`} className="requester-name">
                                    {request.actor.username}
                                </Link>
                                {allowChange && (
                                    <div>
                                        <button
                                            onClick={() =>
                                                handleApproveOrReject(parseId(request.object.id), parseId(request.actor.id), "accept")
                                            }
                                            className="approve-btn"
                                        >
                                            ✅
                                        </button>
                                        <button
                                            onClick={() =>
                                                handleApproveOrReject(parseId(request.object.id), parseId(request.actor.id), "reject")
                                            }
                                            className="reject-btn"
                                        >
                                            ❌
                                        </button>
                                    </div>
                                )}
                            </div>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default FollowRequests;
