"""
Test Suite: Post Author Profile Linking

This test suite ensures that:
1. Each post includes the author's ID in the API response.
2. The author's ID can be used to navigate to their profile.
3. The author's profile is accessible via the correct API endpoint.

This helps users find and connect with each other through posts.
"""
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import Post
from rest_framework.authtoken.models import Token

User = get_user_model()

class PostProfileLinkAPITestCase(APITestCase):
    """Test suite to ensure posts include a reference to the author's profile."""

    @classmethod
    def setUpTestData(cls):
        """Creates test data once before all tests in the class."""
        cls.user = User.objects.create_user(username='author', password='password')
        cls.post = Post.objects.create(
            title="Test Post",
            content="This is a test post.",
            author=cls.user
        )
        cls.token = Token.objects.create(user=cls.user)

    def setUp(self):
        """Runs before each test."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_post_includes_author_id(self):
        """Test that a post response includes the author's ID, which can be used to navigate to their profile."""
        response = self.client.get(f'/api/posts/{self.post.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        
        # Verify the response contains the author's ID
        self.assertIn('author', response.data)
        self.assertIn('id', response.data['author'])
        self.assertEqual(response.data['author']['id'], str(self.user.id))

    def test_author_profile_is_accessible(self):
        """Test that the author's profile can be accessed using their ID."""
        profile_response = self.client.get(f'/api/authors/{self.user.id}/')
        
        self.assertEqual(profile_response.status_code, status.HTTP_200_OK, profile_response.data)
        
        # Verify the profile contains expected user details
        self.assertEqual(profile_response.data['username'], self.user.username)
