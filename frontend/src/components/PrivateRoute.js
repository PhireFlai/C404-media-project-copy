import React from "react";
import { Navigate } from "react-router-dom";
import { useSelector } from "react-redux";

const PrivateRoute = ({ element: Component, ...rest }) => {
  const user = useSelector((state) => state.user.user);

  return user ? <Component {...rest} /> : <Navigate to="/login" />;
};

export default PrivateRoute;