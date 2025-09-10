"""
Test Suite: Post Visibility Logic

This test suite ensures that:
1. The post author can see all of their posts.
2. Mutual friends can see public, friends-only, and unlisted posts.
3. Followers (who are not mutual friends) can see only public and unlisted posts.
4. Strangers can see only public posts.

This follows the visibility ranking logic enforced in PostListCreateView.
"""

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import Post
from rest_framework.authtoken.models import Token

User = get_user_model()

class PostVisibilityLogicAPITestCase(APITestCase):
    """Test suite to ensure post visibility logic works as expected."""

    @classmethod
    def setUpTestData(cls):
        """Creates test data once before all tests in the class."""
        cls.author = User.objects.create_user(username='author', password='password')
        cls.viewer = User.objects.create_user(username='viewer', password='password')
        cls.follower = User.objects.create_user(username='follower', password='password')
        cls.mutual_friend = User.objects.create_user(username='friend', password='password')

        # Establish relationships
        cls.author.followers.add(cls.follower)  # Viewer follows author, but not mutual
        cls.author.followers.add(cls.mutual_friend)
        cls.mutual_friend.followers.add(cls.author)  # Mutual follow relationship

        # Create posts with different visibility settings
        cls.public_post = Post.objects.create(author=cls.author, title="Public Post", content="Public Content", visibility="public")
        cls.friends_post = Post.objects.create(author=cls.author, title="Friends-Only Post", content="Friends Content", visibility="friends")
        cls.unlisted_post = Post.objects.create(author=cls.author, title="Unlisted Post", content="Unlisted Content", visibility="unlisted")

        cls.token_author = Token.objects.create(user=cls.author)
        cls.token_viewer = Token.objects.create(user=cls.viewer)
        cls.token_follower = Token.objects.create(user=cls.follower)
        cls.token_friend = Token.objects.create(user=cls.mutual_friend)

    def setUp(self):
        """Runs before each test."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_author.key)

    def test_author_sees_all_posts(self):
        """The post author should see all their posts."""
        response = self.client.get(f'/api/authors/{self.author.id}/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # Should see all posts

    def test_mutual_friend_sees_friends_and_unlisted_posts(self):
        """Mutual friends should see public, friends-only, and unlisted posts."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_friend.key)
        response = self.client.get(f'/api/authors/{self.author.id}/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # Should see all posts

    def test_follower_sees_only_public_and_unlisted_posts(self):
        """A follower should only see public and unlisted posts (not friends-only)."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_follower.key)
        response = self.client.get(f'/api/authors/{self.author.id}/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Should only see public and unlisted

    def test_stranger_sees_only_public_posts(self):
        """A stranger should only see public posts."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_viewer.key)
        response = self.client.get('/api/public-posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should only see public post
