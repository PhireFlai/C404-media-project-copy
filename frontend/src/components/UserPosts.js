import React, { useEffect} from 'react';
import { useGetUserPostsQuery } from '../Api';
import PostItem from './PostItem';

const UserPosts = ({userId}) => {
  const { data: posts, refetch } = useGetUserPostsQuery(userId); // Fetch user-specific posts

  useEffect(() => {
    refetch();
  }, [refetch]);

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