from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import Post, Comment, Like, User
from rest_framework.authtoken.models import Token

from django.contrib.contenttypes.models import ContentType

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
        self.assertTrue(Like.objects.filter(object_id=self.post.id, user=self.user).exists())

    def test_like_comment(self):
        """Test liking a comment. - Comment/Likes 3"""
        data = {"user": self.user.id, "comment": self.comment.id}
        url = f'/api/authors/{self.user.id}/posts/{self.post.id}/comments/{self.comment.id}/like/'
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Like.objects.filter(object_id=self.comment.id, user=self.user).exists())
    
    def test_likes_by_author(self):
        """Test endpoint .//service/api/authors/{AUTHOR_SERIAL}/liked"""
        # Like the first post
        data = {"user": self.user.id, "post": self.post.id}
        url = f'/api/authors/{self.user.id}/posts/{self.post.id}/like/'
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Like.objects.filter(object_id=self.post.id, user=self.user).exists())

        # Like the second post
        data = {"user": self.user.id, "post": self.post2.id}
        url = f'/api/authors/{self.user.id}/posts/{self.post2.id}/like/'
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Like.objects.filter(object_id=self.post2.id, user=self.user).exists())

        # Retrieve likes by author
        url = f'/api/authors/{self.user.id}/liked/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_get_single_like_authors(self):
        """Test endpoint //service/api/authors/{AUTHOR_SERIAL}/liked/{LIKE_SERIAL}"""
        # Like the first post
        data = {"user": self.user.id, "post": self.post.id}
        url = f'/api/authors/{self.user.id}/posts/{self.post.id}/like/'
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        like_id = response.data['id']

        # Retrieve the single like
        # Get the full like ID from the POST response
        like_url = response.data['id']
        like_uuid = like_url.rstrip('/').split('/')[-1]  # extract UUID

        # Now use that UUID in the GET URL
        url = f'/api/authors/{self.user.id}/liked/{like_uuid}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'].rstrip('/').split('/')[-1], like_uuid)


    def test_get_single_like(self):
        """Test endpoint api/liked/<uuid:id>/"""
        # Create a like for the first post
        content_type = ContentType.objects.get_for_model(Post)
        like = Like.objects.create(user=self.user, content_type=content_type, object_id=self.post.id)
    
        # Retrieve the like using the endpoint
        url = f'/api/liked/{like.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #self.assertEqual(response.data['id'], str(like.id))
        returned_uuid = response.data['id'].rstrip('/').split('/')[-1]
        self.assertEqual(returned_uuid, str(like.id))


    def test_get_comment_likes(self):
        """Test retrieving likes for a comment."""
        # Like the comment
        data = {"user": self.user.id}
        url = f'/api/authors/{self.user.id}/posts/{self.post.id}/comments/{self.comment.id}/like/'
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
        # Retrieve likes for the comment
        url = f'/api/authors/{self.user.id}/posts/{self.post.id}/comments/{self.comment.id}/likes/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
