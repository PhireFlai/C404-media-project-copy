import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom"; // Import Router, Route, and Routes from react-router-dom for routing
import HomePage from "./pages/HomePage"; // Import HomePage component
import CreatePostPage from "./pages/CreatePostPage"; // Import CreatePostPage component
import SignUp from "./pages/Signup"; // Import SignUp component
import Login from "./pages/Login"; // Import Login component
import Profile from "./pages/Profile"; // Import Profile component
import Navbar from "./components/Navbar"; // Import Navbar component
import PrivateRoute from "./components/PrivateRoute"; // Import PrivateRoute component for protected routes
import FollowersList from "./pages/FollowerList";
import FollowingList from "./pages/FollowingList";
import FriendsOnlyPosts from "./pages/FriendsOnlyPosts";

const App = () => {
  // const user = JSON.parse(localStorage.getItem('user')); // Get the current user from local storage

  return (
    <div>
      <Router>
        {<Navbar />}
        <div className="container">
          <Routes>
            <Route path="/signup" element={<SignUp />} />{" "}
            {/* Route for the signup page */}
            <Route path="/login" element={<Login />} />{" "}
            {/* Route for the login page */}
            <Route path="/" element={<HomePage />} />{" "}
            {/*Route for the home page */}
            <Route
              path="/create"
              element={<PrivateRoute element={CreatePostPage} />}
            />{" "}
            <Route
              path="/friends-only"
              element={<PrivateRoute element={FriendsOnlyPosts} />}
            />{" "}
            {/* Protected route for the create post page */}
            <Route path="/:userId/followers" element={<FollowersList />} />{" "}
            <Route path="/:userId/following" element={<FollowingList />} />{" "}
            <Route
              path="/:userId"
              element={<Profile />}
            />{" "}
          </Routes>
        </div>
      </Router>
    </div>
  );
};

export default App;
