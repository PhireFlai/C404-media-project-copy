import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const api = createApi({
  reducerPath: "api",
  baseQuery: fetchBaseQuery({
    baseUrl: "http://127.0.0.1:8000/", // Common base URL
    prepareHeaders: (headers) => {
      const token = localStorage.getItem("token"); // Get the token from local storage
      if (token) {
        headers.set("Authorization", `Token ${token}`); // Add the token to the headers
      }
      return headers;
    },
  }),
  endpoints: (builder) => ({
    getPosts: builder.query({
      query: () => `api/public-posts/`, // Updated endpoint for public posts
    }),
    createPost: builder.mutation({
      query: ({ userId, formData }) => ({
        url: `api/authors/${userId}/posts/`,
        method: "POST",
        body: formData,
        formData: true,
      }),
    }),
    deletePost: builder.mutation({
      query: ({ userId, postId }) => ({
        url: `api/authors/${userId}/posts/${postId}/`,
        method: "DELETE",
      }),
    }),
    editPost: builder.mutation({
      query: ({ userId, postId, updatedPost }) => ({
        url: `api/authors/${userId}/posts/${postId}/`,
        method: "PUT",
        body: updatedPost,
      }),
    }),
    getTest: builder.query({
      query: () => "core/test",
    }),
    createUser: builder.mutation({
      query: (userData) => ({
        url: "api/signup/",
        method: "POST",
        body: userData,
      }),
    }),
    loginUser: builder.mutation({
      query: (credentials) => ({
        url: "api/login/",
        method: "POST",
        body: credentials,
      }),
    }),
    createComment: builder.mutation({
      query: ({ userId, postId, commentData }) => ({
        url: `api/authors/${userId}/posts/${postId}/comment/`,
        method: "POST",
        body: commentData,
      }),
    }),
    postComment: builder.mutation({
      query: ({ author, commentId }) => ({
        url: `api/authors/${author}/inbox/`,
        method: "POST",
        body: { comment_id: commentId },
      }),
    }),
    updateProfilePicture: builder.mutation({
      query: ({ userId, profilePicture }) => {
        const formData = new FormData();
        formData.append("profile_picture", profilePicture);
        return {
          url: `api/authors/${userId}/update-picture/`,
          method: "PUT",
          body: formData,
        };
      },
    }),
    updateUsername: builder.mutation({
      query: ({ userId, newUsername }) => ({
        url: `api/authors/${userId}/`,
        method: "PUT",
        body: { newUsername },
      }),
    }),
    getComments: builder.query({
      query: ({ userId, postId }) =>
        `api/authors/${userId}/posts/${postId}/comments/`,
    }),
    getUserProfile: builder.query({
      query: (userId) => `api/authors/${userId}/`, // Fetch profile by userId
    }),
    getUserPosts: builder.query({
      query: (userId) => `api/authors/${userId}/posts/`, // Updated endpoint
    }),
  }),
});

// Export hooks for each endpoint
export const {
  useGetPostsQuery,
  useCreatePostMutation,
  useDeletePostMutation,
  useGetTestQuery,
  useCreateUserMutation,
  useLoginUserMutation,
  useEditPostMutation,
  useCreateCommentMutation,
  useGetCommentsQuery,
  useGetUserProfileQuery,
  useUpdateProfilePictureMutation,
  useUpdateUsernameMutation,
  usePostCommentMutation,
  useGetUserPostsQuery,
} = api;
