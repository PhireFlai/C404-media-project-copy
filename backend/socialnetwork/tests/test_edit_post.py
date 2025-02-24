from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import Post
from rest_framework.authtoken.models import Token

User = get_user_model()

class EditPostAPITestCase(APITestCase):
    """Test suite for editing a post."""

    @classmethod
    def setUpTestData(cls):
        """Creates test data once before all tests in the class."""
        cls.user = User.objects.create_user(username='author', password='password')
        cls.other_user = User.objects.create_user(username='otheruser', password='password')

        cls.post = Post.objects.create(
            title="Original Title", 
            content="Original Content", 
            author=cls.user
        )

        cls.token = Token.objects.create(user=cls.user)
        cls.other_token = Token.objects.create(user=cls.other_user)

    def setUp(self):
        """Runs before each test."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_author_can_edit_own_post(self):
        """Test if an author can edit their own post."""
        updated_data = {
            "title": "Updated Title",
            "content": "Updated Content"
        }
        response = self.client.put(f'/api/authors/{self.user.id}/posts/{self.post.id}/', updated_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the post was updated
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, updated_data["title"])
        self.assertEqual(self.post.content, updated_data["content"])

    def test_other_user_cannot_edit_post(self):
        """Test if another user cannot edit someone else's post."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.other_token.key)  # Switch to another user

        updated_data = {
            "title": "Hacked Title",
            "content": "Hacked Content"
        }
        response = self.client.put(f'/api/authors/{self.user.id}/posts/{self.post.id}/', updated_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Should not be allowed

        # Verify the post was NOT updated
        self.post.refresh_from_db()
        self.assertNotEqual(self.post.title, updated_data["title"])
        self.assertNotEqual(self.post.content, updated_data["content"])
