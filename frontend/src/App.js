import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import HomePage from "./pages/HomePage";
import SignUp from "./components/signup";
import CreatePostPage from "./pages/CreatePostPage";

const App = () => {
  return (
    <div>
      <Router>
        {/* <Navbar /> */}
        {/* This is a global component that will be shown on all the route/pages we declare here. I haven't implemented it, it is just an example
         */}
        <div className="container">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/signup" element={<SignUp />} />
            <Route path="/create" element={<CreatePostPage />} />
          </Routes>
        </div>
      </Router>
    </div>
  );
};

export default App;
