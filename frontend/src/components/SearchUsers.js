import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useSearchUsersQuery, useCreateRemoteFollowRequestMutation } from "../Api";

const parseFQId = (id) => {
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
    const navigate = useNavigate();
  
    // Fetch search results using the query
    const { data: searchResults = { users: [] }, isFetching } = useSearchUsersQuery(
      searchQuery,
      { skip: searchQuery.length < 2 }
    );
  
    // Placeholder mutation for creating remote follow requests
    const [createRemoteFollowRequest] = useCreateRemoteFollowRequestMutation();
  
    const handleFollow = async (userId) => {
      try {
        // Placeholder logic for creating a remote follow request
        await createRemoteFollowRequest({ target_user_id: userId }).unwrap();
        alert("Follow request sent!");
      } catch (error) {
        console.error("Error sending follow request:", error);
      }
    };
  
    return (
      <div className="search-users">
        <input
          type="text"
          placeholder="Search users..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        {isFetching && <p>Loading...</p>}
        {searchResults.users.length > 0 && (
          <ul className="search-dropdown">
            {searchResults.users.map((user) => (
              <li key={user.id}>
                {parseFQId(user.id) ? (
                  // If the user is local, redirect to their profile
                  <span onClick={() => navigate(`${user.id}`)}>
                    {user.username}
                  </span>
                ) : (
                  // If the user is remote, show the follow button or followed indicator
                  <>
                    <span>{user.username}</span>
                    <button
                      className="button-primary"
                      onClick={() => handleFollow(user.id)}
                    >
                      Follow
                    </button>
                  </>
                )}
              </li>
            ))}
          </ul>
        )}
      </div>
    );
};

export default SearchUsers;