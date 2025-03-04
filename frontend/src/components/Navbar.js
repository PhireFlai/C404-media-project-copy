import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import Dropdown from "./Dropdown.js";
import "./css/navbar.css";

const Navbar = () => {
  const [user, setUser] = useState(JSON.parse(localStorage.getItem("user"))); // State to manage the current user
  // eslint-disable-next-line
  const [forceRender, setForceRender] = useState(false); // Dummy state for forcing re-renders
  const navigate = useNavigate();

  useEffect(() => {
    const handleStorageChange = () => {
      setUser(JSON.parse(localStorage.getItem("user")));
      setForceRender(prev => !prev); // Toggle state to force re-render
    };

    window.addEventListener("navbarTrigger", handleStorageChange);

    return () => {
      window.removeEventListener("navbarTrigger", handleStorageChange);
    };
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("user"); // Remove the user from local storage
    localStorage.removeItem("token"); // Remove the token from local storage
    setUser(null); // Update the state to reflect the user is logged out
    navigate("/login");
  };



  return (
    <nav>
      <ul>
        <li>
          <Link to="/">Home</Link>
        </li>
        {user ? (
          <li>
            <Dropdown label={`${user.username}`}>
              <li>
                <Link to={`/${user.id}`}>Profile</Link>
              </li>
              <li>
                <button onClick={handleLogout}>Logout</button>
              </li>
            </Dropdown>
          </li>
        ) : (
          <li>
            <Link to={`/login`}>Login</Link>
          </li>
        )}
      </ul>
    </nav>
  );
};

export default Navbar;
