import React from "react";
import { Navigate } from "react-router-dom";
import { useSelector } from "react-redux";

const PrivateRoute = ({ element: Component, ...rest }) => {
  const user = useSelector((state) => state.user.user); // Get the current user from the Redux store

  // If the user is logged in, render the component, otherwise redirect to the login page
  return user ? <Component {...rest} /> : <Navigate to="/login" />;
};

export default PrivateRoute;
