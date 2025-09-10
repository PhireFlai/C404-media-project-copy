from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import Post
from rest_framework.authtoken.models import Token

User = get_user_model()

class EditPostPermissionsAPITestCase(APITestCase):
    """Test suite to ensure other users cannot modify an author's post."""

    @classmethod
    def setUpTestData(cls):
        """Creates test data once before all tests in the class."""
        cls.author = User.objects.create_user(username='author1', password='password')
        cls.other_author = User.objects.create_user(username='author2', password='password')

        cls.post = Post.objects.create(
            title="Original Post",
            content="Original Content",
            author=cls.author
        )

        cls.author_token = Token.objects.create(user=cls.author)
        cls.other_author_token = Token.objects.create(user=cls.other_author)

    def setUp(self):
        """Runs before each test."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.other_author_token.key)  # Auth as another user

    def test_other_author_cannot_edit_post(self):
        """Test that a different author cannot modify someone else's post."""
        updated_data = {
            "title": "Unauthorized Edit",
            "content": "Unauthorized Content"
        }
        response = self.client.put(f'/api/authors/{self.author.id}/posts/{self.post.id}/', updated_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Verify the post was NOT updated
        self.post.refresh_from_db()
        self.assertNotEqual(self.post.title, updated_data["title"])
        self.assertNotEqual(self.post.content, updated_data["content"])
