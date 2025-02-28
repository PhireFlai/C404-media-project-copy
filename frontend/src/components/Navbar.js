import React from "react";
import { Link, useNavigate } from "react-router-dom";
import Dropdown from "./dropdown.js";
import "./css/navbar.css";

const Navbar = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("user"); // Remove user from localStorage
    localStorage.removeItem("token"); // Also remove the token
    navigate("/login");
  };

  return (
    <nav>
      <ul>
        <li>
          <Link to="/">Home</Link>
        </li>
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
      </ul>
    </nav>
  );
};

export default Navbar;
