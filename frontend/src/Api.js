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
      query: () => `api/public-posts/`, // Endpoint for fetching public posts
    }),
    createPost: builder.mutation({
      query: ({ userId, formData }) => ({
        url: `api/authors/${userId}/posts/`, // Endpoint for creating a post
        method: "POST",
        body: formData,
        formData: true,
      }),
    }),
    deletePost: builder.mutation({
      query: ({ userId, postId }) => ({
        url: `api/authors/${userId}/posts/${postId}/`, // Endpoint for deleting a post
        method: "DELETE",
      }),
    }),
    editPost: builder.mutation({
      query: ({ userId, postId, updatedPost }) => ({
        url: `api/authors/${userId}/posts/${postId}/`, // Endpoint for editing a post
        method: "PUT",
        body: updatedPost,
      }),
    }),
    getTest: builder.query({
      query: () => "core/test", // Endpoint for fetching test data
    }),
    createUser: builder.mutation({
      query: (userData) => ({
        url: "api/signup/", // Endpoint for creating a user
        method: "POST",
        body: userData,
      }),
    }),
    loginUser: builder.mutation({
      query: (credentials) => ({
        url: "api/login/", // Endpoint for logging in a user
        method: "POST",
        body: credentials,
      }),
    }),
    createComment: builder.mutation({
      query: ({ userId, postId, commentData }) => ({
        url: `api/authors/${userId}/posts/${postId}/comment/`, // Endpoint for creating a comment
        method: "POST",
        body: commentData,
      }),
    }),
    postComment: builder.mutation({
      query: ({ author, commentId }) => ({
        url: `api/authors/${author}/inbox/`, // Endpoint for posting a comment to the author's inbox
        method: "POST",
        body: { comment_id: commentId },
      }),
    }),
    updateProfilePicture: builder.mutation({
      query: ({ userId, profilePicture }) => {
        const formData = new FormData();
        formData.append("profile_picture", profilePicture);
        return {
          url: `api/authors/${userId}/update-picture/`, // Endpoint for updating profile picture
          method: "PUT",
          body: formData,
        };
      },
    }),
    updateUsername: builder.mutation({
      query: ({ userId, newUsername }) => ({
        url: `api/authors/${userId}/`, // Endpoint for updating username
        method: "PUT",
        body: { newUsername },
      }),
    }),
    getComments: builder.query({
      query: ({ userId, postId }) =>
        `api/authors/${userId}/posts/${postId}/comments/`, // Endpoint for fetching comments
    }),
    getUserProfile: builder.query({
      query: (userId) => `api/authors/${userId}/`, // Endpoint for fetching user profile by userId
    }),
    getUserPosts: builder.query({
      query: (userId) => `api/authors/${userId}/posts/`, // Endpoint for fetching posts by userId
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
