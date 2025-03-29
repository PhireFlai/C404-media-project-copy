import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  useSearchUsersQuery,
  useCreateRemoteFollowRequestMutation,
} from "../Api";
import parseId from "../utils/parseId";
import "./css/search.css";

const isLocal = (id) => {
  try {
    // Extract the domain from the FQID
    const url = new URL(id);
    const domain = url.hostname;

    // Get the current application's domain
    const localDomain = window.location.hostname;

    // Check if the domain matches the local domain
    return domain === localDomain;
  } catch (error) {
    return false; // Default to remote if parsing fails
  }
};

const SearchUsers = () => {
    const [searchQuery, setSearchQuery] = useState("");
    const [showResults, setShowResults] = useState(false); // State to control visibility of results
    const navigate = useNavigate();

    const { data: searchResults = { users: [] }, isFetching } =
        useSearchUsersQuery(searchQuery, { skip: searchQuery.length < 2 });

    // Mutation for creating remote follow requests
    const [createRemoteFollowRequest] = useCreateRemoteFollowRequestMutation();

    const handleFollow = async (remoteUser) => {
        try {
            // Assuming the user object is available in the component
            const user = JSON.parse(localStorage.getItem("user")); // Retrieve the user object from localStorage
            if (!user || !user.id || !user.username) {
                throw new Error("User object not found or incomplete in local storage");
            }

            const actorId = user.id; // Get the actorId from the user object
            const actorUsername = user.username; // Get the actor's username

            console.log("Sending follow request from:", actorId, "to:", remoteUser.id);

            // Send the follow request using the new API format
            await createRemoteFollowRequest({
                actorId,
                actorUsername,
                objectFQID: remoteUser.id,
                objectUsername: remoteUser.username,
            }).unwrap();

            alert("Follow request sent!");
        } catch (error) {
            console.error("Error sending follow request:", error);
            alert("Failed to send follow request.");
        }
    };

    const isFollowed = (followers) => {
        const currentUser = JSON.parse(localStorage.getItem("user"));
        if (!currentUser || !currentUser.id) return false;
    
        // Check if any follower contains the current user's ID
        return followers.some((follower) => follower.includes(currentUser.id));
      };
    
      const handleCloseResults = () => {
        setSearchQuery(""); // Clear the search query
        setShowResults(false); // Hide the results
      };

    const handleInputChange = (e) => {
        setSearchQuery(e.target.value);
        setShowResults(true); // Show results when typing
    };

    return (
        <div className="search-users">
            <input
                type="text"
                placeholder="Search users..."
                value={searchQuery}
                onChange={handleInputChange}
            />
            {isFetching && <p>Loading...</p>}
            {showResults && searchResults.users.length > 0 && (
            <div>
                <button className="close-button" onClick={handleCloseResults}>
                  X
                </button>
                <ul className="search-dropdown">
                    {searchResults.users.map((user) => (
                        <li key={user.id}>
                            {isLocal(user.id) ? (
                                // Local, so extract UUID and redirect to the profile
                                <span onClick={() => navigate(parseId(user.id))}>
                                    {user.username}
                                </span>
                            ) : (
                                // If the user is remote, show the follow button or followed indicator
                                <>
                                    <span>{user.username}</span>
                                    {isFollowed(user.followers) ? (
                                        <span className="followed-indicator">Followed</span>
                                    ) : (
                                        <button
                                            className="button-primary"
                                            onClick={() => handleFollow(user)} // Pass the entire user object
                                            >
                                            Follow
                                        </button>
                                    )}
                                </>
                            )}
                        </li>
                    ))}
                </ul>
            </div>
        )}
        </div>
    );
};

export default SearchUsers;
