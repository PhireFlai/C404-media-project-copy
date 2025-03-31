import React, { useState } from "react";
import { useCreatePostMutation, useGetPublicFeedQuery } from "../Api";
import { useNavigate } from "react-router-dom";
import "./css/post.css";

const CreatePostPage = () => {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [image, setImage] = useState(null);
  const [visibility, setVisibility] = useState("PUBLIC"); // Default to "PUBLIC"
  const [createPost] = useCreatePostMutation();
  const { refetch } = useGetPublicFeedQuery();
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem('user')); // Get the current user from local storage

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

    formData.append("visibility", visibility);

    await createPost({ userId: user.id, formData }); // Send form data including image
    await refetch();
    navigate("/");
  };

  return (
    <div className="post-container">
      <h1 className="title">Create a Post</h1>
      <form
        className="create-post-form"
        onSubmit={handleSubmit}
        encType="multipart/form-data"
      >
        <input
          className="post-title-input"
          type="text"
          placeholder="Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
        <br />
        <textarea
          className="post-content-textarea"
          placeholder="Content"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          required
        />
        <br />
        <p>Select a visibility option: </p>
        <select
          className="visibility-select"
          name="visibility"
          value={visibility}
          onChange={(e) => setVisibility(e.target.value)}
        >
          <option value="PUBLIC">Public</option>
          <option value="FRIENDS">Friends Only</option>
          <option value="UNLISTED">Unlisted</option>
        </select>
        <input
          className="image-upload-input"
          type="file"
          accept="image/*"
          onChange={handleImageChange}
        />
        <br />
        <button className="button-primary" type="submit">
          Post
        </button>
      </form>
    </div>
  );
};

export default CreatePostPage;
