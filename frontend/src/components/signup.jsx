import React, { useState } from 'react';
import { useCreateUserMutation } from '../Api';

const CreateUser = () => {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });

  const [createUser] = useCreateUserMutation();
  const [successMessage, setSuccessMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSuccessMessage(''); 
    setErrorMessage(''); 

    try {
      const response = await createUser(formData).unwrap();
      console.log('User created:', response);
      setSuccessMessage('User created successfully!');
    } catch (err) {
      console.error('Error creating user:', err);
      setErrorMessage(err.data?.message || 'Failed to create user. Please try again.');
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
      {successMessage && <p style={{ color: 'green' }}>{successMessage}</p>}
      {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
    </form>
  );
};

export default CreateUser;