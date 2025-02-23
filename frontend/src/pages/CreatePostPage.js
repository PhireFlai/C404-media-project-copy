import React, { useState } from "react";
import { useCreatePostMutation, useGetPostsQuery } from "../Api";
import { useNavigate } from "react-router-dom";
import "./css/post.css";

const CreatePostPage = () => {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [image, setImage] = useState(null);
  const [visibility, setVisibility] = useState("public"); // Default to "public"
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

    formData.append("visibility", visibility);

    await createPost(formData); // Send form data including image
    await refetch();
    navigate("/");
  };

  return (
    <div class="post-container">
      <h1 class="create-post-title">Create a Post</h1>
      <form
        class="create-post-form"
        onSubmit={handleSubmit}
        encType="multipart/form-data"
      >
        <input
          class="post-title-input"
          type="text"
          placeholder="Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
        <br />
        <textarea
          class="post-content-textarea"
          placeholder="Content"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          required
        />
        <br />
        <p>Select a visibility option: </p>
        <select
          class="visibility-select"
          name="visibility"
          value={visibility}
          onChange={(e) => setVisibility(e.target.value)}
        >
          <option value="public">Public</option>
          <option value="friends-only">Friends Only</option>
          <option value="unlisted">Unlisted</option>
        </select>
        <input
          class="image-upload-input"
          type="file"
          accept="image/*"
          onChange={handleImageChange}
        />
        <br />
        <button class="submit-post-button" type="submit">
          Post
        </button>
      </form>
    </div>
  );
};

export default CreatePostPage;
