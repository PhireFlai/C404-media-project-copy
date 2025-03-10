from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from socialnetwork.models import User, Post
from django.db.models import Q

class UserFeedViewTest(TestCase):
    def setUp(self):
        """Setup test data including users, relationships, and posts."""
        self.client = APIClient()

        # Create users
        self.user1 = User.objects.create(username="user1")
        self.user2 = User.objects.create(username="user2")
        self.user3 = User.objects.create(username="user3")
        self.user4 = User.objects.create(username="user4")  # Non-friend/non-follower

        # Create authentication tokens
        self.token1 = Token.objects.create(user=self.user1)
        self.token2 = Token.objects.create(user=self.user2)
        self.token3 = Token.objects.create(user=self.user3)

        # Establish relationships:
        # Make user1 and user2 friends (mutual friendship)
        self.user1.friends.add(self.user2)
        self.user2.friends.add(self.user1)

        # Make user1 follow user3 (but not friends)
        self.user1.following.add(self.user3)

        # Create posts for user2 (friend of user1)
        self.public_post_user2 = Post.objects.create(
            author=self.user2, content="User2 Public Post", visibility=Post.PUBLIC
        )
        self.friends_only_post_user2 = Post.objects.create(
            author=self.user2, content="User2 Friends-Only Post", visibility=Post.FRIENDS_ONLY
        )
        self.deleted_post_user2 = Post.objects.create(
            author=self.user2, content="User2 Deleted Post", visibility=Post.DELETED
        )

        # Create posts for user3 (followed by user1 but not a friend)
        self.public_post_user3 = Post.objects.create(
            author=self.user3, content="User3 Public Post", visibility=Post.PUBLIC
        )
        self.unlisted_post_user3 = Post.objects.create(
            author=self.user3, content="User3 Unlisted Post", visibility=Post.UNLISTED
        )
        self.friends_only_post_user3 = Post.objects.create(
            author=self.user3, content="User3 Friends-Only Post", visibility=Post.FRIENDS_ONLY
        )

        # Create a post by user1 (the logged-in user)
        self.self_post = Post.objects.create(
            author=self.user1, content="User1 Self Post", visibility=Post.PUBLIC
        )

    def test_feed_for_friends(self):
        """
        Friends should see:
          - Their own posts.
          - Public posts.
          - Friends-only posts from friends.
          - Unlisted posts from friends.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        response = self.client.get(reverse('user-feed'))
        self.assertEqual(response.status_code, 200)

        # Convert all returned IDs to a set of strings
        post_ids = {post["id"] for post in response.json()}

        # Check that user1 sees their own post (as a string)
        self.assertIn(str(self.self_post.id), post_ids)
        # Check that user1 sees user2's public and friends-only posts
        self.assertIn(str(self.public_post_user2.id), post_ids)
        self.assertIn(str(self.friends_only_post_user2.id), post_ids)
        # Ensure deleted posts are excluded
        self.assertNotIn(str(self.deleted_post_user2.id), post_ids)

    def test_feed_for_followers(self):
        """
        A user who follows someone (but is not friends) should see that person's public and unlisted posts,
        but NOT friends-only posts.
        In our setup, user1 follows user3 but they are not friends.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        response = self.client.get(reverse('user-feed'))
        self.assertEqual(response.status_code, 200)
        post_ids = {post["id"] for post in response.json()}

        # For user3, user1 should see:
        self.assertIn(str(self.public_post_user3.id), post_ids)
        self.assertIn(str(self.unlisted_post_user3.id), post_ids)
        # But should NOT see user3's friends-only posts.
        self.assertNotIn(str(self.friends_only_post_user3.id), post_ids)

    def test_feed_for_non_friends_non_followers(self):
        """
        A user with no friend/following relationship should only see public posts.
        Here, user4 is not connected to anyone.
        """
        # Create token for user4
        token4 = Token.objects.create(user=self.user4)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token4.key}')
        response = self.client.get(reverse('user-feed'))
        self.assertEqual(response.status_code, 200)
        post_ids = {post["id"] for post in response.json()}

        # User4 should see public posts from any author.
        self.assertIn(str(self.public_post_user2.id), post_ids)
        self.assertIn(str(self.public_post_user3.id), post_ids)
        # User4 should NOT see friends-only or unlisted posts
        self.assertNotIn(str(self.friends_only_post_user2.id), post_ids)
        self.assertNotIn(str(self.friends_only_post_user3.id), post_ids)
        self.assertNotIn(str(self.unlisted_post_user3.id), post_ids)
        self.assertNotIn(str(self.deleted_post_user2.id), post_ids)

    def test_feed_excludes_deleted_posts(self):
        """Feed should never include deleted posts."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        response = self.client.get(reverse('user-feed'))
        self.assertEqual(response.status_code, 200)
        post_ids = {post["id"] for post in response.json()}
        self.assertNotIn(str(self.deleted_post_user2.id), post_ids)

    def test_feed_shows_latest_posts(self):
        """Feed should show the latest version of posts in descending order."""
        # Create a new public post by user2 which should be the most recent.
        new_post = Post.objects.create(
            author=self.user2, content="User2 Newer Public Post", visibility=Post.PUBLIC
        )
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        response = self.client.get(reverse('user-feed'))
        self.assertEqual(response.status_code, 200)
        posts = response.json()
        # The first post in the returned list should have the ID of new_post.
        self.assertEqual(str(posts[0]["id"]), str(new_post.id))