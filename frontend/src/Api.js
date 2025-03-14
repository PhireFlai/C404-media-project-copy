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
    getFriendsPosts: builder.query({
      query: (userId) => `api/authors/${userId}/friends-posts/`, // Endpoint for fetching friends posts
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
      query: ({ userId, postId, updatedPost }) => {
        const formData = new FormData();

        // Append text fields
        formData.append("title", updatedPost.title);
        formData.append("content", updatedPost.content);
        formData.append("visibility", updatedPost.visibility);
        // Append image if it exists
        if (updatedPost.image) {
          formData.append("image", updatedPost.image);
        }

        return {
          url: `api/authors/${userId}/posts/${postId}/`,
          method: "PUT",
          body: formData,
        };
      },
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
    addLike: builder.mutation({
      query: ({ userId, postId }) => ({
        url: `api/authors/${userId}/posts/${postId}/like/`,
        method: "POST",
      }),
    }),
    getLikes: builder.query({
      query: ({ userId, postId }) =>
        `api/authors/${userId}/posts/${postId}/likes/`, // Endpoint for fetching likes
    }),
    addCommentLike: builder.mutation({
      query: ({ userId, postId, commentId }) => ({
        url: `api/authors/${userId}/posts/${postId}/comments/${commentId}/like/`, // Endpoint for liking a comment
        method: "POST",
      }),
    }),
    getCommentLikes: builder.query({
      query: ({ userId, postId, commentId }) =>
        `api/authors/${userId}/posts/${postId}/comments/${commentId}/likes/`, // Endpoint for fetching likes for comments
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
    // Get followers list
    getFollowers: builder.query({
      query: (userId) => `api/authors/${userId}/followers/`,
    }),
    getFriends: builder.query({
      query: (userId) => `api/authors/${userId}/friends/`,
    }),
    getFollowing: builder.query({
      query: (userId) => `api/authors/${userId}/following/`,
    }),
  createFollowRequest: builder.mutation({
      query: ({ actorId, objectId }) => ({
        url: `api/authors/${actorId}/follow/authors/${objectId}/`,
        method: "POST",
      }),
    }),
    acceptFollowRequest: builder.mutation({
      query: ({ objectId, actorId, action }) => ({
        url: `api/authors/${objectId}/accept-follow-request/authors/${actorId}/?action=${action}`,
        method: "POST",
      }),
    }),
    unfollowUser: builder.mutation({
      query: ({ followerId, followedId }) => ({
        url: `api/authors/${followerId}/unfollow/authors/${followedId}/`,
        method: "POST",
      }),
    }),
    removeFollower: builder.mutation({
      query: ({ followedId, followerId }) => ({
        url: `api/authors/${followedId}/remove-follower/authors/${followerId}/`,
        method: "POST",
      }),
    }),
    getFollowRequests: builder.query({
      query: (objectId) => `api/authors/${objectId}/follow-requests/`,
    }),
    postToInbox: builder.mutation({
      query: ({ receiver, data }) => ({
        url: `api/authors/${receiver}/inbox/`,
        method: "POST",
        body: data,
      }),
    }),
    getPostComment: builder.query({
      query: ({ userId, postId, commentId }) =>
        `api/authors/${userId}/posts/${postId}/comments/${commentId}/`,
    }),
    getAuthorComments: builder.query({
      query: (userId) => `api/authors/${userId}/commented/`,
    }),
    getAuthorComment: builder.query({
      query: ({ userId, commentId }) =>
        `api/authors/${userId}/commented/${commentId}/`,
    }),
    getPost: builder.query({
      query: (postId) => `api/posts/${postId}/`, //endpoint for fetching a single post
    }),
    getUserFeed: builder.query({
      query: () => `api/authors/feed/`, //endpoint for user feed
    }),    
  }),
});

// Export hooks for each endpoint
export const {
  useGetFriendsPostsQuery,
  useCreatePostMutation,
  useDeletePostMutation,
  useGetTestQuery,
  useCreateUserMutation,
  useLoginUserMutation,
  useEditPostMutation,
  useCreateCommentMutation,
  useAddLikeMutation,
  useGetLikesQuery,
  useAddCommentLikeMutation,
  useGetCommentLikesQuery,
  useGetCommentsQuery,
  useGetUserProfileQuery,
  useUpdateProfilePictureMutation,
  useUpdateUsernameMutation,
  useGetUserPostsQuery,
  useGetFollowersQuery,
  useGetFriendsQuery,
  useGetFollowingQuery,
  useCreateFollowRequestMutation,
  useAcceptFollowRequestMutation,
  useUnfollowUserMutation,
  useRemoveFollowerMutation,
  useGetPostCommentQuery,
  useGetAuthorCommentsQuery,
  useGetAuthorCommentQuery,
  usePostToInboxMutation,
  useGetFollowRequestsQuery,
  useGetPostQuery,
  useGetUserFeedQuery,
} = api;
