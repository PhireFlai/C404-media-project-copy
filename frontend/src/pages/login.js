import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";
import { useLoginUserMutation } from "../Api";
import { loginUser as loginUserAction } from "../UserContext/userActions";
import "./css/login.css";

const LoginUser = () => {
  // State to manage form data
  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });

  const navigate = useNavigate();
  const dispatch = useDispatch();

  const [loginUser] = useLoginUserMutation(); // Mutation hook for logging in a user

  // State to manage success and error messages
  const [successMessage, setSuccessMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  // Handle form input changes
  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setSuccessMessage("");
    setErrorMessage("");

    try {
      // Log the user in
      const loginResponse = await loginUser({
        username: formData.username,
        password: formData.password,
      }).unwrap();
      console.log("User logged in:", loginResponse);

      setSuccessMessage("User logged in successfully!");

      const userData = {
        id: loginResponse.user_id,
        username: loginResponse.username,
      };

      dispatch(loginUserAction(userData)); // Update Redux state
      // Save the token and user data to local storage
      localStorage.setItem("token", loginResponse.token);
      localStorage.setItem(
        "user",
        JSON.stringify({
          id: loginResponse.user_id,
          username: loginResponse.username,
        })
      );

      navigate(`/${loginResponse.user_id}`); // Redirect to the user's profile page
    } catch (err) {
      console.error("Error:", err);
      setErrorMessage(err.data?.message || "Failed to log in user.");
    }
  };

  return (
    <>
      <h1 className="heading">Login Page</h1>
      <form onSubmit={handleSubmit} className="login-form">
        <div>
          <label>Username:</label>
          <input
            type="text"
            name="username"
            value={formData.username}
            onChange={handleChange}
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
          />
        </div>
        <div className="login-button-row">
          <button type="submit">Login</button>
          <button onClick={() => navigate("/signup")}>Create a User</button>
        </div>

        {/* Success and error messages */}
        {successMessage && <p style={{ color: "green" }}>{successMessage}</p>}
        {errorMessage && <p style={{ color: "red" }}>{errorMessage}</p>}
      </form>
    </>
  );
};

export default LoginUser;
