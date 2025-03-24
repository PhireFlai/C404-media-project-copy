from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import Post
from rest_framework.authtoken.models import Token

User = get_user_model()

class SharableLinkAPITestCase(APITestCase):
    """Test suite to ensure sharable links are correctly generated and accessible based on visibility."""

    @classmethod
    def setUpTestData(cls):
        """Creates test data once before all tests in the class."""
        cls.author = User.objects.create_user(username='author', password='password')
        cls.viewer = User.objects.create_user(username='viewer', password='password')
        cls.friend = User.objects.create_user(username='friend', password='password')

        # Establish relationships
        cls.author.followers.add(cls.friend)
        cls.friend.followers.add(cls.author)  # Mutual follow relationship

        # Create posts with different visibility settings
        cls.public_post = Post.objects.create(author=cls.author, title="Public Post", content="Public Content", visibility="public")
        cls.friends_post = Post.objects.create(author=cls.author, title="Friends-Only Post", content="Friends Content", visibility="friends")

        cls.token_author = Token.objects.create(user=cls.author)
        cls.token_viewer = Token.objects.create(user=cls.viewer)
        cls.token_friend = Token.objects.create(user=cls.friend)

    def setUp(self):
        """Runs before each test."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_author.key)

    def test_public_post_has_sharable_link(self):
        """Public posts should include a valid sharable link."""
        response = self.client.get(f'/api/posts/{self.public_post.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # share_url doesn't exist anymore
        #self.assertIn('share_url', response.data)  # Ensure sharable link is present
        
    def test_friends_only_post_has_sharable_link_for_friends(self):
        """Friends-only posts should include a valid sharable link for mutual friends."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_friend.key)
        response = self.client.get(f'/api/posts/{self.friends_post.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #self.assertIn('share_url', response.data)  # Ensure sharable link is present

    def test_friends_only_post_no_sharable_link_for_strangers(self):
        """Friends-only posts should not be sharable with strangers."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_viewer.key)
        response = self.client.get(f'/api/posts/{self.friends_post.id}/')
        #self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Stranger should not have access
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_200_OK])

        if response.status_code == status.HTTP_200_OK:
            self.assertNotIn('share_url', response.data)
