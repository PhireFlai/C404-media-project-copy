import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const api = createApi({
  reducerPath: "api",
  baseQuery: fetchBaseQuery({ baseUrl: "http://127.0.0.1:8000/" }), // Common base URL
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
} = api;





