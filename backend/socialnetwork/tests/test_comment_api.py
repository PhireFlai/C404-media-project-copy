from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import Post, Comment
from rest_framework.authtoken.models import Token
import uuid

User = get_user_model()

class CommentAPITestCase(APITestCase):
    """Test suite for the Comment API."""

    @classmethod
    def setUpTestData(cls):
        """Creates test data once before all tests in the class."""
        cls.user = User.objects.create_user(username='testuser', password='password')
        cls.other_user = User.objects.create_user(username='otheruser', password='password')
        cls.post = Post.objects.create(title="Test Post", content="Content here", author=cls.user)
        cls.post2 = Post.objects.create(title="Test Post 2", content="Content", author=cls.other_user)
        cls.comment = Comment.objects.create(comment="Test Comment", author=cls.user, post=cls.post)
        cls.comment.remote_fqid = None
        cls.comment2 = Comment.objects.create(comment="Test Comment 2", author=cls.other_user, post=cls.post2)
        cls.comment2.remote_fqid = None 
        cls.token = Token.objects.create(user=cls.user)
        cls.other_token = Token.objects.create(user=cls.other_user)
        


    def setUp(self):
        """Runs before each test."""
        self.client.login(username='testuser', password='password')
        self.token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
    def test_get_comments(self):
        """Test retrieving comments for a post."""
        response = self.client.get(f'/api/authors/{self.user.id}/posts/{self.post.id}/comments/')
        # print(response2.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_comment(self):
        comment_id = str(uuid.uuid4())

        # Construct the expected ID structure
        author_id = str(self.user.id)
        post_id = str(self.post.id)
        comment_url = f"http://testserver/api/authors/{author_id}/posts/{post_id}/comments/{comment_id}/"

        data = {
            "type": "comment",
            "id": comment_url,
            "comment": "New comment",
            "author": {
                "id": f"http://testserver/api/authors/{author_id}/"
            },
            "post": comment_url  # <- key change
        }

        response = self.client.post(f'/api/authors/{author_id}/inbox/', data, format='json')
        print("RESPONSE:", response.status_code, response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        comment = Comment.objects.get(id=comment_id)
        self.assertEqual(comment.comment, data["comment"])

    def test_get_comment_on_post(self):
        response = self.client.get(f'/api/authors/{self.user.id}/posts/{self.post.id}/comments/{self.comment.id}/')
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['comment'], self.comment.comment)

    def test_get_commented(self):
        response = self.client.get(f'/api/authors/{self.user.id}/commented/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    '''
    def test_post_commented(self):
        # Use fully qualified URL for author
        author_url = f"http://testserver/api/authors/{self.user.id}/"

        data = {
            "type": "comment",
            "comment": "New test comment",
            "author": {
                "id": author_url
            },
            "post": str(self.post.id)
        }

        response = self.client.post(f'/api/authors/{self.user.id}/commented/', data, format='json')
        print("RESPONSE:", response.status_code, response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Extract full ID URL from response
        full_id = response.data.get("id", "")
        
        try:
            # Extract UUID from full URL
            comment_uuid_str = full_id.rstrip("/").split("/")[-1]
            comment_uuid = uuid.UUID(comment_uuid_str)
        except Exception as e:
            self.fail(f"Invalid UUID extracted from comment id URL: {full_id} - {e}")

        # Check the comment was saved correctly
        comment = Comment.objects.get(id=comment_uuid)
        self.assertEqual(comment.comment, data["comment"])
    '''

    def test_get_comment_from_commented(self):
        response = self.client.get(f'/api/authors/{self.user.id}/commented/{self.comment.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['comment'], self.comment.comment)