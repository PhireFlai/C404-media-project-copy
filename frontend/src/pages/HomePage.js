import React from "react";
import { useGetTestQuery } from "../Api";
const HomePage = () => {
  const { data, error, isLoading } = useGetTestQuery();

  // Handle loading state
  if (isLoading) return <p>Loading...</p>;

  // Handle error state
  if (error) {
    return <p>Error: {error.data?.message || "Something went wrong"}</p>;
  }

  return (
    <div>
      <h1>Home Page</h1>
      <h2>Test connection with backend, data from API:</h2>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
};

export default HomePage;
