import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import Dropdown from "./Dropdown";
import FollowRequests from "./FollowRequests"; // Import your separate FollowRequests component
import "./css/navbar.css";

const Navbar = () => {
  const [user, setUser] = useState(JSON.parse(localStorage.getItem("user")));
  const navigate = useNavigate();



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
        {user && (
          <>
            {/* <li>
              <Link to="/friends-only">Friends Only</Link>
            </li> */}
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