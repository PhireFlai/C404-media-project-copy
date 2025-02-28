import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom"; // Import Router, Route, and Routes from react-router-dom for routing
import HomePage from "./pages/HomePage"; // Import HomePage component
import CreatePostPage from "./pages/CreatePostPage"; // Import CreatePostPage component
import SignUp from "./pages/Signup"; // Import SignUp component
import Login from "./pages/Login"; // Import Login component
import Profile from "./pages/Profile"; // Import Profile component
import Navbar from "./components/Navbar"; // Import Navbar component
import PrivateRoute from "./components/PrivateRoute"; // Import PrivateRoute component for protected routes

const App = () => {
  const user = JSON.parse(localStorage.getItem('user')); // Get the current user from local storage

  return (
    <div>
      <Router>
        {user && <Navbar />} {/* Render the Navbar if the user is logged in */}
        <div className="container">
          <Routes>
            <Route path="/signup" element={<SignUp />} />{" "}
            {/* Route for the signup page */}
            <Route path="/login" element={<Login />} />{" "}
            {/* Route for the login page */}
            <Route
              path="/"
              element={<PrivateRoute element={HomePage} />}
            />{" "}
            {/* Protected route for the home page */}
            <Route
              path="/create"
              element={<PrivateRoute element={CreatePostPage} />}
            />{" "}
            {/* Protected route for the create post page */}
            <Route
              path="/:userId"
              element={<PrivateRoute element={Profile} />}
            />{" "}
            {/* Protected route for the profile page */}
          </Routes>
        </div>
      </Router>
    </div>
  );
};

export default App;
