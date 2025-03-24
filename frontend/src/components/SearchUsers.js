import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useSearchUsersQuery } from "../Api";

const SearchUsers = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const navigate = useNavigate();

  // Fetch search results using the query
  const { data: searchResults = { users: [] }, isFetching } = useSearchUsersQuery(
    searchQuery,
    { skip: searchQuery.length < 2 }
  );

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
              <span onClick={() => navigate(`/${user.id}`)}>{user.username}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default SearchUsers;