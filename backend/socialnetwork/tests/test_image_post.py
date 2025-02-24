import os
from pathlib import Path
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from ..models import Post

User = get_user_model()

class PostAPITestCase(APITestCase):
    """Test suite for the Post API."""

    @classmethod
    def setUpTestData(cls):
        """Creates test data once before all tests in the class."""
        cls.user = User.objects.create_user(username="testuser", password="password")
        cls.token = Token.objects.create(user=cls.user)

    def setUp(self):
        """Runs before each test."""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_create_post_with_image(self):
        # Addresses Posting 1 and 9 User Stories
        """Test creating a new post with an actual image file."""
        
        # Define the image path
        image_path = Path(settings.BASE_DIR) / "socialnetwork/tests/test_images/turbo-alpaca.png"

        # Check if the test image exists
        if not image_path.exists():
            self.fail(f"Test image not found at {image_path}. Please ensure the file exists.")

        # Load the actual image file
        with open(image_path, "rb") as img:
            image_file = SimpleUploadedFile(
                name="test_image.png",  # Keep extension consistent
                content=img.read(),
                content_type="image/png",  # Correct MIME type for PNG
            )

        # Prepare the request data
        data = {
            "title": "New Post with Image",
            "content": "New Content with Image",
            "author": self.user.id,
            "image": image_file,  # Using actual image file
        }

        # Send a POST request with multipart form data
        response = self.client.post(
            f"/api/authors/{self.user.id}/posts/",
            data,
            format="multipart",
        )

        # Debugging: Print response data
        print("Response Data:", response.data)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], data["title"])
        self.assertIn("image", response.data)  # Ensure image URL is returned

        # Print actual image path returned for debugging
        #print("Returned image path:", response.data["image"])

        file_path = Path(settings.MEDIA_ROOT) / "post_images/test_image.png"
        self.assertTrue(file_path.exists(), f"File {file_path} does not exist")