import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import { logoutUser } from "../UserContext/userActions";
import Dropdown from "./dropdown.js";
import './css/navbar.css';

const Navbar = () => {
    const user = useSelector((state) => state.user.user); // Redux gets user state
    const dispatch = useDispatch();
    const navigate = useNavigate();

    const handleLogout = () => {
        dispatch(logoutUser());
        navigate("/login");
    };

    return (
        <nav>
        <ul>
            <li>
                <Link to="/">Home</Link>
            </li>
            <li>
                <Link to="/create">Create Post</Link>
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
