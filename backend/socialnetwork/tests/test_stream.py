from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from socialnetwork.models import User, Post
from django.db.models import Q

class FeedStreamTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Users
        self.user1 = User.objects.create(username="user1")
        self.user2 = User.objects.create(username="user2")
        self.user3 = User.objects.create(username="user3")
        self.user4 = User.objects.create(username="user4")

        # Tokens
        self.token1 = Token.objects.create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        self.token2 = Token.objects.create(user=self.user2)
        self.token3 = Token.objects.create(user=self.user3)

        # Relationships
        self.user1.friends.add(self.user2)
        self.user2.friends.add(self.user1)
        self.user1.following.add(self.user3)

        # Posts by user2 (friend)
        self.friend_public = Post.objects.create(author=self.user2, content="Friend Public", visibility=Post.PUBLIC)
        self.friend_friends = Post.objects.create(author=self.user2, content="Friend Only", visibility=Post.FRIENDS_ONLY)
        self.friend_unlisted = Post.objects.create(author=self.user2, content="Unlisted", visibility=Post.UNLISTED)
        self.friend_deleted = Post.objects.create(author=self.user2, content="Deleted", visibility=Post.DELETED)

        # Posts by user3 (followed)
        self.followed_public = Post.objects.create(author=self.user3, content="Followed Public", visibility=Post.PUBLIC)
        self.followed_unlisted = Post.objects.create(author=self.user3, content="Unlisted", visibility=Post.UNLISTED)
        self.followed_friends = Post.objects.create(author=self.user3, content="Friend Only", visibility=Post.FRIENDS_ONLY)

        # Self post
        self.self_post = Post.objects.create(author=self.user1, content="My Post", visibility=Post.PUBLIC)

    def test_public_feed(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        url = reverse('public-feed')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        post_ids = {post['id'].rstrip('/').split('/')[-1] for post in response.json()}

        # Posts that should appear
        self.assertIn(str(self.self_post.id), post_ids)
        self.assertIn(str(self.friend_public.id), post_ids)
        self.assertIn(str(self.friend_friends.id), post_ids)
        self.assertIn(str(self.followed_public.id), post_ids)
        self.assertIn(str(self.followed_unlisted.id), post_ids)

        # Posts that should NOT appear
        self.assertNotIn(str(self.friend_deleted.id), post_ids)
        self.assertNotIn(str(self.followed_friends.id), post_ids)
        self.assertNotIn(str(self.friend_unlisted.id), post_ids)

    def test_friends_feed(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        url = reverse('friends-feed')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        post_ids = {post['id'].rstrip('/').split('/')[-1] for post in response.json()}

        self.assertIn(str(self.friend_friends.id), post_ids)
        self.assertIn(str(self.friend_unlisted.id), post_ids)
        self.assertNotIn(str(self.friend_public.id), post_ids)
        self.assertNotIn(str(self.friend_deleted.id), post_ids)
        self.assertNotIn(str(self.followed_public.id), post_ids)

    def test_followers_feed(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        url = reverse('followers-feed')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        post_ids = {post['id'].rstrip('/').split('/')[-1] for post in response.json()}

        self.assertIn(str(self.followed_unlisted.id), post_ids)
        self.assertNotIn(str(self.followed_public.id), post_ids)
        self.assertNotIn(str(self.followed_friends.id), post_ids)
        self.assertNotIn(str(self.friend_friends.id), post_ids)
        self.assertNotIn(str(self.friend_public.id), post_ids)