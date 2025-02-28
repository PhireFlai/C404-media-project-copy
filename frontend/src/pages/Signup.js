import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useCreateUserMutation, useLoginUserMutation } from "../Api";
import { useDispatch } from "react-redux";
import { loginUser as loginUserAction } from "../UserContext/userActions";
import "./css/signup.css";

const CreateUser = () => {
  // State to manage form data
  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });

  const navigate = useNavigate();
  const dispatch = useDispatch(); // Add Redux dispatch

  const [createUser] = useCreateUserMutation(); // Mutation hook for creating a user
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
      // 1: Create the user
      const createResponse = await createUser(formData).unwrap();
      console.log("User created:", createResponse);

      // 2: Log the user in
      const loginResponse = await loginUser({
        username: formData.username,
        password: formData.password,
      }).unwrap();
      console.log("User logged in:", loginResponse);

      // 3: Update Redux & Local Storage
      const userData = {
        id: loginResponse.user_id,
        username: loginResponse.username,
      };

      dispatch(loginUserAction(userData)); // Immediately updates Redux state
      // localStorage.setItem("token", loginResponse.token);
      // localStorage.setItem("user", JSON.stringify(userData));

      setSuccessMessage("User created and logged in successfully!");
      navigate("/"); // Redirect to the home page
    } catch (err) {
      console.error("Error:", err);
      setErrorMessage(err.data?.message || "Failed to create or log in user.");
    }
  };

  return (
    <>
      <h1 className="title">Sign Up</h1>
      <form onSubmit={handleSubmit} className="signup-form">
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
        <div className="button-row">
          <button className="button-primary" type="submit">
            Create User
          </button>
          <button
            className="button-secondary"
            type="button"
            onClick={() => navigate("/login")}
          >
            Back to Login
          </button>
        </div>

        {/* Success and error messages */}
        {successMessage && <p className="success-message">{successMessage}</p>}
        {errorMessage && <p className="error-message">{errorMessage}</p>}
      </form>
    </>
  );
};

export default CreateUser;
