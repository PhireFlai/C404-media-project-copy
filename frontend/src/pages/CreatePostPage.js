import React, { useState } from "react";
import { useCreatePostMutation, useGetPostsQuery } from "../Api";
import { useNavigate } from "react-router-dom";

const CreatePostPage = () => {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [image, setImage] = useState(null);
  const [createPost] = useCreatePostMutation();
  const { refetch } = useGetPostsQuery();
  const navigate = useNavigate();

  const handleImageChange = (e) => {
    setImage(e.target.files[0]); // Store the selected file
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("title", title);
    formData.append("content", content);
    if (image) {
      formData.append("image", image);
    }

    await createPost(formData); // Send form data including image
    await refetch();
    navigate("/");
  };

  return (
    <div>
      <h1>Create a Post</h1>
      <form onSubmit={handleSubmit} encType="multipart/form-data">
        <input
          type="text"
          placeholder="Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
        <textarea
          placeholder="Content"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          required
        />
        <input type="file" accept="image/*" onChange={handleImageChange} />{" "}
        {/* Image upload */}
        <button type="submit">Post</button>
      </form>
    </div>
  );
};

export default CreatePostPage;
