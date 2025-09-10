from django.test import TestCase
from unittest.mock import patch
from socialnetwork.models import User, Post
from socialnetwork.utils import create_github_posts
from time import sleep

class CreateGithubPostsTestCase(TestCase):
    def setUp(self):
        """Set up a test user with a GitHub URL."""
        self.user = User.objects.create(
            username="testuser",
            github="https://github.com/testuser",
            github_etag=None  # Initially, no ETag stored
        )

    @patch("socialnetwork.utils.requests.get")
    def test_create_github_posts_creates_new_posts(self, mock_get):
        """Test that GitHub events are turned into posts."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {
                "type": "PushEvent",
                "repo": {"name": "testuser/test-repo", "url": "https://github.com/testuser/test-repo"},
                "created_at": "2024-03-05T13:00:00Z"
            }
        ]
        mock_get.return_value.headers = {"ETag": '"test-etag-123"'}

        create_github_posts(self.user)

        # Verify that a post was created
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.first()
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.content, "New GitHub activity: PushEvent on testuser/test-repo at 2024-03-05T13:00:00Z. Find at https://github.com/testuser/test-repo")

        # Verify ETag is saved
        self.user.refresh_from_db()
        self.assertEqual(self.user.github_etag, '"test-etag-123"')

    @patch("socialnetwork.utils.requests.get")
    def test_create_github_posts_avoids_duplicate_posts(self, mock_get):
        """Test that duplicate GitHub events are not posted twice."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {
                "type": "PushEvent",
                "repo": {"name": "testuser/test-repo", "url": "https://github.com/testuser/test-repo"},
                "created_at": "2024-03-05T12:00:00Z"
            }
        ]
        mock_get.return_value.headers = {"ETag": '"test-etag-123"'}

        # Create the first post
        create_github_posts(self.user)
        self.assertEqual(Post.objects.count(), 1)

        # Try to create the same post again
        create_github_posts(self.user)
        self.assertEqual(Post.objects.count(), 1)  # Count should not increase

    @patch("socialnetwork.utils.requests.get")
    @patch("builtins.print")
    def test_create_github_posts_handles_no_new_events(self, mock_get, mock_print):
        """Test that no new posts are created if GitHub returns 304 (Not Modified)."""
        self.user.github_etag = '"test-etag-123"'  # Simulate an existing ETag
        self.user.save()

        mock_get.return_value.status_code = 304  # No new events
        create_github_posts(self.user)

        # No new posts should be created
        self.assertEqual(Post.objects.count(), 0)

    @patch("socialnetwork.utils.requests.get")
    @patch("builtins.print")
    def test_create_github_posts_handles_api_error(self, mock_get, mock_print):
        """Test that errors from GitHub API do not create posts."""
        mock_get.return_value.status_code = 500  # Simulate server error
        create_github_posts(self.user)

        # No posts should be created
        self.assertEqual(Post.objects.count(), 0)
