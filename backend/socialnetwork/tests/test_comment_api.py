# from django.contrib.auth import get_user_model
# from rest_framework.test import APITestCase
# from rest_framework import status
# from ..models import Post, Comment
# from rest_framework.authtoken.models import Token

# User = get_user_model()

# class CommentAPITestCase(APITestCase):
#     """Test suite for the Comment API."""

#     @classmethod
#     def setUpTestData(cls):
#         """Creates test data once before all tests in the class."""
#         cls.user = User.objects.create_user(username='testuser', password='password')
#         cls.other_user = User.objects.create_user(username='otheruser', password='password')
#         cls.post = Post.objects.create(title="Test Post", content="Content here", author=cls.user)
#         cls.post2 = Post.objects.create(title="Test Post 2", content="Content", author=cls.other_user)
#         cls.comment = Comment.objects.create(content="Test Comment", author=cls.user, post=cls.post)
#         cls.comment2 = Comment.objects.create(content="Test Comment 2", author=cls.other_user, post=cls.post2)
#         cls.token = Token.objects.create(user=cls.user)
#         cls.other_token = Token.objects.create(user=cls.other_user)

#     def setUp(self):
#         """Runs before each test."""
#         self.client.login(username='testuser', password='password')
#         self.token = Token.objects.get(user=self.user)
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
#     def test_get_comments(self):
#         """Test retrieving comments for a post."""
#         response = self.client.get(f'/api/posts/{self.post.id}/comments/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertGreaterEqual(len(response.data), 1)
#         # Need to expand to check that the data is correct

    