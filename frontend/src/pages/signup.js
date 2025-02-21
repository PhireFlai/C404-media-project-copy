import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useCreateUserMutation, useLoginUserMutation } from "../Api";
import { useDispatch } from "react-redux";
import { loginUser as loginUserAction } from "../UserContext/userActions";

const CreateUser = () => {
  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });

  const navigate = useNavigate();
  const dispatch = useDispatch(); // Add Redux dispatch

  const [createUser] = useCreateUserMutation();
  const [loginUser] = useLoginUserMutation();

  const [successMessage, setSuccessMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

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
      localStorage.setItem("token", loginResponse.token);
      localStorage.setItem("user", JSON.stringify(userData));

      setSuccessMessage("User created and logged in successfully!");
      navigate("/");
    } catch (err) {
      console.error("Error:", err);
      setErrorMessage(err.data?.message || "Failed to create or log in user.");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
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
      <button type="submit">Create User</button>

      {/* Success and error messages for testing*/}
      {successMessage && <p style={{ color: "green" }}>{successMessage}</p>}
      {errorMessage && <p style={{ color: "red" }}>{errorMessage}</p>}
    </form>
  );
};

export default CreateUser;
