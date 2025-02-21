import { configureStore } from "@reduxjs/toolkit";
import { api } from "./Api";
import userReducer from "./UserContext/userReducer";

// Load initial user state from localStorage
const loadUserFromLocalStorage = () => {
  try {
    const user = localStorage.getItem("user");
    return user ? JSON.parse(user) : null;
  } catch (err) {
    console.error("Error loading user from localStorage", err);
    return null;
  }
};

const preloadedState = {
  user: { user: loadUserFromLocalStorage() },
};

export const store = configureStore({
  reducer: {
    [api.reducerPath]: api.reducer,
    user: userReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(api.middleware),
  preloadedState, // Set initial state with user data from localStorage
});
