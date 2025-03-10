import { useGetUserFeedQuery } from "../redux/api";
import { useSelector } from "react-redux";

const FeedPage = () => {
  const userId = useSelector((state) => state.auth.user.id);
  const { data: feed, error, isLoading } = useGetUserFeedQuery(userId);

  if (isLoading) return <p>Loading...</p>;
  if (error) return <p>Error loading feed</p>;

  return (
    <div>
      <h2>Your Feed</h2>
      {feed.map((post) => (
        <div key={post.id}>
          <h3>{post.title}</h3>
          <p>{post.content}</p>
        </div>
      ))}
    </div>
  );
};

export default FeedPage;