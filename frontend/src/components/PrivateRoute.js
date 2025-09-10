import React from "react";
import { Navigate } from "react-router-dom";

const PrivateRoute = ({ element: Component, ...rest }) => {
  const user = JSON.parse(localStorage.getItem('user')); // Get the current user from local storage

  // If the user is logged in, render the component, otherwise redirect to the login page
  return user ? <Component {...rest} /> : <Navigate to="/login" />;
};

export default PrivateRoute;
