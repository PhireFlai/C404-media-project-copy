import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const api = createApi({
  reducerPath: "api",
  baseQuery: fetchBaseQuery({
    baseUrl: "http://127.0.0.1:8000/", // Common base URL
    prepareHeaders: (headers, { getState }) => {
      const token = localStorage.getItem('token'); // Get the token from local storage
      if (token) {
        headers.set('Authorization', `Token ${token}`); // Add the token to the headers
      }
      return headers;
    },
  }),
  endpoints: (builder) => ({
    getPosts: builder.query({
      query: () => "api/posts/",
    }),
    createPost: builder.mutation({
      query: (formData) => ({
        url: "api/posts/",
        method: "POST",
        body: formData,
        formData: true,
      }),
    }),
    deletePost: builder.mutation({
      query: (postId) => ({
        url: `api/posts/${postId}/`,
        method: "DELETE",
      }),
    }),
    editPost: builder.mutation({
      query: ({ postId, updatedPost }) => ({
        url: `api/posts/${postId}/`,
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
      query: ({ pk, commentData }) => ({
        url: `api/posts/${pk}/comment/`,
        method: "POST",
        body: commentData,
      }),
    }),
    postComment: builder.mutation({
      query: ({ author, commentId }) => ({
        url: `api/authors/${author}/inbox/`,
        method: "POST",
        body: {"comment_id": commentId},
      }),
    }),
    updateProfilePicture: builder.mutation({
      query: ({ username, profilePicture }) => {
        const formData = new FormData();
        formData.append('profile_picture', profilePicture);
        return {
          url: `api/profile/${username}/update-picture/`,
          method: 'PUT',
          body: formData,
        }
      },
    }),
    updateUsername: builder.mutation({
      query: ({ username, newUsername }) => ({
        url: `api/profile/${username}/update-username/`,
        method: 'PUT',
        body: { newUsername },
        headers: {
          Authorization: `Token ${localStorage.getItem('token')}`,
        },
      }),
    }),
    getComments: builder.query({
      query: (pk) => `api/posts/${pk}/comments/`,
    }),
    getUserProfile: builder.query({
      query: (username) => `api/profile/${username}/`, // Fetch profile by username
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
} = api;