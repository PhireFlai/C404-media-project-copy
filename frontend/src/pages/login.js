import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { useLoginUserMutation } from '../Api';
import { loginUser as loginUserAction } from '../UserContext/userActions';

const LoginUser = () => {
    const [formData, setFormData] = useState({
        username: '',
        password: '',
    });

    const navigate = useNavigate();
    const dispatch = useDispatch();

    const [loginUser] = useLoginUserMutation();

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
            const loginResponse = await loginUser({
                username: formData.username,
                password: formData.password,
            }).unwrap();
            console.log('User logged in:', loginResponse);

            setSuccessMessage('User logged in successfully!');

            const userData = {
                id: loginResponse.user_id,
                username: loginResponse.username,
            };

            dispatch(loginUserAction(userData));
            // Save the token or user data to local storage or state
            setSuccessMessage('User created and logged in successfully!');
            localStorage.setItem('token', loginResponse.token);
            localStorage.setItem('user', JSON.stringify({
                id: loginResponse.user_id,
                username: loginResponse.username,
            }));

            navigate(`/${loginResponse.user_id}`);

        } catch (err) {
            console.error('Error:', err);
            setErrorMessage(err.data?.message || 'Failed to create or log in user.');
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
            <button type="submit">Login</button>
            <button onClick={() => navigate('/signup')}>Create a User</button>

            {/* Success and error messages for testing*/}
            {successMessage && <p style={{ color: 'green' }}>{successMessage}</p>}
            {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
        </form>
    );
};

export default LoginUser;