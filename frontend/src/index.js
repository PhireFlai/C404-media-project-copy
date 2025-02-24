import React from "react";
import ReactDOM from "react-dom/client";
import { Provider } from "react-redux";
import { store } from "./store";
import App from "./App";

// Create a root element using React 18's createRoot method
const root = ReactDOM.createRoot(document.getElementById("root"));

// Render the App component wrapped with the Provider to make the Redux store available to the entire app
root.render(
  <Provider store={store}>
    <App />
  </Provider>
);
