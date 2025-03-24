import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import Dropdown from "./Dropdown";
import FollowRequests from "./FollowRequests"; // Import your separate FollowRequests component
import "./css/navbar.css";

const Navbar = () => {
  const [user, setUser] = useState(JSON.parse(localStorage.getItem("user")));
  const navigate = useNavigate();

  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const handleSearch = async (query) => {
    setSearchQuery(query);
    if (query.length < 2) {
      setSearchResults([]); // Clear results if query is too short
      return;
    }
  
    // Get the current hostname dynamically
    const host = window.location.hostname;
  
    try {
      const response = await fetch(
        `http://${host}:8000/api/search-users/?q=${query}`
      );
      const data = await response.json();
      setSearchResults(data.users);
    } catch (error) {
      console.error("Error fetching users:", error);
    }
  };  

  useEffect(() => {
    const handleStorageChange = () => {
      setUser(JSON.parse(localStorage.getItem("user")));
    };

    window.addEventListener("navbarTrigger", handleStorageChange);

    return () => {
      window.removeEventListener("navbarTrigger", handleStorageChange);
    };
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("user");
    localStorage.removeItem("token");
    setUser(null);
    navigate("/login");
  };

  return (
    <nav>
      <ul>
        <li>
          <Link to="/">Home</Link>
        </li>

        {user && ( //displays feed sections and search bar only on successful authentication
          <>
            {/* <li>
              <Link to="/friends-only">Friends Only</Link>
            </li> */}
            <li>
              <input
                type="text"
                placeholder="Search users..."
                value={searchQuery}
                onChange={(e) => handleSearch(e.target.value)}
              />
              {searchResults.length > 0 && (
                <ul className="search-dropdown">
                  {searchResults.map((user) => (
                    <li key={user.id} onClick={() => navigate(`/${user.id}`)}>
                      {user.username}
                    </li>
                  ))}
                </ul>
              )}
            </li>
            
            <li>
              <Link to="/friends-feed">Friends Feed</Link>
            </li>
            <li>
              <Link to="/followers-feed">Followers Feed</Link>
            </li>
            <li>
              <Dropdown label={`Follow Requests`}>
                <FollowRequests userId={user.id} />
              </Dropdown>
            </li>
          </>
        )}
        {user ? (
          <li>
            <Dropdown label={`${user.username}`}>
              <li>
                <Link to={`/${user.id}`}>Profile</Link>
              </li>
              <li>
                <button className="remove-shadow" onClick={handleLogout}>
                  Logout
                </button>
              </li>
            </Dropdown>
          </li>
        ) : (
          <button onClick={() => navigate("/login")}>Login</button>
        )}
      </ul>
    </nav>
  );
};

export default Navbar;