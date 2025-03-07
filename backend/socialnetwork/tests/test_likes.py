from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import Post, Comment, Like, CommentLike
from rest_framework.authtoken.models import Token

User = get_user_model()

class LikeAPITestCase(APITestCase):
    """Test suite for the Like API."""

    @classmethod
    def setUpTestData(cls):
        """Creates test data once before all tests in the class."""
        cls.user = User.objects.create_user(username='testuser', password='password')
        cls.other_user = User.objects.create_user(username='otheruser', password='password')
        cls.post = Post.objects.create(title="Test Post", content="Content here", author=cls.user)
        cls.post2 = Post.objects.create(title="Test Post 2", content="Content", author=cls.other_user)
        cls.comment = Comment.objects.create(content="Test Comment", author=cls.user, post=cls.post)
        cls.comment2 = Comment.objects.create(content="Test Comment 2", author=cls.other_user, post=cls.post2)
        cls.token = Token.objects.create(user=cls.user)
        cls.other_token = Token.objects.create(user=cls.other_user)

    def setUp(self):
        """Runs before each test."""
        self.client.login(username='testuser', password='password')
        self.token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
    def test_like_post(self):
        """Test liking a post - Comment/Likes 2"""
        data = {"user": self.user.id, "post": self.post.id}
        url = f'/api/authors/{self.user.id}/posts/{self.post.id}/like/'
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Like.objects.filter(post=self.post, user=self.user).exists())

    def test_like_comment(self):
        """Test liking a comment. - Comment/Likes 3"""
        data = {"user": self.user.id, "comment": self.comment.id}
        url = f'/api/authors/{self.user.id}/posts/{self.post.id}/comments/{self.comment.id}/like/'
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(CommentLike.objects.filter(comment=self.comment, user=self.user).exists())
    
    def test_retrieve_post_like_count(self):
            """Test retrieving like count for a post. - Comment/Likes 4"""
            # User 1 likes the post
            self.client.login(username='testuser', password='password')
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
            url = f'/api/authors/{self.user.id}/posts/{self.post.id}/like/'
            response = self.client.post(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            # User 2 likes the post
            self.client.login(username='otheruser', password='password')
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.other_token.key)
            url = f'/api/authors/{self.other_user.id}/posts/{self.post.id}/like/'
            response = self.client.post(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            # Retrieve the post and check like count
            url = f'/api/authors/{self.user.id}/posts/{self.post.id}/'
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['like_count'], 2)