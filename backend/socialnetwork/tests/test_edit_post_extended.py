"""
Test Suite: Edit Post Functionality

This test suite verifies that:
1. Authors can edit their own posts, including title, content, visibility, and images.
2. Unauthorized users cannot modify someone else's post.
3. Proper permissions are enforced for updating visibility and uploading images.

Ensures that only the post author has full control over their post updates.
"""

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io
from ..models import Post
from rest_framework.authtoken.models import Token


User = get_user_model()

def generate_test_image():
    """Generates a valid in-memory test image."""
    image = Image.new("RGB", (100, 100), "white")
    image_io = io.BytesIO()
    image.save(image_io, format='JPEG')
    return SimpleUploadedFile("test.jpg", image_io.getvalue(), content_type="image/jpeg")

class EditPostExtendedAPITestCase(APITestCase):
    """Test suite for extended post editing (visibility and images)."""

    @classmethod
    def setUpTestData(cls):
        """Creates test data once before all tests in the class."""
        cls.user = User.objects.create_user(username='author', password='password')
        cls.other_user = User.objects.create_user(username='otheruser', password='password')

        cls.post = Post.objects.create(
            title="Original Title",
            content="Original Content",
            author=cls.user,
            visibility=Post.PUBLIC
        )

        cls.token = Token.objects.create(user=cls.user)
        cls.other_token = Token.objects.create(user=cls.other_user)

    def setUp(self):
        """Runs before each test."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_author_can_edit_visibility(self):
        """Test if an author can change the post visibility."""
        updated_data = {
            "title": "Updated Title",
            "content": "Updated Content",
            "visibility": Post.FRIENDS_ONLY  # Change visibility
        }
        response = self.client.put(f'/api/authors/{self.user.id}/posts/{self.post.id}/', updated_data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the visibility was updated
        self.post.refresh_from_db()
        self.assertEqual(self.post.visibility, Post.FRIENDS_ONLY)

    def test_author_can_edit_post_image(self):
        """Test if an author can update the post image."""
        image = generate_test_image()
        updated_data = {
            "title": "Updated Title",
            "content": "Updated Content",
            "image": image  # Upload new image
        }
        response = self.client.put(
            f'/api/authors/{self.user.id}/posts/{self.post.id}/',
            updated_data,
            format='multipart'  
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        
        # Verify the image was updated
        self.post.refresh_from_db()
        self.assertIsNotNone(self.post.image)

    def test_other_user_cannot_edit_visibility_or_image(self):
        """Test if another user cannot change visibility or image."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.other_token.key)  # Switch to another user
        
        updated_data = {
            "title": "Hacked Title",
            "content": "Hacked Content",
            "visibility": Post.UNLISTED  # Attempt to change visibility
        }
        response = self.client.put(f'/api/authors/{self.user.id}/posts/{self.post.id}/', updated_data)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.data)

        # Verify the post was NOT updated
        self.post.refresh_from_db()
        self.assertNotEqual(self.post.visibility, Post.UNLISTED)

        # Test image upload by unauthorized user
        image = generate_test_image()
        response = self.client.put(
            f'/api/authors/{self.user.id}/posts/{self.post.id}/',
            {"title": "Hacked Title", "content": "Hacked Content", "image": image},
            format='multipart'  # Ensure correct format
        )
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.data)

        #  Refresh Post Object Before Checking Image
        self.post.refresh_from_db()
        
        # Ensure image was NOT changed
        self.assertFalse(bool(self.post.image), "Unauthorized user should not be able to change the image")