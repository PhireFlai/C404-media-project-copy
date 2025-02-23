import React from 'react';
import PostItem from './PostItem';

const UserPosts = ({ posts }) => {
  return (
    <div className="user-posts">
      {posts && posts.length > 0 ? (
        posts.map((post) => <PostItem key={post.id} post={post} refetchPosts={() => {}} />)
      ) : (
        <p>No posts yet.</p>
      )}
    </div>
  );
};

export default UserPosts;