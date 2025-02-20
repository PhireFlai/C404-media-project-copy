import { configureStore } from "@reduxjs/toolkit";
import { api } from "./Api";
import userReducer from './UserContext/userReducer';

export const store = configureStore({
    reducer: {
        [api.reducerPath]: api.reducer,
        user: userReducer,
    },
    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware().concat(api.middleware),
});
