import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import HomePage from "./pages/HomePage";
import CreatePostPage from "./pages/CreatePostPage";
import SignUp from "./pages/signup";
import Login from "./pages/login";
import Profile from './pages/Profile';
import Navbar from "./components/navbar";
import PrivateRoute from "./components/PrivateRoute";
import { useSelector } from "react-redux";

const App = () => {
  const user = useSelector((state) => state.user.user);

  return (
    <div>
      <Router>
        {user && <Navbar />}
        <div className="container">
          <Routes>
            <Route path="/signup" element={<SignUp />} />
            <Route path="/login" element={<Login />} />
            <Route path="/" element={<PrivateRoute element={HomePage} />} />
            <Route path="/create" element={<PrivateRoute element={CreatePostPage} />} />
            <Route path="/:userId" element={<PrivateRoute element={Profile} />} />
          </Routes>
        </div>
      </Router>
    </div>
  );
};

export default App;
