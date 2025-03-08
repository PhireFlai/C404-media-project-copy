from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import Post, Friendship
from rest_framework.authtoken.models import Token

User = get_user_model()

class FeedAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="password")
        cls.friend = User.objects.create_user(username="friend", password="password")
        cls.other_user = User.objects.create_user(username="otheruser", password="password")

        # Create a friendship
        Friendship.objects.create(user=cls.user, friend=cls.friend)

        # Create posts
        cls.public_post = Post.objects.create(author=cls.other_user, title="Public Post", visibility=Post.PUBLIC)
        cls.unlisted_post = Post.objects.create(author=cls.friend, title="Unlisted Post", visibility=Post.UNLISTED)
        cls.friends_only_post = Post.objects.create(author=cls.friend, title="Friends-Only Post", visibility=Post.FRIENDS_ONLY)
        #cls.private_post = Post.objects.create(author=cls.other_user, title="Private Post", visibility=Post.FRIENDS_ONLY)

        # Tokens
        cls.token = Token.objects.create(user=cls.user)

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_user_feed(self):
        """Test fetching the user's feed."""
        response = self.client.get(f"/api/authors/{self.user.id}/feed/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Extract post titles from response
        post_titles = [post["title"] for post in response.data]

        # Check if expected posts are in the feed
        self.assertIn("Public Post", post_titles)
        self.assertIn("Friends-Only Post", post_titles)
        self.assertIn("Unlisted Post", post_titles)
        self.assertNotIn("Private Post", post_titles)  # Private post shouldn't be visible