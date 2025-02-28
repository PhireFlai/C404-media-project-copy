import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useLoginUserMutation } from "../Api";
import "./css/login.css";

const LoginUser = () => {
  // State to manage form data
  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });

  const navigate = useNavigate();

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

      setSuccessMessage("User logged in successfully!");

      const userData = {
        id: loginResponse.user_id,
        username: loginResponse.username,
      };

      // Save the token and user data to local storage
      localStorage.setItem("token", loginResponse.token);
      localStorage.setItem("user", JSON.stringify(userData));

      // Manually trigger a navbar update
      window.dispatchEvent(new Event("navbarTrigger"));

      navigate(`/${loginResponse.user_id}`); // Redirect to the user's profile page
    } catch (err) {
      console.error("Error:", err);
      setErrorMessage(err.data?.message || "Failed to log in user.");
    }
  };

  return (
    <>
      <h1 className="title">Login Page</h1>
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
          <button className="button-primary" type="submit">
            Login
          </button>
          <button
            className="button-secondary"
            onClick={() => navigate("/signup")}
          >
            Create a User
          </button>
        </div>

        {/* Success and error messages */}
        {successMessage && <p className="success-message">{successMessage}</p>}
        {errorMessage && <p className="error-message">{errorMessage}</p>}
      </form>
    </>
  );
};

export default LoginUser;
