import React from 'react';
import { useGetUserPostsQuery } from '../Api';
import { useSelector } from 'react-redux';
import PostItem from './PostItem';

const UserPosts = () => {
  const user = useSelector((state) => state.user.user); // Get the user from the Redux store
  const { data: posts, refetch } = useGetUserPostsQuery(user.id); // Fetch user-specific posts

  return (
    <div className="user-posts">
      {posts && posts.length > 0 ? (
        posts.map((post) => <PostItem key={post.id} post={post} refetchPosts={refetch} />)
      ) : (
        <p>No posts yet.</p>
      )}
    </div>
  );
};

export default UserPosts;