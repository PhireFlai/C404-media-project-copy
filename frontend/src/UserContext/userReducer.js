const initialState = {
  user: JSON.parse(localStorage.getItem("user")) || null, // Load from localStorage
};

const userReducer = (state = initialState, action) => {
  switch (action.type) {
    case "LOGIN_USER":
      // Store user in localStorage
      localStorage.setItem("user", JSON.stringify(action.payload));
      return {
        ...state,
        user: action.payload,
      };
    case "LOGOUT_USER":
      localStorage.removeItem("user"); // Remove user from localStorage
      localStorage.removeItem("token"); // Also remove the token
      return {
        ...state,
        user: null,
      };
    default:
      return state;
  }
};

export default userReducer;
