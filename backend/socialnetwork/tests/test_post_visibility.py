from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import Post
from rest_framework.authtoken.models import Token

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

    def create_post(self, title, content, visibility):
        """Helper function to create a post with a given visibility"""
        data = {
            "title": title,
            "content": content,
            "author": self.user.id,
            "visibility": visibility,
        }
        return self.client.post(f"/api/authors/{self.user.id}/posts/", data)

    def test_create_public_post(self):
        # Addresses Visibility 1 - Create Public Posts
        """Test creating a public post."""
        response = self.create_post("Public Post", "This is a public post", Post.PUBLIC)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["visibility"], Post.PUBLIC)

    def test_create_friends_only_post(self):
        # Addresses Visibility 3 - Create Friends-only Posts
        """Test creating a friends-only post."""
        response = self.create_post("Friends Only Post", "This is a friends-only post", Post.FRIENDS_ONLY)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["visibility"], Post.FRIENDS_ONLY)

    def test_create_unlisted_post(self):
        # Addresses Visibility 2 - Create Unlisted Posts
        """Test creating an unlisted post."""
        response = self.create_post("Unlisted Post", "This is an unlisted post", Post.UNLISTED)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["visibility"], Post.UNLISTED)