import React from "react"
import {
    useGetFollowRequestsQuery,
    useAcceptFollowRequestMutation
} from "../Api";
import { Link } from "react-router-dom"

const FollowRequests = () => {
    const user = JSON.parse(localStorage.getItem("user")); // Get the current user from local storage
    console.log(user.id);
    const { data: requests, isLoading, isError, error, refetch } = useGetFollowRequestsQuery(user.id);
    const [acceptFollowRequest] = useAcceptFollowRequestMutation();

    if (isLoading) return <div className="loader">Loading requests...</div>;
    if (isError) return <div>Error loading requests: {error.message}</div>;

    const handleApproveOrReject = async (objectId, actorId, action) => {
        try{
            await acceptFollowRequest({
            objectId: objectId,
            actorId: actorId,
            action: action,
        }).unwrap();
        refetch();
        } catch (err){
            console.error("Failed to accept or reject request:", err);
        }
    }

    return (
        <div className="request-container">
            <h2>Impending Requests</h2>
            {requests?.length === 0 ? (
                <p>No follow requests yet</p>
            ) : (
                <ul className="follower-request-list">
                    {requests?.map((request) =>(
                        <li key={request.actor.id}>
                            <div className="requester-info">
                                <Link to={`/${request.actor.id}`} className="requester-name">
                                    {request.actor.username}
                                </Link>
                                <button
                                    onClick={() => handleApproveOrReject(request.object.id, request.actor.id, "accept")}
                                    className="approve-btn"
                                >
                                ✅
                                </button>
                                {/* Decline Button ❌ */}
                                <button
                                    onClick={() => handleApproveOrReject(request.object.id, request.actor.id, "reject")}
                                    className="reject-btn"
                                >
                                ❌
                                </button>
                            </div>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    )
}

export default FollowRequests;